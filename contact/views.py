from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from contact.models import ContactMessage
from contact.forms import ContactForm


@require_http_methods(["GET", "POST"])
def contact(request):
    """Contact form view"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('home')
        else:
            messages.error(request, 'There was an error submitting your message.')
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'contact/form.html', context)
