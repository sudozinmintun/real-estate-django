from django import forms
from apps.accounts.models import Profile
from apps.country.models import Country
from apps.city.models import City
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from apps.accounts.models import Company


class LoginForm(forms.Form):
    use_required_attribute = False

    username = forms.CharField(
        label="Email",
        required=True,
        error_messages={
            "required": "Email address is required.",
        },
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Email address"}
        ),
    )

    password = forms.CharField(
        label="Password",
        required=True,
        error_messages={
            "required": "Password is required.",
        },
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )

    # username exists
    def clean_username(self):
        username = self.cleaned_data.get("username")

        if username and not User.objects.filter(username=username).exists():
            raise forms.ValidationError("This user does not exist.")

        return username

    # password length
    def clean_password(self):
        password = self.cleaned_data.get("password")

        if password and len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters.")

        return password

    # username + password together
    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError("Email or password is incorrect.")

        return cleaned_data


class CompanyRegistrationForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Company
        fields = ["name", "address"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Company name"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Address / Location"}
            ),
        }
        error_messages = {
            "name": {
                "unique": "A company with this name is already registered.",
            }
        }

    # Optional: Force case-insensitive check (e.g., 'Apple' vs 'apple')
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Company.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("A company with this name already exists.")
        return name


class UserRegistrationForm(forms.ModelForm):
    use_required_attribute = False

    full_name = forms.CharField(
        required=True,
        error_messages={"required": "Please enter your full name."},
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Full name"}
        ),
    )

    email = forms.EmailField(
        required=True,
        error_messages={"required": "Email address is required."},
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email address"}
        ),
    )

    password = forms.CharField(
        required=True,
        error_messages={"required": "Password is required."},
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )

    class Meta:
        model = User
        fields = ["email", "password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if password and len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters.")

        return password


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
        fields = [
            "phone",
            "country",
            "city",
            "address",
            "photo",
            "facebook",
            "linkedin",
            "x",
            "website",
        ]


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


class AddNewUserForm(forms.ModelForm):
    use_required_attribute = False

    full_name = forms.CharField(
        required=True,
        error_messages={"required": "Please enter your full name."},
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Full name"}
        ),
    )

    email = forms.EmailField(
        required=True,
        error_messages={"required": "Email address is required."},
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email address"}
        ),
    )

    password = forms.CharField(
        required=True,
        error_messages={"required": "Password is required."},
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )

    class Meta:
        model = User
        # IMPORTANT: password NOT in fields (we control it manually)
        fields = ["email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            # Editing existing user
            self.fields["full_name"].initial = self.instance.first_name

            # Password not required when editing
            self.fields["password"].required = False
            self.fields["password"].widget.attrs[
                "placeholder"
            ] = "Leave blank to keep current password"

    def clean_email(self):
        email = self.cleaned_data.get("email")

        qs = User.objects.filter(username=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("This email is already registered.")

        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password and len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["full_name"]

        password = self.cleaned_data.get("password")

        # Only set password when user typed something
        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user


GENDER_TYPE_CHOICES = [
    ("MALE", "Male"),
    ("FEMALE", "Female"),
]


class AddNewProfileForm(forms.ModelForm):
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

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Notes",
                "rows": 6,
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

    gender = forms.ChoiceField(
        required=True,
        choices=Profile.GENDER_TYPE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ["phone", "country", "city", "address", "photo", "gender", "notes"]
