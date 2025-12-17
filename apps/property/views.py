from django.shortcuts import render
from apps.property.models import Property


def properties(request):
    return render(request, "property/properties.html")


def property_list_htmx(request):
    q = request.GET.get("q", "")
    properties = Property.objects.filter(title__icontains=q)

    context = {"properties": properties}
    return render(request, "property/partials/property_list.html", context)
