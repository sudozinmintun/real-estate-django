from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from apps.accounts.models import Profile
from apps.accounts.forms import (
    LoginForm,
    ProfileUpdateForm,
    UserUpdateForm,
    CustomPasswordChangeForm,
    CompanyRegistrationForm,
    UserRegistrationForm,
)


def user_login(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )

        login(request, user)
        return redirect("accounts:dashboard")

    return render(request, "accounts/login.html", {"form": form})


def user_register(request):
    company_form = CompanyRegistrationForm(request.POST or None)
    user_form = UserRegistrationForm(request.POST or None)

    if request.method == "POST":
        if company_form.is_valid() and user_form.is_valid():
            try:
                with transaction.atomic():
                    company = company_form.save()

                    user_data = user_form.cleaned_data
                    user = User.objects.create_user(
                        username=user_data["email"],
                        email=user_data["email"],
                        password=user_data["password"],
                        first_name=user_data["full_name"],
                    )

                    profile, created = Profile.objects.get_or_create(user=user)
                    profile.company = company
                    profile.save()

                login(
                    request, user, backend="django.contrib.auth.backends.ModelBackend"
                )

                messages.success(request, f"Welcome to {company.name}!")
                return redirect("accounts:dashboard")

            except Exception as e:
                company_form.add_error(None, f"Registration failed: {str(e)}")

    context = {
        "company_form": company_form,
        "user_form": user_form,
    }
    return render(request, "accounts/register.html", context)


def user_logout(request):
    logout(request)
    return redirect("accounts:login")


@login_required(login_url="accounts:login")
def dashboard(request):
    return render(request, "accounts/dashboard.html")


@login_required(login_url="accounts:login")
def profile(request):
    profile = request.user.profile

    if request.method == "POST":
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")

    else:
        p_form = ProfileUpdateForm(instance=profile)
        u_form = UserUpdateForm(instance=request.user)
        change_password_form = CustomPasswordChangeForm(user=request.user)

    return render(
        request,
        "accounts/profile.html",
        {
            "p_form": p_form,
            "u_form": u_form,
            "change_password_form": change_password_form,
        },
    )


@login_required(login_url="accounts:login")
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated successfully.")
            return redirect("accounts:profile")
        else:
            messages.error(request, "Unable to update your password. Please try again.")
            return redirect("accounts:profile")
