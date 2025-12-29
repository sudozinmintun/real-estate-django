from django.urls import path
from . import views

app_name = "property"
urlpatterns = [
    path("properties/", views.properties, name="properties"),
    path("properties/htmx-list/", views.property_list_htmx, name="backend_htmx_list"),
    path("property/create", views.create, name="create"),
    path(
        "manage/properties/create/",
        views.create,
        name="backend_create",
    ),
    path(
        "manage/properties/<int:id>/edit/",
        views.property_edit,
        name="backend_edit",
    ),
    path(
        "manage/properties/<int:id>/delete/",
        views.property_delete,
        name="backend_delete",
    ),
    path(
        "manage/properties/<int:id>/upload/",
        views.photo_upload,
        name="backend_photo_upload",
    ),
    path("photo/delete/<int:id>/", views.photo_delete, name="photo_delete"),
]
