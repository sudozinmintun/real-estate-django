from django import forms
from apps.property.models import Property
from apps.order.models import Order
from apps.amenities.models import Amenity
from apps.city.models import City, Township


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


PROPERTY_STATUS_CHOICES = [
    ("", "Select Status"),
    ("fully_furnished", "Fully Furnished"),
    ("semi_furnished", "Semi Furnished"),
    ("unfurnished", "Unfurnished"),
    ("under_renovation", "Under Renovation"),
    ("newly_built", "Newly Built"),
    ("move_in_ready", "Move-in Ready"),
    ("pre_owned", "Pre-Owned"),
]

ADVERTISER_CHOICES = {
    ("Agent", "Agent"),
    ("Owner", "Owner"),
}


class PropertyForm(forms.ModelForm):

    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        required=False,
    )

    property_status = forms.ChoiceField(
        choices=PROPERTY_STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "select_2"}),
        required=False,
    )

    advertiser = forms.ChoiceField(
        choices=ADVERTISER_CHOICES,
        widget=forms.Select(attrs={"class": "select_2"}),
        required=False,
    )

    class Meta:
        model = Property
        fields = [
            "title",
            "property_type",
            "area",
            "area_unit",
            "country",
            "city",
            "township",
            "purpose",
            "price",
            "currency",
            "property_status",
            "video_link",
            "description",
            "floor",
            "bedroom",
            "bathroom",
            "advertiser",
            "amenities",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Property Title"}),
            "property_type": forms.Select(attrs={"class": "select_2"}),
            "area": forms.TextInput(attrs={"placeholder": "Size"}),
            "area_unit": forms.Select(attrs={"class": "select_2"}),
            "country": forms.Select(attrs={"class": "select_2"}),
            "city": forms.Select(attrs={"class": "select_2"}),
            "township": forms.Select(attrs={"class": "select_2"}),
            "purpose": forms.Select(attrs={"class": "select_2"}),
            "price": forms.NumberInput(attrs={"placeholder": "Price"}),
            "currency": forms.Select(attrs={"class": "select_2"}),
            "floor": forms.TextInput(
                attrs={"placeholder": "e.g. Ground, 1st Floor, Penthouse"}
            ),
            "bedroom": forms.TextInput(attrs={"placeholder": "e.g. 1, 2, Studio"}),
            "bathroom": forms.TextInput(attrs={"placeholder": "e.g. 1, 2, 1.5"}),
            "video_link": forms.TextInput(
                attrs={"placeholder": "YouTube or Video URL"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control summer_note", "rows": 4}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initially empty querysets
        # self.fields["city"].queryset = City.objects.none()
        # self.fields["township"].queryset = Township.objects.none()

        # If POST data exists, filter querysets accordingly
        if "country" in self.data:
            try:
                country_id = int(self.data.get("country"))
                self.fields["city"].queryset = City.objects.filter(
                    country_id=country_id
                )
            except (ValueError, TypeError):
                pass

        if "city" in self.data:
            try:
                city_id = int(self.data.get("city"))
                self.fields["township"].queryset = Township.objects.filter(
                    city_id=city_id
                )
            except (ValueError, TypeError):
                pass

    def clean(self):
        cleaned_data = super().clean()

        required_fields = {
            "title": "Please enter a title.",
            "property_type": "Please select a property type.",
            "country": "Please select a country.",
            "city": "Please select a city.",
            "price": "Please enter a valid price.",
            "currency": "Please select a currency.",
        }

        for field, message in required_fields.items():
            if not cleaned_data.get(field):
                self.add_error(field, message)

        price = cleaned_data.get("price")
        if price is not None and price <= 0:
            self.add_error("price", "Price must be greater than zero.")

        return cleaned_data
