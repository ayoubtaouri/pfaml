from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from contact.models import ContactMessage


@require_http_methods(["GET"])
def home(request):
    """Home page - public"""
    context = {}
    return render(request, 'home.html', context)


@require_http_methods(["GET"])
def about(request):
    """About page - public"""
    context = {}
    return render(request, 'about.html', context)
