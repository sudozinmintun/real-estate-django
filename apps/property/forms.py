from django import forms
from apps.property.models import Property
from apps.order.models import Order


class PropertyAdminForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("user")

        if not user:
            return cleaned_data

        # Count properties created by this user
        current_property_count = Property.objects.filter(user=user).count()

        # Get user's active allowed max from Orders
        max_allowed = Order.total_max_properties(user)

        if current_property_count >= max_allowed:
            raise forms.ValidationError(
                f"User '{user.username}' can only post {max_allowed} properties. "
                f"They already posted {current_property_count}."
            )

        return cleaned_data
