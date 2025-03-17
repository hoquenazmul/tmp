from django import forms

class EnvSelectionForm(forms.Form):
    ENV_CHOICES = [
        ('qa', 'QA'),
        ('uat', 'UAT'),
    ]
    environment = forms.ChoiceField(choices=ENV_CHOICES)