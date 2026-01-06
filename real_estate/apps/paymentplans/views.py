from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import PaymentPlan
from .forms import PaymentPlanForm, PaymentPlanStepFormSet


@login_required
def index(request):
    plans = PaymentPlan.objects.filter(company=request.user.profile.company)
    return render(request, "paymentplans/index.html", {"plans": plans})


@login_required
def create(request):
    if request.method == "POST":
        form = PaymentPlanForm(request.POST)

        if form.is_valid():
            plan = form.save(commit=False)
            plan.company = request.user.profile.company
            plan.created_by = request.user
            plan.save()

            formset = PaymentPlanStepFormSet(request.POST, instance=plan)

            if formset.is_valid():
                formset.save()
                return redirect("paymentplans:index")
    else:
        form = PaymentPlanForm()
        formset = PaymentPlanStepFormSet()

    return render(
        request,
        "paymentplans/form.html",
        {"form": form, "formset": formset},
    )


@login_required
def update(request, pk):
    plan = get_object_or_404(PaymentPlan, pk=pk, company=request.user.profile.company)

    if request.method == "POST":
        form = PaymentPlanForm(request.POST, instance=plan)
        formset = PaymentPlanStepFormSet(request.POST, instance=plan)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("paymentplan_list")
    else:
        form = PaymentPlanForm(instance=plan)
        formset = PaymentPlanStepFormSet(instance=plan)
    context = {"form": form, "formset": formset, "object": plan}
    return render(request, "paymentplans/plan_form.html", context)


@login_required
def delete(request, pk):
    plan = get_object_or_404(PaymentPlan, pk=pk, company=request.user.profile.company)

    if request.method == "POST":
        plan.delete()
        return redirect("paymentplan:index")

    return render(request, "paymentplans/plan_confirm_delete.html", {"object": plan})
