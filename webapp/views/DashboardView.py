from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rma.models import RMA
from webapp.models import JobCard, CustomUser
from datetime import timedelta
from django.utils import timezone


@login_required
def dashboard(request):
    user = request.user
    context = {}

    sla_duration = timedelta(days=7)

    if user.role == CustomUser.FIELD_TECHNICIAN:
        open_jobs = JobCard.objects.filter(job_status='Open', assigned_technician=user.username)
        closed_jobs = JobCard.objects.filter(job_status='Closed', assigned_technician=user.username)
        out_of_sla_jobs = JobCard.objects.filter(
            job_status='Open',
            assigned_technician=user.username,
            date_created__lte=timezone.now() - sla_duration
        )
    else:
        open_jobs = JobCard.objects.filter(job_status='Open')
        closed_jobs = JobCard.objects.filter(job_status='Closed')
        out_of_sla_jobs = JobCard.objects.filter(
            job_status='Open',
            date_created__lte=timezone.now() - sla_duration
        )

    total_rmas = RMA.objects.all().count()
    closed_rmas = RMA.objects.filter(converted_or_closed=True).count()
    in_transit_rmas = RMA.objects.filter(received_at_warehouse=False).count()

    # Extracting the job numbers
    open_job_numbers = [job.job_number for job in open_jobs]

    # Convert job numbers to IDs
    open_job_ids = [int(job.job_number[-4:]) - 0 for job in open_jobs]
    out_of_sla_job_ids = [int(job.job_number[-4:]) - 0 for job in out_of_sla_jobs]

    context.update({
        'user': user,
        'total_jobs': open_jobs.count() + closed_jobs.count(),
        'closed_jobs': closed_jobs.count(),
        'open_jobs': open_jobs.count(),
        'out_of_sla_jobs': out_of_sla_jobs.count(),
        'total_rmas': total_rmas,
        'closed_rmas': closed_rmas,
        'in_transit_rmas': in_transit_rmas,
        'open_job_numbers': open_job_numbers,  # Adding the list of open job numbers to the context
        'open_job_ids': open_job_ids,
        'out_of_sla_job_ids': out_of_sla_job_ids,
    })

    return render(request, 'dashboard.html', context)

