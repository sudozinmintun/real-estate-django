from django.shortcuts import render, redirect, get_object_or_404
from apps.package.models import Package
from django.contrib.auth.decorators import login_required
from apps.payment.models import Payment
from apps.order.models import Order
from django.contrib import messages


@login_required(login_url="accounts:login")
def pricing_plan(request):
    packages = Package.objects.exclude(price=0)
    payments = Payment.objects.all()
    context = {
        "packages": packages,
        "payments": payments,
    }
    return render(request, "package/pricing_plan.html", context=context)


@login_required(login_url="accounts:login")
def create_order(request):
    if request.method != "POST":
        return redirect("package:pricing_plan")

    package_id = request.POST.get("package_id")
    payment_id = request.POST.get("payment")
    screenshot = request.FILES.get("screenshot")

    # 🔐 Validate package
    if not package_id:
        messages.error(request, "Invalid package selection.")
        return redirect("package:pricing_plan")

    package = get_object_or_404(Package, id=int(package_id))

    # 🔐 Handle empty payment correctly
    payment = None
    if payment_id and payment_id.isdigit():
        payment = Payment.objects.get(id=int(payment_id))

    Order.objects.create(
        user=request.user,
        package=package,
        payment=payment,
        screenshot=screenshot,
        amount=package.price,
        status=Order.STATUS_PENDING,
    )

    messages.success(request, "Order submitted successfully. Waiting for approval.")
    return redirect("package:pricing_plan")
