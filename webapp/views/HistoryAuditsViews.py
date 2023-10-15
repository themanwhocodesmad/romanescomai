# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from system.models import JobCard
from webapp.forms.HistoryAuditsForm import JobCardQueryForm, JobHistoryForm
from webapp.forms.JobCardPDFForm import JobNumberForm
from webapp.models import JobCardHistory, JobCardHistory
from django.contrib import messages


@login_required
def job_history_query(request):
    form = JobNumberForm(request.POST or None)
    if form.is_valid():
        job_number = form.cleaned_data['job_number']
        job_card = JobCard.objects.filter(
            job_number=job_number).first()  # Use filter() and first() instead of get_object_or_404
        if job_card:
            return redirect('job_history_view', job_card_id=job_card.id)
        else:
            messages.error(request, "Job card not found, please try again.")  # Add an error message

    return render(request, 'jobcards/job_history_query.html', {'form': form})


@login_required
def job_history_view(request, job_card_id):
    job_card = get_object_or_404(JobCard, id=job_card_id)
    history = JobCardHistory.objects.filter(job_card=job_card).order_by('-timestamp')[:10]
    return render(request, 'jobcards/job_history_view.html', {
        'job_card': job_card,
        'history': history,
    })
