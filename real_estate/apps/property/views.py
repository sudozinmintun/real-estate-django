from django.shortcuts import render
from apps.property.models import Property


def properties(request, type):
    context = {"type": type}
    return render(request, "property/properties.html", context)


def property_list_htmx(request, type):
    q = request.GET.get("q", "")
    properties = Property.objects.filter(purpose=type, title__icontains=q)
    context = {"properties": properties}
    return render(request, "property/partials/property_list.html", context)
