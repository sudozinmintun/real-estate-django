from django.urls import path
from . import views

app_name = "buyers"
urlpatterns = [
    path("buyers/", views.index, name="index"),
    path("buyers/list/htmx", views.buyer_list_htmx, name="buyer_list_htmx"),
    path("buyers/create/", views.create, name="create"),
    path("buyers/<int:pk>/edit/", views.edit, name="edit"),
    path("buyers/<int:pk>/delete/", views.delete, name="delete"),
    path("communication/logs/<int:buyer_id>", views.list_logs, name="list_logs"),
    path("create/log/<int:buyer_id>", views.create_log, name="create_log"),
]
