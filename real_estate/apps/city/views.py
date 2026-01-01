from apps.city.models import City, Township
from django.template.loader import render_to_string
from django.shortcuts import render


def get_cities(request):
    country_id = request.GET.get("country_id")
    cities = City.objects.filter(country_id=country_id)
    return render(request, 'partials/city_options.html', {'cities': cities})


def get_townships(request):
    city_id = request.GET.get("city_id")
    townships = Township.objects.filter(city_id=city_id)
    return render(request, 'partials/township_options.html', {'townships': townships})

