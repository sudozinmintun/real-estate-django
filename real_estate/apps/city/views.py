from apps.city.models import City, Township
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string


def get_cities(request):
    country_id = request.GET.get("country")
    cities = City.objects.filter(country_id=country_id)

    html = render_to_string("partials/city_options.html", {"cities": cities})
    return JsonResponse({"html": html})


def get_townships(request):
    city_id = request.GET.get("city")
    townships = Township.objects.filter(city_id=city_id)

    html = render_to_string("partials/township_options.html", {"townships": townships})
    return JsonResponse({"html": html})
