from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from webapp.forms import CustomerForm, JobCardForm
from webapp.permissions import role_required

from django.contrib import messages


@login_required
@role_required('Technical Admin')
def create_job(request):
    if request.method == "POST":
        customer_form = CustomerForm(request.POST)
        job_form = JobCardForm(request.POST)

        try:
            if customer_form.is_valid() and job_form.is_valid():
                customer_instance = customer_form.save()  # Save the customer first

                # Assign the saved customer instance to the JobCard and then save it
                job_instance = job_form.save(commit=False)
                job_instance.customer = customer_instance
                job_instance.save()
                return redirect('success_page')  # Redirect to the success page
            else:
                # Handle form validation errors
                messages.error(request, 'There was an error in the form submission. Please check your input.')
        except Exception as e:
            # Handle other exceptions, such as database errors
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('dashboard')  # Redirect to the dashboard with the error message

    else:
        customer_form = CustomerForm()
        job_form = JobCardForm()

    context = {
        'customer_form': customer_form,
        'job_form': job_form,
    }

    return render(request, 'jobcards/create_job.html', context)
