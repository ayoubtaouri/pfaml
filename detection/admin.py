from django.contrib import admin
from detection.models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'blood_glucose_level', 'risk_level', 'risk_score', 'created_at')
    list_filter = ('risk_level', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'risk_score', 'risk_level')
    
    fieldsets = (
        ('Utilisateur', {'fields': ('user',)}),
        ('Données Médicales', {'fields': (
            'gender', 'age', 'hypertension', 'heart_disease',
            'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level'
        )}),
        ('Résultat', {'fields': ('risk_score', 'risk_level')}),
        ('Métadonnées', {'fields': ('created_at', 'updated_at')}),
    )
