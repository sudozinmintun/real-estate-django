from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url="accounts:login")
def property_list(request):
    return render(request, "property/manage/list.html")


def property_create(request):
    return render(request, "property/manage/create.html")


def property_edit(request):
    return render(request, "property/manage/list.html")


def property_delete(request):
    return render(request, "property/manage/list.html")
