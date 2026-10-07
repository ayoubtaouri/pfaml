from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm, PasswordChangeCustomForm
from detection.models import Prediction


@require_http_methods(["GET", "POST"])
def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = CustomAuthenticationForm()
    
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    """User dashboard"""
    user = request.user
    predictions = Prediction.objects.filter(user=user).order_by('-created_at')[:10]
    
    # Calculate statistics
    total_predictions = Prediction.objects.filter(user=user).count()
    risk_stats = {}
    for risk_level in ['LOW', 'MEDIUM', 'HIGH']:
        risk_stats[risk_level] = Prediction.objects.filter(
            user=user,
            risk_level=risk_level
        ).count()
    
    context = {
        'user': user,
        'predictions': predictions,
        'total_predictions': total_predictions,
        'risk_stats': risk_stats,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def profile(request):
    """User profile view — update info & password"""
    user = request.user

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_info':
            form = ProfileUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profil mis à jour avec succès.')
                return redirect('profile')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        elif action == 'change_password':
            pw_form = PasswordChangeCustomForm(user=user, data=request.POST)
            if pw_form.is_valid():
                pw_form.save()
                update_session_auth_hash(request, pw_form.user)
                messages.success(request, 'Mot de passe modifié avec succès.')
                return redirect('profile')
            else:
                for field, errors in pw_form.errors.items():
                    for error in errors:
                        messages.error(request, error)

    profile_form = ProfileUpdateForm(instance=user)
    pw_form = PasswordChangeCustomForm(user=user)

    total_predictions = Prediction.objects.filter(user=user).count()
    last_prediction = Prediction.objects.filter(user=user).order_by('-created_at').first()

    context = {
        'profile_form': profile_form,
        'pw_form': pw_form,
        'total_predictions': total_predictions,
        'last_prediction': last_prediction,
    }
    return render(request, 'accounts/profile.html', context)
