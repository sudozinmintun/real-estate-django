from django.shortcuts import render
from apps.order.models import Order
from django.contrib.auth.decorators import login_required


@login_required(login_url="accounts:login")
def order(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        "orders": orders,
    }
    return render(request, "order/order.html", context)
