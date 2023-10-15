from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404

from system.models import JobCard
from webapp.forms import EditCustomerForm, EditJobCardForm, ImageFormSet
from webapp.models import JobCardHistory



def generate_change_description(old_instance, new_instance):
    old_dict = model_to_dict(old_instance)
    new_dict = model_to_dict(new_instance)
    changes = []
    detailed_changes = []
    for field, old_value in old_dict.items():
        new_value = new_dict.get(field)
        if old_value != new_value:
            changes.append(f"{field} updated to {new_value}")
            detailed_changes.append(f"{field} updated from {old_value} to {new_value}")
    summary = ', '.join(changes)
    details = ', '.join(detailed_changes)
    return summary, details



def log_job_card_change(job_card, user, summary, details=None):
    JobCardHistory.objects.create(
        job_card=job_card,
        changed_by=user,
        change_description=summary,
        change_details=details
    )



def edit_job_card(request, job_card_id):
    job_card = get_object_or_404(JobCard, id=job_card_id)
    customer = job_card.customer

    if request.method == 'POST':
        edit_customer_form = EditCustomerForm(request.POST, instance=customer)
        edit_job_card_form = EditJobCardForm(request.POST, instance=job_card)
        image_formset = ImageFormSet(request.POST, request.FILES, instance=job_card, prefix='images')

        if edit_customer_form.is_valid() and edit_job_card_form.is_valid() and image_formset.is_valid():
            old_instance = JobCard.objects.get(id=job_card_id)
            edit_customer_form.save()
            edit_job_card_form.save()
            image_formset.save()
            summary, details = generate_change_description(old_instance, job_card)
            log_job_card_change(job_card, request.user, summary, details)
            return redirect('update_success_page')

    else:
        edit_customer_form = EditCustomerForm(instance=customer)
        edit_job_card_form = EditJobCardForm(instance=job_card)
        image_formset = ImageFormSet(instance=job_card, prefix='images')

    history = JobCardHistory.objects.filter(job_card=job_card).order_by('-timestamp')[:10]

    return render(request, 'jobcards/edit_job_card.html', {
        'customer_form': edit_customer_form,
        'job_card_form': edit_job_card_form,
        'job_card': job_card,
        'image_formset': image_formset,
        'history': history,
    })


@login_required
def open_job_cards(request):
    open_cards = JobCard.objects.filter(job_status='Open')
    return render(request, 'jobcards/open_job_cards.html', {'open_cards': open_cards})
