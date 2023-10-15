# views.py
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from system.models import JobCard
from webapp.forms.JobCardPDFForm import JobNumberForm
from webapp.models import PDFRecord


@method_decorator(login_required, name='dispatch')
class JobQuickView(View):
    template_name = 'job_quick_view.html'

    def get(self, request):
        form = JobNumberForm()
        recent_pdfs = PDFRecord.objects.filter(user=request.user).order_by('-timestamp')[:5]
        return render(request, self.template_name, {'form': form, 'recent_pdfs': recent_pdfs})

    def post(self, request):
        form = JobNumberForm(request.POST)
        form.submitted = True  # Set a flag indicating the form was submitted
        if form.is_valid():
            job_number = form.cleaned_data['job_number']
            try:
                job_card = JobCard.objects.get(job_number=job_number)
            except JobCard.DoesNotExist:
                job_card = None
            recent_pdfs = PDFRecord.objects.filter(user=request.user).order_by('-timestamp')[:5]
            return render(request, self.template_name, {'form': form, 'job_card': job_card, 'recent_pdfs': recent_pdfs})
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class JobCardPDFView(View):

    def get(self, request, job_card_id):
        job_card = get_object_or_404(JobCard, id=job_card_id)
        PDFRecord.objects.create(user=request.user, job_card=job_card)
        template_path = 'job_card_pdf.html'

        # Get the current date
        current_date = datetime.now().strftime('%B %d, %Y')

        context = {'job_card': job_card, 'current_date': current_date}

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{job_card.job_number}.pdf"'

        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(html, dest=response)
        return response
