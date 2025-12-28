from django.shortcuts import render


def home(request):
    return render(request, "pages/home.html")


def contact(request):
    return render(request, "pages/contact.html")

def unauthorized(request):
    return render(request, "pages/unauthorized.html")
