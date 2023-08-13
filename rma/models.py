from django.db import models
from django.db.models import Max

from system.models import JobCard, Customer


# models.py

class RMA(models.Model):
    GOOD_CONDITIONS = [
        ('Good', 'Good'),
        ('Average', 'Average'),
        ('Poor', 'Poor')
    ]
    PACKAGE_CONDITIONS = [
        ('Intact', 'Intact'),
        ('Damaged', 'Damaged'),
        ('Sealed', 'Sealed'),
        ('No Packaging', 'No Packaging')
    ]
    SERVICE_CENTRES = [
        ('MRE Service Centre', 'MRE Service Centre'),
        ('Johannesburg Centre', 'Johannesburg Centre'),
        ('Durban Service Centre', 'Durban Service Centre'),
        ('Bloemfontein Service Centre', 'Bloemfontein Service Centre'),
        ('Cape Town Service Centre', 'Cape Town Service Centre'),
        ('Middelburg Service Centre', 'Middelburg Service Centre'),
        ('Polokwane Service Centre', 'Polokwane Service Centre')
    ]
    ACTIONS = [
        ('Repair', 'Repair'),
        ('Replace', 'Replace'),
        ('Refund', 'Refund'),
    ]

    rma_number = models.CharField(max_length=200, null=True, blank=True)
    service_centre = models.CharField(max_length=200, choices=SERVICE_CENTRES, null=True, blank=True)
    date_returned = models.DateField(null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    contact_person = models.CharField(max_length=200, null=True, blank=True)
    contact_number = models.CharField(max_length=200, null=True, blank=True)
    email_address = models.EmailField(null=True, blank=True)
    inv_no = models.CharField(max_length=200, null=True, blank=True)
    inv_date = models.DateField(null=True, blank=True)
    item_code = models.CharField(max_length=200, null=True, blank=True)
    serial_no = models.OneToOneField(JobCard, max_length=200, null=True, blank=True, on_delete=models.CASCADE)
    package_condition = models.CharField(max_length=200, choices=PACKAGE_CONDITIONS, null=True, blank=True)
    goods_condition = models.CharField(max_length=200, choices=GOOD_CONDITIONS, null=True, blank=True)

    ACTION_CHOICES = [
        ('Repair', 'Repair'),
        ('Replace', 'Replace'),
        ('Refund', 'Refund'),
    ]
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    customer_name = models.CharField(max_length=200, null=True, blank=True)
    customer_signature = models.ImageField(null=True, blank=True)
    received_at_warehouse = models.BooleanField(default=False, blank=True)
    converted_or_closed = models.BooleanField(default=False, blank=True)

    def generate_rma_number(self):
        # Get the last used RMA number or start from 0
        last_rma = RMA.objects.all().aggregate(Max('rma_number'))['rma_number__max'] or "RMA0000"
        # Strip off the "RMA" prefix, convert the remainder to int, add 1 and format again
        new_rma_num = int(last_rma[3:]) + 1
        # Return as RMA formatted string
        return f"RMA{new_rma_num:04}"

    def save(self, *args, **kwargs):
        # If no RMA number set, generate it
        if not self.rma_number:
            self.rma_number = self.generate_rma_number()
        super(RMA, self).save(*args, **kwargs)

    def __str__(self):
        return self.rma_number

    def create_job_card(self):
        customer, created = Customer.objects.get_or_create(
            name=self.customer_name,
            email=self.email_address,
            contact_number=self.contact_number,
        )

        job_card = JobCard.objects.create(
            customer=customer,
            complaint_or_query=self.reason,
            serial_number=self.serial_no,  # this should be a serial number string, not a reference to a JobCard
            product_name=self.item_code,
            vendor_name=self.company_name,
            job_type=self.action,
            job_status='Open',  # Default to 'Open' status
            priority='Medium',  # Default to 'Medium' priority
            date_of_query=self.date_returned,  # Assuming date_returned is the date of the query
            date_of_purchase=self.inv_date,  # Assuming inv_date is the date of purchase
            repair_type=self.action,  # Assuming action is the repair type
            service_location=self.service_centre,  # Assuming service_centre is the service location
        )

        return job_card
