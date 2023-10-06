from django import forms
from .models import Ticket
from django.contrib.auth.models import User


class TicketForm(forms.ModelForm):
    assigned_user = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Reception'),
        required=False,
        label='Assign to Reception User',
    )
    class Meta:
        model = Ticket
        fields = ('name', 'creator_name', 'priority', 'description', 'assigned_user')

