from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import pandas as pd
import joblib
from django.conf import settings

from detection.models import Prediction
from detection.forms import PredictionForm

# Load ML model
try:
    MODEL_PATH = settings.ML_MODELS_DIR / 'xgboost_diabetes_model.pkl'
    ml_model = joblib.load(str(MODEL_PATH))
    print(f"ML model loaded successfully from {MODEL_PATH}")
    print(f"Features: {list(ml_model.feature_names_in_)}")
except Exception as e:
    ml_model = None
    print(f"Error loading ML model: {e}")


def get_risk_level(probability):
    """Determine risk level based on probability"""
    if probability < 0.3:
        return 'LOW'
    elif probability < 0.6:
        return 'MEDIUM'
    else:
        return 'HIGH'


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def prediction_form(request):
    """Diabetes risk prediction form"""
    if not ml_model:
        messages.error(request, "Modèle ML non disponible. Veuillez contacter l'administrateur.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            try:
                features_dict = {
                    'gender': [int(form.cleaned_data['gender'])],
                    'age': [float(form.cleaned_data['age'])],
                    'hypertension': [int(form.cleaned_data['hypertension'])],
                    'heart_disease': [int(form.cleaned_data['heart_disease'])],
                    'smoking_history': [int(form.cleaned_data['smoking_history'])],
                    'bmi': [float(form.cleaned_data['bmi'])],
                    'HbA1c_level': [float(form.cleaned_data['HbA1c_level'])],
                    'blood_glucose_level': [float(form.cleaned_data['blood_glucose_level'])],
                }
                features = pd.DataFrame(features_dict)

                probability = ml_model.predict_proba(features)[0][1]
                risk_score = float(probability)
                risk_level = get_risk_level(risk_score)

                prediction = form.save(commit=False)
                prediction.user = request.user
                prediction.risk_score = risk_score
                prediction.risk_level = risk_level
                prediction.save()

                return redirect('detection:prediction_result', pk=prediction.pk)

            except Exception as e:
                messages.error(request, f'Erreur lors du calcul : {str(e)}')
                return render(request, 'detection/form.html', {'form': form})
    else:
        form = PredictionForm()

    return render(request, 'detection/form.html', {'form': form})


@login_required(login_url='login')
def prediction_result(request, pk):
    """Display prediction result"""
    try:
        prediction = Prediction.objects.get(pk=pk, user=request.user)
    except Prediction.DoesNotExist:
        messages.error(request, 'Résultat introuvable.')
        return redirect('dashboard')

    context = {
        'prediction': prediction,
        'risk_percentage': prediction.get_risk_percentage(),
        'recommendation': prediction.get_recommendation(),
    }
    return render(request, 'detection/result.html', context)


@login_required(login_url='login')
def prediction_history(request):
    """Display user's prediction history"""
    predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'detection/history.html', {'predictions': predictions})


@login_required(login_url='login')
@require_http_methods(["POST"])
def delete_prediction(request, pk):
    """Delete a user's prediction"""
    try:
        if request.user.is_staff or request.user.is_superuser:
            prediction = Prediction.objects.get(pk=pk)
        else:
            prediction = Prediction.objects.get(pk=pk, user=request.user)
            
        prediction.delete()
        messages.success(request, 'Évaluation supprimée avec succès.')
    except Prediction.DoesNotExist:
        messages.error(request, "Résultat introuvable ou vous n'avez pas la permission de le supprimer.")

    next_url = request.POST.get('next', 'dashboard')
    return redirect(next_url)
