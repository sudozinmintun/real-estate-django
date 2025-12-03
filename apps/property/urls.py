from django.urls import path
from . import views

app_name = "property"
urlpatterns = [
    path("properties/", views.properties, name="properties"),
    path("properties/htmx-list/", views.property_list_htmx, name="property_list_htmx"),
]
