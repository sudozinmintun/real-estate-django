from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.lawyers.models import Lawyer
from apps.lawyers.forms import LawyerForm
from django.contrib import messages


@login_required(login_url="accounts:login")
def index(request):
    lawyers = Lawyer.objects.filter(
        company=request.user.profile.company
    ).select_related("company")

    context = {"lawyers": lawyers}

    return render(request, "lawyers/index.html", context)


@login_required(login_url="accounts:login")
def create(request):
    if request.method == "POST":
        form = LawyerForm(request.POST)
        if form.is_valid():
            lawyer = form.save(commit=False)
            admin = request.user
            lawyer.company = request.user.profile.company
            lawyer.created_by = admin

            lawyer.save()
            return redirect("lawyers:index")
    else:
        form = LawyerForm()

    return render(request, "lawyers/form.html", {"form": form})


@login_required(login_url="accounts:login")
def edit(request, pk):
    lawyer = Lawyer.objects.filter(pk=pk, company=request.user.profile.company).first()

    if not lawyer:
        messages.error(request, "You cannot access this lawyer.")
        return redirect("pages:unauthorized")

    form = LawyerForm(request.POST or None, instance=lawyer)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Lawyer updated successfully.")
        return redirect("lawyers:index")

    return render(request, "lawyers/form.html", {"form": form})


@login_required(login_url="accounts:login")
def delete(request, pk):
    laywer = Lawyer.objects.filter(pk=pk, company=request.user.profile.company).first()

    if not laywer:
        messages.error(request, "You cannot access this laywer.")
        return redirect("pages:unauthorized")

    if request.method == "POST":
        laywer.delete()
        messages.success(request, "Lawyer deleted successfully.")
        return redirect("lawyers:index")

    return render(request, "lawyers/confirm_delete.html", {"laywer": laywer})
