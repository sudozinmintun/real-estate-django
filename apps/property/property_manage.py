from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.property.forms import PropertyForm
from apps.property.models import Property, PropertyPhoto
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse


@login_required(login_url="accounts:login")
def property_list(request):
    return render(request, "property/manage/list.html")


@login_required(login_url="accounts:login")
def property_list_htmx(request):
    q = request.GET.get("q", "")
    properties = Property.objects.filter(
        user=request.user,
        title__icontains=q,
    )
    context = {"properties": properties}
    return render(request, "property/manage/_table_body.html", context)


@login_required(login_url="accounts:login")
def property_create(request):
    form = PropertyForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.user = request.user
            property_instance.save()
            form.save_m2m()

            messages.success(request, "Property created successfully!")
            return redirect("property:backend_create")

    return render(request, "property/manage/property_form.html", {"form": form})


@login_required(login_url="accounts:login")
def property_edit(request, id):
    property_instance = get_object_or_404(Property, id=id, user=request.user)
    form = PropertyForm(request.POST or None, instance=property_instance)

    if request.method == "POST":
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.user = request.user
            property_instance.save()
            form.save_m2m()
            messages.success(request, "Property updated successfully!")
            return redirect("property:backend_list")

    return render(request, "property/manage/property_form.html", {"form": form})


@login_required(login_url="accounts:login")
@require_http_methods(["POST", "DELETE"])
def property_delete(request, id):
    property_instance = get_object_or_404(Property, id=id, user=request.user)
    property_instance.delete()

    if request.headers.get("Hx-Request"):
        return HttpResponse("")  # HTMX removes the row dynamically

    messages.success(request, "Property deleted successfully!")
    return redirect("property:backend_list")


@login_required(login_url="accounts:login")
def photo_upload(request, id):
    property_instance = get_object_or_404(Property, id=id, user=request.user)

    if request.method == "POST":
        photos = request.FILES.getlist("photos")

        for img in photos:
            PropertyPhoto.objects.create(property=property_instance, image=img)

        return redirect("property:backend_edit", id=id)

    context = {"property": property_instance}
    return render(request, "property/manage/photo_upload.html", context)
