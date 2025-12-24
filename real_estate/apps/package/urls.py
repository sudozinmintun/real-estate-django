from django.urls import path
from . import views

app_name = "package"
urlpatterns = [
    path("pricing/plan/", views.pricing_plan, name="pricing_plan"),
    path("confirm/order/", views.confirm_order, name="confirm_order"),
]
