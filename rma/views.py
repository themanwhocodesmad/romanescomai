from django.utils import timezone
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import CustomUser
from .models import JobCard
from .models import RMA
from .serializers import RMASerializer
from .serializers import RMAToJobCardSerializer


class RMAQueryView(RetrieveAPIView):
    queryset = RMA.objects.all()
    serializer_class = RMASerializer
    lookup_field = 'rma_number'
    lookup_url_kwarg = 'rmaNumber'


class ConvertRMAToJobCardView(APIView):

    def post(self, request, rmaNumber, assignedTechnician):
        try:
            rma = RMA.objects.get(rma_number=rmaNumber)

            # Check if the RMA has already been converted or closed
            if rma.converted_or_closed:
                return Response({'error': 'RMA has already been converted or closed'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Convert the RMA to a JobCard
            job_card = rma.create_job_card()

            # Update technician or any other properties
            job_card.assigned_technician = assignedTechnician  # adjust the property name as per your JobCard model
            job_card.save()

            # Mark the RMA as converted
            rma.converted_or_closed = True
            rma.save()

            return Response({'message': 'Converted RMA to JobCard successfully'}, status=status.HTTP_201_CREATED)

        except RMA.DoesNotExist:
            return Response({'error': 'RMA not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': f'Error converting RMA: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RMAUpdateView(UpdateAPIView):
    queryset = RMA.objects.all()
    serializer_class = RMASerializer
    lookup_field = 'rma_number'
    lookup_url_kwarg = 'rmaNumber'

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Ensure we only update non-null fields from rmaUpdateDto
        data = {k: v for k, v in request.data.items() if v is not None}

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RMACreateView(generics.CreateAPIView):
    queryset = RMA.objects.all()
    serializer_class = RMASerializer

    def perform_create(self, serializer):
        serializer.save(
            # created_by=self.request.user.username,
            # created_at=timezone.now()
        )


class RMAListView(generics.ListCreateAPIView):
    serializer_class = RMASerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated before accessing

    def get_queryset(self):
        user = self.request.user

        # If the user is a HUB_CONTROLLER, filter RMAs accordingly
        if user.role == CustomUser.HUB_CONTROLLER:
            return RMA.objects.filter(converted_or_closed=False, recieved_at_warehouse=False)
        else:
            return RMA.objects.filter(converted_or_closed=False)


class RMADetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RMA.objects.all()
    serializer_class = RMASerializer


class RMAToJobCardView(generics.CreateAPIView):
    queryset = JobCard.objects.all()
    serializer_class = RMAToJobCardSerializer

    def create(self, request, *args, **kwargs):
        assigned_technician = self.kwargs.get('technician_name')
        rma_id = self.kwargs.get('pk')
        if not assigned_technician or not rma_id:
            return Response({"detail": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)
        rma = RMA.objects.get(pk=rma_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                rma=rma,
                assigned_technician=assigned_technician,
                assigned_date=timezone.now(),
                last_modified_by=request.user.username,
                last_modified_at=timezone.now(),
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
