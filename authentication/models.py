# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

from system.models import JobCard


class CustomUser(AbstractUser):
    SERVICE_CENTERS = [
        ('Middelburg SC', 'Middelburg SC'),
        ('Polokwane SC', 'Polokwane SC'),
        ('Cape Town SC', 'Cape Town SC'),
        ('Johannesburg SC', 'Johannesburg SC'),
        ('Bloemfontein SC', 'Bloemfontein SC'),
        ('Port Elizabeth SC', 'Port Elizabeth SC'),
        ('Durban SC', 'Durban SC'),
        ('MRE JHB', 'MRE JHB'),
    ]

    TECHNICAL_ADMIN = 'Technical Admin'
    FIELD_TECHNICIAN = 'Field Technician'

    ROLE_CHOICES = [
        (TECHNICAL_ADMIN, 'Technical Admin'),
        (FIELD_TECHNICIAN, 'Field Technician'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    cell_number = models.CharField(max_length=15, null=True, blank=True)  # Add the cell_number field here
    service_center = models.CharField(max_length=100, choices=SERVICE_CENTERS, null=True, blank=True)

    @property
    def assigned_jobs(self):
        return JobCard.objects.filter(assigned_technician=self.username).count()

    @property
    def completed_jobs(self):
        return JobCard.objects.filter(assigned_technician=self.username, job_status='Closed').count()

    @property
    def open_jobs(self):
        return JobCard.objects.filter(assigned_technician=self.username, job_status='Open').count(),

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
