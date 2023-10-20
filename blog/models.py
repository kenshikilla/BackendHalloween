from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

PRIORITY_CHOICES = (
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
)

STATUS_CHOICES = (
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('resolved', 'Resolved'),
    ('confirmed', 'Confirmed'),
)

class Ticket(models.Model):
    name = models.CharField(max_length=255)
    creator_name = models.CharField(max_length=255, default='idontknow')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    actions_taken = models.TextField(blank=True)
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tickets')
    resolved_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resolved_tickets')
    confirmed = models.BooleanField(default=False)
