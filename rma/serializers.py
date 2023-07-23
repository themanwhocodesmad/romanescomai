from rest_framework import serializers

from system.models import JobCard
from .models import RMA


class RMASerializer(serializers.ModelSerializer):
    class Meta:
        model = RMA
        fields = '__all__'


class RMAToJobCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCard
        fields = [
            'rma',
            'assigned_technician',
            'assigned_date',
            'last_modified_by',
            'last_modified_at',
            # Include all the fields from the JobCard that we are using
        ]
        read_only_fields = ['rma']

    def create(self, validated_data):
        job_card = JobCard.objects.create(**validated_data)
        return job_card
