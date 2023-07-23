from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rma.models import RMA
from system.models import JobCard


@login_required
def dashboard(request):
    user = request.user

    # Get all Open jobs
    open_jobs = JobCard.objects.filter(job_status='Open')

    # Calculate the number of out-of-SLA jobs
    out_of_sla_jobs = sum(1 for job in open_jobs if job.sla_status == 'Out-of-SLA')

    total_jobs = JobCard.objects.all().count()
    closed_jobs = JobCard.objects.filter(job_status='Closed').count()

    total_rmas = RMA.objects.all().count()
    closed_rmas = RMA.objects.filter(converted_or_closed=True).count()
    in_transit_rmas = RMA.objects.filter(received_at_warehouse=False).count()

    context = {
        'user': user,
        'total_jobs': total_jobs,
        'closed_jobs': closed_jobs,
        'open_jobs': open_jobs.count(),
        'out_of_sla_jobs': out_of_sla_jobs,
        'total_rmas': total_rmas,
        'closed_rmas': closed_rmas,
        'in_transit_rmas': in_transit_rmas
    }

    return render(request, 'dashboard.html', context)
