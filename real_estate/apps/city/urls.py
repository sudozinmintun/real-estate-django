from django.urls import path
from . import views

app_name = "city"
urlpatterns = [
    path("get-cities/", views.get_cities, name="get_cities"),
    path('get-townships/', views.get_townships, name='get_townships'),
]
