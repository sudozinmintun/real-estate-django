from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from apps.accounts.forms import (
    LoginForm,
    ProfileUpdateForm,
    UserUpdateForm,
    CustomPasswordChangeForm,
)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


def user_login(request):
    form = LoginForm(request.POST or None)
    message = ""
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        try:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("accounts:dashboard")
            else:
                message = "Invalid credentials"
        except User.DoesNotExist:
            message = "User with this email does not exist"

    context = {"form": form, "message": message}
    return render(request, "accounts/login.html", context=context)


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


def user_logout(request):
    logout(request)
    return redirect("accounts:login")
