from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.buyers.models import Buyer
from apps.buyers.forms import BuyerForm
from django.contrib import messages


@login_required(login_url="accounts:login")
def index(request):
    buyers = Buyer.objects.filter(company=request.company).select_related("company")
    context = {"buyers": buyers}

    return render(request, "buyers/index.html", context)


@login_required(login_url="accounts:login")
def create(request):
    admin = request.user
    if request.method == "POST":
        form = BuyerForm(request.POST, user=admin)
        if form.is_valid():
            buyer = form.save(commit=False)
            buyer.company = admin.profile.company
            buyer.created_by = admin
            buyer.assigned_to = admin
            buyer.save()
            return redirect("buyers:index")
    else:
        form = BuyerForm(user=admin)

    return render(request, "buyers/form.html", {"form": form})


@login_required(login_url="accounts:login")
def edit(request, pk):
    buyer = Buyer.objects.filter(pk=pk, company=request.user.profile.company).first()

    if not buyer:
        messages.error(request, "You cannot access this buyer.")
        return redirect("pages:unauthorized")

    if request.method == "POST":
        form = BuyerForm(request.POST, instance=buyer, user=request.user)
        if form.is_valid():
            buyer = form.save(commit=False)
            buyer.company = buyer.company 
            buyer.created_by = buyer.created_by 
            buyer.save()
            messages.success(request, "Buyer updated successfully.")
            return redirect("buyers:index")
    else:
        form = BuyerForm(instance=buyer, user=request.user)
    return render(request, "buyers/form.html", {"form": form})


@login_required(login_url="accounts:login")
def delete(request, pk):
    buyer = Buyer.objects.filter(pk=pk, company_id=request.company.id).first()

    if not buyer:
        messages.error(request, "You cannot access this buyer.")
        return redirect("pages:unauthorized")

    if request.method == "POST":
        buyer.delete()
        messages.success(request, "Buyer deleted successfully.")
        return redirect("buyers:index")

    return render(request, "buyers/confirm_delete.html", {"buyer": buyer})
