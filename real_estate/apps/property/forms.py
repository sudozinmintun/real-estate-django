from django import forms
from apps.property.models import Property
from apps.order.models import Order
from apps.amenities.models import Amenity
from apps.city.models import City, Township
from apps.owners.models import Owner


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
    ("Fully Furnished", "Fully Furnished"),
    ("Semi Furnished", "Semi Furnished"),
    ("Unfurnished", "Unfurnished"),
    ("Under Renovation", "Under Renovation"),
    ("Newly Built", "Newly Built"),
    ("Move-in Ready", "Move-in Ready"),
    ("Pre-Owned", "Pre-Owned"),
]

PRICE_FREQUENCY_CHOICES = (
    ("", "--Select--"),
    ("monthly", "Per month"),
    ("yearly", "Per year"),
)


class OwnerChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.phone:
            return f"{obj.name} ({obj.phone})"
        return obj.name


class PropertyForm(forms.ModelForm):

    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        required=False,
    )

    property_status = forms.ChoiceField(
        choices=PROPERTY_STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-control select_2"}),
        required=False,
    )

    price_frequency = forms.ChoiceField(
        choices=PRICE_FREQUENCY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control select_2"}),
        required=False,
    )

    owner = OwnerChoiceField(
        queryset=Owner.objects.none(),
        widget=forms.Select(attrs={"class": "form-control select_2"}),
        required=False,
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        widget=forms.Select(attrs={"class": "form-control select_2"}),
        required=False,
    )

    township = forms.ModelChoiceField(
        queryset=Township.objects.none(),
        widget=forms.Select(attrs={"class": "form-control select_2"}),
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
            "price_frequency",
            "contract_duration",
            "property_status",
            "video_link",
            "description",
            "floor",
            "bedroom",
            "bathroom",
            "installment",
            "co_brokerage",
            "owner",
            "amenities",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Property Title"}
            ),
            "property_type": forms.Select(attrs={"class": "form-control select_2"}),
            "area": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Size"}
            ),
            "area_unit": forms.Select(attrs={"class": "form-control select_2"}),
            "country": forms.Select(attrs={"class": "form-control select_2"}),
            "city": forms.Select(attrs={"class": "form-control select_2"}),
            "township": forms.Select(attrs={"class": "form-control select_2"}),
            "purpose": forms.Select(attrs={"class": "form-control select_2"}),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Price"}
            ),
            "currency": forms.Select(attrs={"class": "form-control select_2"}),
            "contract_duration": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Contract Duration"}
            ),
            "floor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Ground, 1st Floor, Penthouse",
                }
            ),
            "bedroom": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g. 1, 2, Studio"}
            ),
            "bathroom": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g. 1, 2, 1.5"}
            ),
            "video_link": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "YouTube or Video URL"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control summer_note", "rows": 10}
            ),
            "installment": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "co_brokerage": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter owner by company
        if company:
            self.fields["owner"].queryset = Owner.objects.filter(
                company=company
            ).select_related("company")

        # ===== Populate city queryset based on selected country =====
        if "country" in self.data:
            try:
                country_id = int(self.data.get("country"))
                self.fields["city"].queryset = City.objects.filter(
                    country_id=country_id
                ).order_by("name")
            except (ValueError, TypeError):
                self.fields["city"].queryset = City.objects.none()
        elif self.instance.pk and self.instance.city:
            self.fields["city"].queryset = City.objects.filter(
                country=self.instance.country
            )

        # ===== Populate township queryset based on selected city =====
        if "city" in self.data:
            try:
                city_id = int(self.data.get("city"))
                self.fields["township"].queryset = Township.objects.filter(
                    city_id=city_id
                ).order_by("name")
            except (ValueError, TypeError):
                self.fields["township"].queryset = Township.objects.none()
        elif self.instance.pk and self.instance.township:
            self.fields["township"].queryset = Township.objects.filter(
                city=self.instance.city
            )

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
