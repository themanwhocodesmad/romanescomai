from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone  # Importing timezone to set the current date and time

from system.models import JobCard
from webapp.forms import CloseJobCardForm


def close_job_card(request, job_card_id):
    job_card = get_object_or_404(JobCard, id=job_card_id)

    if request.method == 'POST':
        form = CloseJobCardForm(request.POST, instance=job_card)

        if form.is_valid():
            closed_card = form.save(commit=False)
            closed_card.job_status = 'Closed'
            closed_card.closed_by = request.user.username  # Setting the logged-in user as the person who closed the card
            closed_card.closed_at = timezone.now()  # Setting the current date and time
            closed_card.save()
            return redirect('success_page')  # Redirect to a success screen. Remember to define this view and URL.
    else:
        form = CloseJobCardForm(instance=job_card)

    return render(request, 'close_job_card.html', {
        'form': form,
        'job_card': job_card
    })
