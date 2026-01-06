from django.urls import path
from . import views

app_name = "paymentplans"
urlpatterns = [
    path("plans/", views.index, name="index"),
    path("plans/create/", views.create, name="create"),
    path("plans/<int:pk>/edit/", views.update, name="edit"),
    path("plans/<int:pk>/delete/", views.delete, name="delete"),
]
