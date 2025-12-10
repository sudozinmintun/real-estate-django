from django.urls import path
from . import views
from . import property_manage

app_name = "property"
urlpatterns = [
    path("properties/", views.properties, name="properties"),
    path("properties/htmx-list/", views.property_list_htmx, name="property_list_htmx"),
]


urlpatterns += [
    path("manage/properties/", property_manage.property_list, name="backend_list"),
    path(
        "manage/properties/htmx-list/",
        property_manage.property_list_htmx,
        name="backend_htmx_list",
    ),
    path(
        "manage/properties/create/",
        property_manage.property_create,
        name="backend_create",
    ),
    path(
        "manage/properties/<int:id>/edit/",
        property_manage.property_edit,
        name="backend_edit",
    ),
    path(
        "manage/properties/<int:id>/delete/",
        property_manage.property_delete,
        name="backend_delete",
    ),
    path(
        "manage/properties/<int:id>/upload/",
        property_manage.photo_upload,
        name="backend_photo_upload",
    ),
    path("photo/delete/<int:id>/", property_manage.photo_delete, name="photo_delete"),
]
