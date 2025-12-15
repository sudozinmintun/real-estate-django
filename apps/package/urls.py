from django.urls import path
from . import views

app_name = "package"
urlpatterns = [
    path("pricing/plan/", views.pricing_plan, name="pricing_plan"),
    path("order/create/", views.create_order, name="create_order"),
]
