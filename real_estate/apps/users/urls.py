from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("users/", views.users, name="users"),
    path("users/create/", views.create, name="create"),
    path("users/<int:pk>/edit/", views.edit, name="edit"),
    path("users/<int:pk>/delete/", views.delete, name="delete"),
]
