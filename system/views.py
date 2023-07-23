import io
from datetime import date
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.urls import reverse

import pandas as pd
from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import FileResponse
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from django.views import View
from rest_framework import status, generics

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from xhtml2pdf import pisa

from authentication.models import CustomUser
from .models import Image
from .models import JobCard
from .serializers import ImageSerializer, JobCardSerializerForJobCreation
from .serializers import JobCardSerializer
from .twilio_whatsapp.technician_notifications import send_whatsapp_message


# noinspection PyMethodMayBeStatic
class DashboardDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {}
        if user.role == CustomUser.TECHNICAL_ADMIN:
            data = self._get_technical_admin_data()
        elif user.role == CustomUser.FIELD_TECHNICIAN:
            data = self._get_field_technician_data(user)
        return Response(data)

    def _get_technical_admin_data(self):
        jobs = JobCard.objects.all()

        data = {
            'overall': self._get_job_statistics(jobs),
            'monthly': self._get_monthly_statistics(jobs),
            'fault_breakdown': list(
                jobs.values('product_name', 'fault_code').annotate(total=Count('id')).order_by('-total')),
            'top_repaired_products': list(
                jobs.filter(job_status='Closed').values('product_name').annotate(total=Count('id')).order_by('-total')[:5]),
            'sla_breakdown_per_technician': self._get_sla_breakdown_per_technician(jobs),
        }
        return data

    def _get_field_technician_data(self, user):
        jobs = JobCard.objects.filter(assigned_technician=user.username)

        data = {
            'overall': self._get_job_statistics(jobs),
            'monthly': self._get_monthly_statistics(jobs),
        }
        return data

    def _get_job_statistics(self, jobs):
        return {
            'total_jobs': jobs.count(),
            'closed_jobs': jobs.filter(job_status='Closed').count(),
            'open_jobs': jobs.filter(job_status='Open').count(),
            'out_of_sla_jobs': self._get_out_of_sla_jobs(jobs),
        }

    def _get_monthly_statistics(self, jobs):
        monthly_data = jobs.annotate(
            year=ExtractYear('date_created'),
            month=ExtractMonth('date_created')
        ).values('year', 'month').annotate(
            total_jobs=Count('id'),
            closed_jobs=Count('id', filter=Q(job_status='Closed')),
            open_jobs=Count('id', filter=Q(job_status='Open')),
        ).order_by('year', 'month')

        for month in monthly_data:
            month['out_of_sla_jobs'] = self._get_out_of_sla_jobs(
                jobs.filter(date_created__year=month['year'], date_created__month=month['month']))

        return list(monthly_data)

    def _get_sla_breakdown_per_technician(self, jobs):
        sla_breakdown = []
        technicians = jobs.values_list('assigned_technician', flat=True).distinct()

        for tech in technicians:
            tech_jobs = jobs.filter(assigned_technician=tech)
            sla_breakdown.append({
                'technician': tech,
                'total_jobs': tech_jobs.count(),
                'out_of_sla_jobs': self._get_out_of_sla_jobs(tech_jobs),
            })

        return sla_breakdown

    def _get_out_of_sla_jobs(self, jobs):
        out_of_sla_jobs = 0

        for job in jobs:
            if job.sla_status == 'Out-of-SLA':
                out_of_sla_jobs += 1

        return out_of_sla_jobs


# noinspection PyMethodMayBeStatic
class CreateNewJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()  # Copy the request data

        job_card_serializer = JobCardSerializerForJobCreation(data=data)
        if job_card_serializer.is_valid(raise_exception=True):
            job_card = job_card_serializer.save()
            job_card.assigned_date = timezone.now()
            job_card.save()

            # Here we assume that your CustomUser's username field is used for storing technicians' names
            assigned_technician = CustomUser.objects.get(username=job_card.assigned_technician)
            if assigned_technician.cell_number:  # Make sure technician has a contact number
                # Now you can send the WhatsApp message
                send_whatsapp_message(assigned_technician.first_name, job_card.job_number,
                                      assigned_technician.cell_number)

            return Response({
                'job_number': job_card.job_number  # Return job number
            }, status=status.HTTP_201_CREATED)


