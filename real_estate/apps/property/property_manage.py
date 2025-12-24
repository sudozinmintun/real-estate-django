from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.property.forms import PropertyForm
from apps.property.models import Property, PropertyPhoto
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.db.models import Q
from apps.property_type.models import PropertyType
from apps.country.models import Currency, Country

@login_required(login_url="accounts:login")
def property_list(request):
    types = PropertyType.objects.all()
    currencies = Currency.objects.all()
    countries = Country.objects.all()
    context = {
        "types": types,
        "currencies": currencies,
        "countries": countries,
    }
    return render(request, "property/manage/list.html", context=context)


@login_required(login_url="accounts:login")
def property_list_htmx(request):
    q = request.GET.get("q", "").strip()
    country_id = request.GET.get("country")
    city_id = request.GET.get("city")
    township_id = request.GET.get("township")
    type_id = request.GET.get("property_type")
    purpose = request.GET.get("purpose")
    bedroom = request.GET.get("bedroom")
    bathroom = request.GET.get("bathroom")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    currency = request.GET.get("currency")

    properties = Property.objects.filter(user=request.user)

    # Text search
    if q:
        properties = properties.filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        )

    # Country → City → Township
    if country_id:
        properties = properties.filter(country_id=country_id)

    if city_id:
        properties = properties.filter(city_id=city_id)

    if township_id:
        properties = properties.filter(township_id=township_id)

    # Property type
    if type_id:
        properties = properties.filter(property_type_id=type_id)

    # Purpose
    if purpose:
        properties = properties.filter(purpose=purpose)

    # Bedrooms + Bathrooms
    if bedroom:
        properties = properties.filter(bedroom__icontains=bedroom)

    if bathroom:
        properties = properties.filter(bathroom__icontains=bathroom)

    # Price range
    if min_price:
        properties = properties.filter(price__gte=min_price)

    if max_price:
        properties = properties.filter(price__lte=max_price)

    if currency:
        properties = properties.filter(currency_id=currency)

    context = {"properties": properties}
    return render(request, "property/manage/_table_body.html", context)


@login_required(login_url="accounts:login")
def property_list_htmx1(request):
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

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
    ALLOWED_EXT = ["jpg", "jpeg", "png"]
    MAX_PHOTOS = 20  # optional limit

    if request.method == "POST":
        photos = request.FILES.getlist("photos")

        # optional: block too many uploads
        if len(photos) > MAX_PHOTOS:
            messages.error(
                request, f"You can upload a maximum of {MAX_PHOTOS} photos at once."
            )
            return redirect(request.path)

        for img in photos:
            # validate file size
            if img.size > MAX_FILE_SIZE:
                messages.error(
                    request, f"{img.name} is too large. Maximum allowed size is 5 MB."
                )
                return redirect(request.path)

            # validate file extension
            ext = img.name.split(".")[-1].lower()
            if ext not in ALLOWED_EXT:
                messages.error(
                    request,
                    f"{img.name} has invalid format. Allowed: JPG, JPEG, PNG.",
                )
                return redirect(request.path)

            # save valid image
            PropertyPhoto.objects.create(property=property_instance, image=img)

        messages.success(request, "Photos uploaded successfully.")
        return redirect("property:backend_list")

    context = {"property": property_instance}
    return render(request, "property/manage/photo_upload.html", context)


@login_required(login_url="accounts:login")
@require_http_methods(["POST", "DELETE"])
def photo_delete(request, id):
    photo = get_object_or_404(PropertyPhoto, id=id, property__user=request.user)
    photo.delete()
    return HttpResponse("", status=200)
