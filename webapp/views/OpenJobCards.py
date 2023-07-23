from django.shortcuts import render
from system.models import JobCard

from django.shortcuts import render, redirect, get_object_or_404

from webapp.forms import EditCustomerForm, EditJobCardForm


def edit_job_card(request, job_card_id):
    job_card = get_object_or_404(JobCard, id=job_card_id)
    customer = job_card.customer

    if request.method == 'POST':
        edit_customer_form = EditCustomerForm(request.POST, instance=customer)
        edit_job_card_form = EditJobCardForm(request.POST, instance=job_card)

        if edit_customer_form.is_valid() and edit_job_card_form.is_valid():
            edit_customer_form.save()
            edit_job_card_form.save()
            return redirect('success_page')  # Redirect to a success screen. Remember to define this view and URL.
    else:
        edit_customer_form = EditCustomerForm(instance=customer)
        edit_job_card_form = EditJobCardForm(
            initial={
                'region': job_card.region,
                'product_name': job_card.product_name,
                'assigned_technician': job_card.assigned_technician,
                'error_code': job_card.error_code,
                'vendor_name': job_card.vendor_name,
            },
            instance=job_card
        )

    return render(request, 'edit_job_card.html', {
        'customer_form': edit_customer_form,
        'job_card_form': edit_job_card_form,
        'job_card': job_card
    })


def open_job_cards(request):
    open_cards = JobCard.objects.filter(job_status='Open')
    return render(request, 'open_job_cards.html', {'open_cards': open_cards})
