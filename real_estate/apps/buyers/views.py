from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.buyers.models import Buyer, CommunicationLog, STATUS_CHOICES, SOURCE_CHOICES
from apps.buyers.forms import BuyerForm, CommunicationLogForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User


@login_required(login_url="accounts:login")
def index(request):
    users = User.objects.filter(
        profile__company=request.user.profile.company
    ).select_related("profile")
    context = {
        "STATUS_CHOICES": STATUS_CHOICES,
        "SOURCE_CHOICES": SOURCE_CHOICES,
        "users": users,
    }

    return render(request, "buyers/index.html", context)


@login_required(login_url="accounts:login")
def buyer_list_htmx(request):
    buyers = Buyer.objects.filter(company=request.user.profile.company).select_related(
        "company"
    )

    q = request.GET.get("q", "").strip()
    status = request.GET.get("status")
    source = request.GET.get("source")
    assigned_to = request.GET.get("assigned_to")
    budget_min = request.GET.get("budget_min")
    budget_max = request.GET.get("budget_max")
    preferred_location = request.GET.get("preferred_location", "").strip()
    preferred_type = request.GET.get("preferred_type", "").strip()
    deal_probability = request.GET.get("deal_probability")
    notes = request.GET.get("notes", "").strip()

    if q:
        buyers = buyers.filter(
            Q(name__icontains=q)
            | Q(email__icontains=q)
            | Q(phone__icontains=q)
            | Q(address__icontains=q)
        )

    if status:
        buyers = buyers.filter(status=status)
    if source:
        buyers = buyers.filter(source=source)
    if assigned_to:
        buyers = buyers.filter(assigned_to_id=assigned_to)
    if preferred_location:
        buyers = buyers.filter(preferred_location__icontains=preferred_location)
    if preferred_type:
        buyers = buyers.filter(preferred_type__icontains=preferred_type)

    if deal_probability:
        # Split the range, e.g., "25-50" → [25, 50]
        try:
            min_prob, max_prob = map(int, deal_probability.split("-"))
            buyers = buyers.filter(
                deal_probability__gte=min_prob, deal_probability__lte=max_prob
            )
        except ValueError:
            pass  # ignore if the value is invalid

    if notes:
        buyers = buyers.filter(notes__icontains=notes)

    # Budget overlap filter
    if budget_min and budget_max:
        buyers = buyers.filter(
            Q(budget_min__lte=budget_max) & Q(budget_max__gte=budget_min)
        )
    elif budget_min:
        buyers = buyers.filter(budget_max__gte=budget_min)
    elif budget_max:
        buyers = buyers.filter(budget_min__lte=budget_max)

    context = {
        "buyers": buyers,
    }

    return render(request, "buyers/partials/_table_body.html", context)


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


@login_required
def list_logs(request, buyer_id):
    buyer = Buyer.objects.filter(
        id=buyer_id, company=request.user.profile.company
    ).first()

    if not buyer:
        messages.error(request, "You cannot access this buyer.")
        return redirect("pages:unauthorized")

    logs = buyer.communications.select_related("assigned_by").order_by("-created_at")

    context = {
        "buyer": buyer,
        "logs": logs,
    }
    return render(request, "buyers/communications/log_table_modal.html", context)


@login_required
def create_log(request, buyer_id):
    buyer = get_object_or_404(Buyer, id=buyer_id, company=request.user.profile.company)

    if request.method == "POST":
        form = CommunicationLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.buyer = buyer
            log.company = request.user.profile.company
            log.created_by = request.user
            log.assigned_by = request.user
            log.save()
            return list_logs(request, buyer_id)
    else:
        form = CommunicationLogForm()

    context = {"form": form, "buyer": buyer}
    return render(request, "buyers/communications/form_modal.html", context)
