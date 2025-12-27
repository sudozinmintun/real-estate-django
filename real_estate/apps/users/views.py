from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from apps.accounts.models import Profile
from apps.accounts.forms import AddNewUserForm, AddNewProfileForm
from django.shortcuts import get_object_or_404


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
    user = get_object_or_404(User, pk=pk)
    profile = get_object_or_404(Profile, user=user)

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
        "obj": user,
    }

    return render(request, "users/form.html", context)
