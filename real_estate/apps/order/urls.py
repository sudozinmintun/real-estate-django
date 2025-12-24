from django.urls import path
from . import views

app_name = "order"
urlpatterns = [
    path("order/", views.order, name="order"),
]
