from django.urls import path
from . import views

app_name = "owners"
urlpatterns = [
    path("owners/", views.index, name="index"),
    path("owners/create/", views.create, name="create"),
    path("owners/<int:pk>/edit/", views.edit, name="edit"),
    path("owners/<int:pk>/delete/", views.delete, name="delete"),
]
