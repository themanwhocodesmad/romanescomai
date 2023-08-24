from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone


class Customer(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    alt_contact_number = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class JobCounter(models.Model):
    counter = models.IntegerField(default=0)

    @classmethod
    def increment(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        obj.counter += 1
        obj.save()
        return obj.counter


class job_numberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 7)
        super().__init__(*args, **kwargs)

    def generate_job_number(self):
        prefix = 'MRE'
        count = JobCounter.increment()  # This will increment the counter each time a job number is generated
        suffix = f"{count:04d}"  # Format the count as a 4-digit number
        return f"{prefix}{suffix}"


class JobCard(models.Model):
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('In Progress', 'In Progress')
    )

    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    )

    JOB_TYPE_CHOICES = (
        ('Field Repair', 'Field Repair'),
        ('Service Centre Repair', 'Service Centre Repair'),
        ('Installation', 'Installation')
    )

    # JOB_TYPE_CHOICES = (
    #     ('Maintenance', 'Maintenance'),
    #     ('Repair', 'Repair'),
    #     ('Installation', 'Installation')
    # )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    complaint_or_query = models.CharField(max_length=100,blank=True, null=True)
    error_code = models.CharField(max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_of_query = models.DateField(blank=True, null=True)
    date_of_purchase = models.DateField(blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    vendor_name = models.CharField(max_length=50, blank=True, null=True)
    product_name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, blank=True, null=True)
    date_of_technician_assessment = models.DateField(blank=True, null=True)
    technician_assessment = models.CharField(max_length=100,blank=True, null=True)
    technician_notes = models.CharField(max_length=500,blank=True, null=True)
    additional_notes = models.CharField(max_length=500,blank=True, null=True)
    fault_code = models.CharField(max_length=5, blank=True, null=True)
    repair_type = models.CharField(max_length=50, blank=True, null=True)
    assigned_technician = models.CharField(max_length=50, blank=True, null=True)
    job_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Open")
    resolution = models.CharField(max_length=500, blank=True, null=True)
    last_modified_by = models.CharField(max_length=50, blank=True, null=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    closed_by = models.CharField(max_length=50, blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    job_number = job_numberField(unique=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="Medium")
    job_type = models.CharField(max_length=15, choices=JOB_TYPE_CHOICES, default="Repair")
    service_location = models.CharField(max_length=50, blank=True, null=True)
    follow_up_required = models.BooleanField(default=False)

    survey_completed = models.BooleanField(default=False)
    customer_satisfaction = models.IntegerField(blank=True,
                                                null=True)  # Could be a scale of 1-10 or any other method of rating.
    customer_comment = models.CharField(max_length=50, blank=True, null=True)

    assigned_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    pdf_file_1 = models.FileField(upload_to='pdfs/', null=True, blank=True)
    pdf_file_2 = models.FileField(upload_to='pdfs/', null=True, blank=True)

    @property
    def time_to_complete(self):
        if self.assigned_time and self.completed_time:
            return self.completed_time - self.assigned_time
        else:
            return None

    @property
    def sla_status(self):
        # SLA in days
        sla_days = 7
        sla_duration = timedelta(days=sla_days)
        if timezone.now() > self.date_created + sla_duration and self.job_status != 'Closed':
            return 'Out-of-SLA'
        else:
            return 'With-In-SLA'

    def __str__(self):
        return f"{self.customer.name} - {self.job_number}"


def job_card_directory(instance, filename):
    date_string = datetime.now().strftime('%Y-%m-%d')
    return f'job_cards/{instance.job_card.job_number}/{date_string}/{filename}'


class Image(models.Model):
    description = models.TextField(blank=True, null=True)
    job_card = models.ForeignKey(JobCard, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=job_card_directory, blank=True, null=True)

    def __str__(self):
        return f"{self.job_card.job_number} - {self.job_card.customer.name} | {self.description}"
