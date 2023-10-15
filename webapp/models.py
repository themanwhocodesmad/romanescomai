# models.py
from django.db import models

from authentication.models import CustomUser
from system.models import JobCard


class PDFRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']  # To ensure the latest records come first


class JobCardHistory(models.Model):
    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE, related_name='history')
    change_details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    change_description = models.TextField()

    class Meta:
        ordering = ['-timestamp']  # To ensure the most recent changes are shown first

    def __str__(self):
        return f"{self.job_card.job_number} - {self.timestamp}"


class KnowledgeBase(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
