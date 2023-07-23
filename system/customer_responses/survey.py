from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from system.customer_responses.forms import CustomerSatisfactionForm
from system.models import JobCard
from django.views.generic.base import TemplateView


class SurveySuccessView(TemplateView):
    template_name = 'survey_success.html'

from django.http import HttpResponseRedirect

class CustomerSatisfactionFormView(FormView):
    template_name = 'customer_survey.html'  # replace with your template name
    form_class = CustomerSatisfactionForm
    success_url = reverse_lazy('survey-success')  # replace with your success page

    def get(self, request, *args, **kwargs):
        job_card = get_object_or_404(JobCard, job_number=kwargs['job_number'])
        if job_card.survey_completed:
            return HttpResponseRedirect(self.success_url)  # If the survey is completed, redirect to success page
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        job_card = get_object_or_404(JobCard, job_number=self.kwargs['job_number'])
        initial['job_number'] = job_card.job_number
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_card = get_object_or_404(JobCard, job_number=self.kwargs['job_number'])
        context['job_card'] = job_card
        return context

    def form_valid(self, form):
        job_card = get_object_or_404(JobCard, job_number=form.cleaned_data['job_number'])
        if job_card.survey_completed:
            return self.form_invalid(form)  # The survey has already been completed, so return form_invalid
        job_card.customer_satisfaction = form.cleaned_data['service_rating']
        job_card.customer_comment = form.cleaned_data['comments']
        job_card.survey_completed = True
        job_card.save()
        return super().form_valid(form)
