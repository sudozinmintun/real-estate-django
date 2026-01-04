from django.urls import path
from . import views

app_name = "lawyers"
urlpatterns = [
    path("lawyers/", views.index, name="index"),
    path("lawyers/create/", views.create, name="create"),
    path("lawyers/<int:pk>/edit/", views.edit, name="edit"),
    path("lawyers/<int:pk>/delete/", views.delete, name="delete"),
]