# noinspection PyMethodMayBeStatic
class JobQueryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, queryType, inputQuery):
        # Define the queryset based on the query type
        if queryType == "job_number":
            job = JobCard.objects.get(job_number=inputQuery)
        elif queryType == "name":
            job = JobCard.objects.get(customer__name=inputQuery)
        elif queryType == "contact_number":
            job = JobCard.objects.get(customer__contact_number=inputQuery)
        else:
            return Response({"detail": "Invalid query type."}, status=400)

        # Serialize and return the job data
        serializer = JobCardSerializer(job)
        return Response(serializer.data)


# noinspection PyMethodMayBeStatic
class CloseJobView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, job_number):
        try:
            job = JobCard.objects.get(job_number=job_number)
            job.job_status = 'Closed'
            job.closed_by = request.user.username
            job.closed_at = timezone.now()
            job.save()

            try:
                # Send the survey link via email after successfully closing a job.
                survey_link = request.build_absolute_uri(
                    reverse('customer-satisfaction', kwargs={'job_number': job.job_number}))
                email_body = f"""
                <p>Dear {job.customer.name},</p>

                <p>Thank you for using our services. We would appreciate it if you could take a few minutes to fill out our satisfaction survey.</p>

                <p><a href="{survey_link}">Click here to start the survey</a></p>

                <p>Best regards,</p>
                <p>Magneto Renewable Energy</p>
                
                <img src="www.google.com/imgres?imgurl=https%3A%2F%2Fwww.magnetoenergy.co.za%2Fog-image.png&tbnid=LDm536f5KAcbGM&vet=12ahUKEwiZ1dKw16WAAxVNnCcCHRTLC98QMygAegUIARDPAQ..i&imgrefurl=https%3A%2F%2Fmagnetoenergy.co.za%2F&docid=WoHAGTOZOwGTAM&w=1200&h=630&q=magneto%20renewable%20energy%20logo&ved=2ahUKEwiZ1dKw16WAAxVNnCcCHRTLC98QMygAegUIARDPAQ" alt="Logo"> 
                """

                email = EmailMessage(
                    'Your Feedback Matters',
                    email_body,
                    to=[job.customer.email]  # assuming the customer has an 'email' field
                )
                email.content_subtype = 'html'  # Make the content HTML
                email.send()
            except Exception as e:
                print(
                    f"Failed to send email: {e}")  # You might want to handle this differently depending on your requirements

            return Response(status=status.HTTP_204_NO_CONTENT)
        except JobCard.DoesNotExist:
            return Response({"detail": "Job not found."}, status=status.HTTP_404_NOT_FOUND)


# noinspection PyMethodMayBeStatic
class FetchJobView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_number):
        try:
            job = JobCard.objects.get(job_number=job_number)
            serializer = JobCardSerializer(job)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except JobCard.DoesNotExist:
            return Response({"detail": "Job not found."}, status=status.HTTP_404_NOT_FOUND)


