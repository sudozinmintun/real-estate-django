from django import forms
from apps.lawyers.models import Lawyer


class LawyerForm(forms.ModelForm):
    class Meta:
        model = Lawyer
        fields = ["name", "phone", "email", "address", "license_number", "bio", "notes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "name": "Owner name",
            "phone": "Phone number",
            "email": "Email address",
            "address": "Full address",
            "license_number": "License number",
            "bio": "Bio",
            "notes": "Additional note",
        }

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": placeholders.get(name, "")}
            )
