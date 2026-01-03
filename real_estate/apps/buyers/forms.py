from django import forms
from apps.buyers.models import Buyer, CommunicationLog
from django.contrib.auth.models import User
from apps.property.models import Property


class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = [
            "name",
            "phone",
            "email",
            "address",
            "status",
            "source",
            "deal_probability",
            "budget_min",
            "budget_max",
            "preferred_location",
            "preferred_type",
            "assigned_to",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        placeholders = {
            "name": "Enter full name",
            "phone": "09… / +95…",
            "email": "example@email.com",
            "address": "Street, City",
            "budget_min": "Min budget",
            "budget_max": "Max budget",
            "preferred_location": "Yangon, Mandalay, etc.",
            "preferred_type": "Condo, Land, House…",
            "notes": "Additional notes",
            "deal_probability": "Deal Probability",
        }

        for name, field in self.fields.items():
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs.update({"class": "form-select"})
            else:
                field.widget.attrs.update({"class": "form-control"})

            if name in placeholders:
                field.widget.attrs["placeholder"] = placeholders[name]

        if user:
            qs = User.objects.filter(profile__company=user.profile.company)
            self.fields["assigned_to"].queryset = qs
            self.fields["assigned_to"].label_from_instance = (
                lambda obj: obj.first_name or obj.username
            )


class CommunicationLogForm(forms.ModelForm):
    class Meta:
        model = CommunicationLog
        fields = [
            "communication_type",
            "reminder_date",
            "reminder_time",
            "content",
        ]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Optional details"}
            ),
            "reminder_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "reminder_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "communication_type": "Select type",
            "content": "Optional details",
        }

        for name, field in self.fields.items():
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs.update({"class": "form-select"})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({"class": "form-control"})
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update({"class": "form-control"})
            else:
                field.widget.attrs.update({"class": "form-control"})

            if name in placeholders and not isinstance(
                field.widget, (forms.Select, forms.SelectMultiple)
            ):
                field.widget.attrs.update({"placeholder": placeholders[name]})
