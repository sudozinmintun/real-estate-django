from django.shortcuts import render


def order_form(request, id):
    return render(request, "order/order_form.html")
