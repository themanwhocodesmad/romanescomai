from django.shortcuts import render, redirect
from webapp.forms import CustomerForm, JobCardForm


def create_job(request):
    if request.method == "POST":
        customer_form = CustomerForm(request.POST)
        job_form = JobCardForm(request.POST)

        if customer_form.is_valid() and job_form.is_valid():
            customer_instance = customer_form.save()  # Save the customer first

            # Assign the saved customer instance to the JobCard and then save it
            job_instance = job_form.save(commit=False)
            job_instance.customer = customer_instance
            job_instance.save()

            return redirect('success_page')  # Redirect to success page  # Redirect to dashboard or some other page after successful creation
    else:
        customer_form = CustomerForm()
        job_form = JobCardForm()

    context = {
        'customer_form': customer_form,
        'job_form': job_form,
    }

    return render(request, 'jobcards/create_job.html', context)
