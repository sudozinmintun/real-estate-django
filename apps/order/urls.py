from django.urls import path
from . import views

app_name = "order"
urlpatterns = [
    path("package/order/<int:id>/form/", views.order_form, name="order_form"),
]
