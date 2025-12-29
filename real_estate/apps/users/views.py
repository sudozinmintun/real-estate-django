from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from apps.accounts.models import Profile
from apps.accounts.forms import AddNewUserForm, AddNewProfileForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import logout


@login_required(login_url="accounts:login")
def users(request):
    users = User.objects.filter(profile__company=request.company).select_related(
        "profile"
    )
    context = {"current_company": request.company, "users": users}

    return render(request, "users/users.html", context)


@login_required(login_url="accounts:login")
def create(request):
    user_form = AddNewUserForm(request.POST or None)
    profile_form = AddNewProfileForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        admin = request.user
        company = admin.profile.company

        user = User.objects.create_user(
            username=user_form.cleaned_data["email"],
            email=user_form.cleaned_data["email"],
            password=user_form.cleaned_data["password"],
            first_name=user_form.cleaned_data["full_name"],
        )

        Profile.objects.update_or_create(
            user=user,
            defaults={
                "company": company,
                "created_by": admin,
                "user_type": "MEMBER",
                **profile_form.cleaned_data,
            },
        )

        return redirect("users:users")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "users/form.html", context)


@login_required(login_url="accounts:login")
def edit(request, pk):
    user = User.objects.filter(pk=pk, profile__company=request.company).first()
    if not user:
        messages.error(request, "You cannot access this user.")
        return redirect("pages:unauthorized")

    # 2. Logic flags
    is_self = request.user.pk == user.pk
    is_admin = request.user.is_staff  # is_staff = 1 → admin

    # 3. Permission check
    if not (is_self or is_admin):
        messages.error(request, "You do not have permission to edit this account.")
        return redirect("users:users")

    profile = user.profile

    user_form = AddNewUserForm(request.POST or None, instance=user)
    profile_form = AddNewProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile,
    )

    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user_form.save()

        profile_form.save(commit=False)
        profile_form.instance.updated_by = request.user
        profile_form.save()

        return redirect("users:users")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "users/form.html", context)


@login_required(login_url="accounts:login")
def delete(request, pk):
    # 1. Fetch the user (must belong to same company)
    target_user = User.objects.filter(pk=pk, profile__company=request.company).first()

    if not target_user:
        messages.error(request, "You cannot access this user.")
        return redirect("pages:unauthorized")

    # 2. Logic flags
    is_self = request.user.pk == target_user.pk
    is_admin = request.user.is_staff  # is_staff = 1 → admin

    # 3. Permission check
    if not (is_self or is_admin):
        messages.error(request, "You do not have permission to delete this account.")
        return redirect("users:users")

    # 4. Prevent deleting the last admin
    if is_admin:
        admin_count = User.objects.filter(
            profile__company=request.company, is_staff=True
        ).count()

        if target_user.is_staff and admin_count <= 1:
            messages.error(request, "You can’t delete an admin account.")
            return redirect("users:users")

    # 5. Handle deletion (POST)
    if request.method == "POST":
        username = target_user.username
        target_user.delete()

        # If they deleted themselves → logout
        if is_self:
            logout(request)
            messages.success(request, "Your account has been successfully deleted.")
            return redirect("accounts:login")

        messages.success(request, f"User {username} has been deleted.")
        return redirect("users:users")

    # 6. Confirmation page (GET)
    return render(
        request,
        "users/confirm_delete.html",
        {"target_user": target_user, "is_self": is_self},
    )
