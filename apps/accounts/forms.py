from django import forms
from apps.accounts.models import Profile
from django.contrib.auth.models import User
from apps.country.models import Country
from apps.city.models import City
from django.contrib.auth.forms import PasswordChangeForm


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
            }
        )
    )


class ProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone",
            }
        ),
    )
    address = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Address",
            }
        ),
    )
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Select Country",
            }
        ),
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Select City",
            }
        ),
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "placeholder": "Profile Photo",
            }
        ),
    )

    facebook = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Facebook Link",
            }
        ),
    )

    linkedin = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Public profile & URL",
            }
        ),
    )

    x = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "X",
            }
        ),
    )

    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Website Link",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ["phone", "country", "city", "address", "photo", "facebook", "linkedin", "x", "website"]


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First Name",
            }
        )
    )

    class Meta:
        model = User
        fields = ["first_name"]


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Current Password"}
        )
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New Password"}
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        )
    )
