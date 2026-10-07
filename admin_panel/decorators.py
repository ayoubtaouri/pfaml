from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


def admin_required(view_func):
    """Decorator to check if user is admin"""
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if request.user.is_admin or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden('Access denied. Admin privileges required.')
    return wrapper
