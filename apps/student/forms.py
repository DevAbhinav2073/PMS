from django import forms

from apps.student.models import ElectivePriority


class PriorityForm(forms.ModelForm):
    class Meta:
        model = ElectivePriority
        fields = ('subject', 'priority')
