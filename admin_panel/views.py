from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
import csv

from admin_panel.decorators import admin_required
from accounts.models import CustomUser
from detection.models import Prediction
from contact.models import ContactMessage


@admin_required
def dashboard(request):
    """Admin dashboard with statistics"""
    
    # Total users and stats
    total_users = CustomUser.objects.filter(role='user').count()
    total_admins = CustomUser.objects.filter(role='admin').count()
    total_predictions = Prediction.objects.count()
    
    # Risk level distribution
    risk_distribution = Prediction.objects.values('risk_level').annotate(count=Count('id'))
    
    # Unread messages
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    
    # Recent predictions
    recent_predictions = Prediction.objects.select_related('user').order_by('-created_at')[:10]
    
    context = {
        'total_users': total_users,
        'total_admins': total_admins,
        'total_predictions': total_predictions,
        'risk_distribution': risk_distribution,
        'unread_messages': unread_messages,
        'recent_predictions': recent_predictions,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@admin_required
def users_list(request):
    """List all users with pagination and search"""
    
    query = request.GET.get('q', '')
    role_filter = request.GET.get('role', '')
    
    users = CustomUser.objects.filter(role='user')
    
    if query:
        users = users.filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    if role_filter:
        users = users.filter(role=role_filter)
    
    # Add prediction count
    users = users.annotate(prediction_count=Count('predictions'))
    
    paginator = Paginator(users, 20)  # 20 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'role_filter': role_filter,
    }
    return render(request, 'admin_panel/users_list.html', context)


@admin_required
def user_detail(request, user_id):
    """Display detailed user profile with prediction history"""
    
    user = get_object_or_404(CustomUser, id=user_id, role='user')
    predictions = Prediction.objects.filter(user=user).order_by('-created_at')
    
    # Statistics
    total_predictions = predictions.count()
    risk_stats = {}
    for risk_level in ['LOW', 'MEDIUM', 'HIGH']:
        risk_stats[risk_level] = predictions.filter(risk_level=risk_level).count()
    
    # Paginate predictions
    paginator = Paginator(predictions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'user': user,
        'page_obj': page_obj,
        'total_predictions': total_predictions,
        'risk_stats': risk_stats,
    }
    return render(request, 'admin_panel/user_detail.html', context)


@admin_required
def toggle_user_status(request, user_id):
    """Toggle user active/inactive status"""
    
    user = get_object_or_404(CustomUser, id=user_id, role='user')
    
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        
        status = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'User {user.email} has been {status}.')
    
    return redirect('admin_panel:user_detail', user_id=user_id)


@admin_required
def export_user_history(request, user_id):
    """Export user's prediction history as CSV"""
    
    user = get_object_or_404(CustomUser, id=user_id, role='user')
    predictions = Prediction.objects.filter(user=user).order_by('-created_at')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="user_{user.id}_history.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Date', 'Age', 'Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness',
        'Insulin', 'BMI', 'Diabetes Pedigree', 'Risk Score', 'Risk Level'
    ])
    
    for pred in predictions:
        writer.writerow([
            pred.created_at.strftime('%Y-%m-%d %H:%M'),
            pred.age,
            pred.pregnancies,
            pred.glucose,
            pred.blood_pressure,
            pred.skin_thickness,
            pred.insulin,
            pred.bmi,
            pred.diabetes_pedigree,
            f'{pred.risk_score:.4f}',
            pred.risk_level,
        ])
    
    return response


@admin_required
def messages_list(request):
    """List contact messages"""
    
    read_filter = request.GET.get('read', '')
    messages_qs = ContactMessage.objects.order_by('-created_at')
    
    if read_filter == 'read':
        messages_qs = messages_qs.filter(is_read=True)
    elif read_filter == 'unread':
        messages_qs = messages_qs.filter(is_read=False)
    
    paginator = Paginator(messages_qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    unread_count = ContactMessage.objects.filter(is_read=False).count()
    
    context = {
        'page_obj': page_obj,
        'read_filter': read_filter,
        'unread_count': unread_count,
    }
    return render(request, 'admin_panel/messages_list.html', context)


@admin_required
def message_detail(request, message_id):
    """Display message detail"""
    
    message = get_object_or_404(ContactMessage, id=message_id)
    
    if request.method == 'POST':
        message.mark_as_read()
        messages.success(request, 'Message marked as read.')
    
    context = {'message': message}
    return render(request, 'admin_panel/message_detail.html', context)


@admin_required
@require_http_methods(["POST"])
def admin_delete_prediction(request, prediction_id):
    """Delete any prediction (Admin only)"""
    try:
        prediction = Prediction.objects.get(id=prediction_id)
        prediction.delete()
        messages.success(request, 'Prediction deleted successfully.')
    except Prediction.DoesNotExist:
        messages.error(request, 'Prediction not found.')
    
    # Redirect back to the page the admin came from, or dashboard
    next_url = request.POST.get('next', 'admin_panel:dashboard')
    return redirect(next_url)
