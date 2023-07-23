from django.db.models.signals import pre_save
from django.dispatch import receiver

from system.models import JobCard, job_numberField


@receiver(pre_save, sender=JobCard)
def add_job_number(sender, instance, **kwargs):
    if not instance.job_number:  # only if job_number doesn't already exist
        job_number_field = job_numberField()  # instantiate the job_numberField
        instance.job_number = job_number_field.generate_job_number()