# noinspection PyMethodMayBeStatic
class UpdateJobView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, job_number):
        try:
            job = JobCard.objects.get(job_number=job_number)
            request.data['last_modified_by'] = request.user.pk
            request.data['last_modified_at'] = timezone.now()
            job.completed_date = timezone.now()
            job.save()
            serializer = JobCardSerializer(job, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except JobCard.DoesNotExist:
            return Response({"detail": "Job not found."}, status=status.HTTP_404_NOT_FOUND)


def DatabaseDownloadView(request):
    # permission_classes = [IsAuthenticated]

    job_cards = JobCard.objects.all()

    basic_headers = ['Job Number', 'Status', 'Priority', 'Job Type']
    customer_details = ['Customer Name', 'Customer Email', 'Customer Contact Number',
                        'Customer Alt Contact Number', 'Customer Address']
    job_details = ['Complaint or Query', 'Error Code', 'Date Created', 'Date of Query',
                   'Date of Purchase', 'Region', 'Vendor Name', 'Product Name', 'Serial Number',
                   'Fault Code', 'Repair Type', 'Assigned Technician', 'Assigned Time', 'Completed Time']
    technician_details = ['Date of Technician Assessment', 'Technician Assessment',
                          'Technician Notes', 'Additional Notes', 'Resolution', 'Last Modified By',
                          'Last Modified At', 'Created By', 'Created At', 'Closed By', 'Closed At']
    feedback_details = ['Service Location', 'Follow Up Required', 'Customer Satisfaction', 'Customer Comment']

    headers = basic_headers + customer_details + job_details + technician_details + feedback_details

    data = []

    for job_card in job_cards:
        customer = job_card.customer
        customer_data = [customer.name, customer.email, customer.contact_number, customer.alt_contact_number,
                         customer.address]
        job_data = [
            job_card.complaint_or_query, job_card.error_code,
            job_card.date_created.strftime('%Y-%m-%d %H:%M:%S') if job_card.date_created else 'Not yet provided',
            job_card.date_of_query.strftime('%Y-%m-%d') if job_card.date_of_query else 'Not yet provided',
            job_card.date_of_purchase.strftime('%Y-%m-%d') if job_card.date_of_purchase else 'Not yet provided',
            job_card.region, job_card.vendor_name, job_card.product_name, job_card.serial_number,
            job_card.fault_code, job_card.repair_type, job_card.assigned_technician,
            job_card.assigned_time.strftime('%Y-%m-%d %H:%M:%S') if job_card.assigned_time else 'Not yet provided',
            job_card.completed_time.strftime('%Y-%m-%d %H:%M:%S') if job_card.completed_time else 'Not yet provided'
        ]
        technician_data = [
            job_card.date_of_technician_assessment.strftime(
                '%Y-%m-%d') if job_card.date_of_technician_assessment else 'Not yet provided',
            job_card.technician_assessment, job_card.technician_notes, job_card.additional_notes,
            job_card.resolution, job_card.last_modified_by, job_card.last_modified_at.strftime('%Y-%m-%d %H:%M:%S'),
            job_card.created_by, job_card.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            job_card.closed_by,
            job_card.closed_at.strftime('%Y-%m-%d %H:%M:%S') if job_card.closed_at else 'Not yet provided',
        ]
        feedback_data = [job_card.service_location, job_card.follow_up_required, job_card.customer_satisfaction,
                         job_card.customer_comment]

        row_data = [job_card.job_number, job_card.job_status, job_card.priority, job_card.job_type]
        row_data.extend(customer_data)
        row_data.extend(job_data)
        row_data.extend(technician_data)
        row_data.extend(feedback_data)

        data.append(row_data)

    # Create a pandas DataFrame from the list of data
    df = pd.DataFrame(data, columns=headers)

    # Fill any empty cells with "Not yet provided."
    df.fillna("Not yet provided.", inplace=True)

    # Write DataFrame to an Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Job Cards', index=False)

    # Get the value of the BytesIO buffer and write it to the response
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Generate the current date string
    current_date = date.today().strftime('%d_%m_%Y')

    # Append the current date to the output filename
    output_filename = f'MRE_Database_{current_date}.xlsx'
    response['Content-Disposition'] = f'attachment; filename={output_filename}'

    return response


# noinspection PyMethodMayBeStatic
class DownloadJobCardView(View):
    def get(self, request, *args, **kwargs):
        job_number = kwargs.get('job_number')
        job_card = get_object_or_404(JobCard, job_number=job_number)

        template = get_template('job_card_pdf.html')
        context = {
            'job_card': job_card,
        }
        html = template.render(context)
        result = BytesIO()

        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return FileResponse(BytesIO(result.getvalue()), content_type='application/pdf',
                                as_attachment=True, filename=f'{job_number}.pdf')
        else:
            return None


# noinspection PyMethodMayBeStatic
class UploadImagesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_number):
        try:
            job = JobCard.objects.get(job_number=job_number)

            if 'image' not in request.FILES:
                return Response({"detail": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

            if 'description' not in request.data:
                return Response({"detail": "No description provided."}, status=status.HTTP_400_BAD_REQUEST)

            image_file = request.FILES['image']
            description = request.data['description']

            if description.strip() == '':
                raise ValidationError({"detail": "Description can't be empty."})

            image = Image.objects.create(job_card=job, image=image_file, description=description)

            return Response(ImageSerializer(image).data, status=status.HTTP_201_CREATED)
        except JobCard.DoesNotExist:
            return Response({"detail": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)


class UserAssignedJobsList(generics.ListAPIView):
    serializer_class = JobCardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == CustomUser.TECHNICAL_ADMIN:
            return JobCard.objects.filter(job_status="Open")
        else:
            return JobCard.objects.filter(assigned_technician=user, job_status="Open")
