from django.urls import path
from . import views

app_name = "buyers"
urlpatterns = [
    path("buyers/", views.index, name="index"),
    path("buyers/create/", views.create, name="create"),
    path("buyers/<int:pk>/edit/", views.edit, name="edit"),
    path("buyers/<int:pk>/delete/", views.delete, name="delete"),
]
