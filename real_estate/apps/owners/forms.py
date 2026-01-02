from django import forms
from apps.owners.models import Owner


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ["name", "phone", "email", "address", "notes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "name": "Owner name",
            "phone": "Phone number",
            "email": "Email address",
            "address": "Full address",
            "notes": "Additional note",
        }

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": placeholders.get(name, "")}
            )
