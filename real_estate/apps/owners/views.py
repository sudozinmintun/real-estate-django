from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.owners.models import Owner
from apps.owners.forms import OwnerForm
from django.contrib import messages
from django.shortcuts import get_object_or_404


@login_required(login_url="accounts:login")
def index(request):
    owners = Owner.objects.filter(company=request.company).select_related("company")
    context = {"owners": owners}

    return render(request, "owners/index.html", context)


@login_required(login_url="accounts:login")
def create(request):
    if request.method == "POST":
        form = OwnerForm(request.POST)
        if form.is_valid():
            owner = form.save(commit=False)

            admin = request.user
            owner.company = admin.profile.company
            owner.created_by = admin

            owner.save()
            return redirect("owners:index")
    else:
        form = OwnerForm()

    return render(request, "owners/form.html", {"form": form})


@login_required(login_url="accounts:login")
def edit(request, pk):
    owner = Owner.objects.filter(pk=pk, company=request.company.id).first()

    if not owner:
        messages.error(request, "You cannot access this owner.")
        return redirect("pages:unauthorized")

    form = OwnerForm(request.POST or None, instance=owner)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Owner updated successfully.")
        return redirect("owners:index")

    return render(request, "owners/form.html", {"form": form})


@login_required(login_url="accounts:login")
def delete(request, pk):
    owner = Owner.objects.filter(pk=pk, company_id=request.company.id).first()

    if not owner:
        messages.error(request, "You cannot access this owner.")
        return redirect("pages:unauthorized")

    if request.method == "POST":
        owner.delete()
        messages.success(request, "Owner deleted successfully.")
        return redirect("owners:index")

    return render(request, "owners/confirm_delete.html", {"owner": owner})
