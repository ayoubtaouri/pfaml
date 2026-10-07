from django import forms
from detection.models import Prediction


class PredictionForm(forms.ModelForm):
    """Form for diabetes risk prediction - 8 features"""
    
    class Meta:
        model = Prediction
        fields = [
            'gender', 'age', 'hypertension', 'heart_disease',
            'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level'
        ]
        widgets = {
            'gender': forms.Select(attrs={'class': 'vitalis-input w-full bg-surface-container-lowest border border-outline-variant text-on-surface rounded-DEFAULT focus:ring-2 focus:ring-primary focus:border-primary transition-colors py-2 px-3'}),
            'age': forms.NumberInput(attrs={
                'class': 'vitalis-input w-full bg-surface-container-lowest border border-outline-variant text-on-surface rounded-DEFAULT focus:ring-2 focus:ring-primary focus:border-primary transition-colors py-2 px-3 placeholder-text-secondary',
                'placeholder': 'ex., 45',
                'min': '0', 'max': '120', 'step': '1'
            }),
            'hypertension': forms.Select(attrs={'class': 'vitalis-input w-full bg-surface-container-lowest border border-outline-variant text-on-surface rounded-DEFAULT focus:ring-2 focus:ring-primary focus:border-primary transition-colors py-2 px-3'}),
            'heart_disease': forms.Select(attrs={'class': 'vitalis-input w-full bg-surface-container-lowest border border-outline-variant text-on-surface rounded-DEFAULT focus:ring-2 focus:ring-primary focus:border-primary transition-colors py-2 px-3'}),
            'smoking_history': forms.Select(attrs={'class': 'vitalis-input w-full bg-surface-container-lowest border border-outline-variant text-on-surface rounded-DEFAULT focus:ring-2 focus:ring-primary focus:border-primary transition-colors py-2 px-3'}),
            'bmi': forms.NumberInput(attrs={
                'class': 'vitalis-input w-full bg-surface-container-lowest border border-outline-variant text-on-surface rounded-DEFAULT focus:ring-2 focus:ring-primary focus:border-primary transition-colors py-2 px-3 placeholder-text-secondary',
                'placeholder': 'ex., 25.4',
                'min': '10', 'max': '100', 'step': '0.1'
            }),
            'HbA1c_level': forms.NumberInput(attrs={
                'class': 'vitalis-input w-full bg-surface-container-lowest border border-outline-variant text-on-surface rounded-DEFAULT focus:ring-2 focus:ring-primary focus:border-primary transition-colors py-2 px-3 placeholder-text-secondary',
                'placeholder': 'ex., 6.5',
                'min': '3.0', 'max': '15.0', 'step': '0.1'
            }),
            'blood_glucose_level': forms.NumberInput(attrs={
                'class': 'vitalis-input w-full bg-surface-container-lowest border border-outline-variant text-on-surface rounded-DEFAULT focus:ring-2 focus:ring-primary focus:border-primary transition-colors py-2 px-3 placeholder-text-secondary',
                'placeholder': 'ex., 120',
                'min': '50', 'max': '500', 'step': '1'
            }),
        }
