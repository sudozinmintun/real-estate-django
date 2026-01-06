from django import forms
from django.forms import inlineformset_factory
from apps.paymentplans.models import PaymentPlan, PaymentPlanStep


class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.Select):
                widget.attrs.update({"class": "form-select"})
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({"class": "form-check-input"})
            else:
                widget.attrs.update({"class": "form-control"})


class PaymentPlanForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = PaymentPlan
        fields = ["name", "description"]


class PaymentPlanStepForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = PaymentPlanStep
        fields = [
            "step_type",
            "percentage",
            "months",
            "due_after_month",
        ]


PaymentPlanStepFormSet = inlineformset_factory(
    PaymentPlan,
    PaymentPlanStep,
    form=PaymentPlanStepForm,
    extra=1,
    can_delete=True,
)
