from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Prediction(models.Model):
    """Model to store user diabetes risk predictions"""
    RISK_LEVEL_CHOICES = [
        ('LOW', 'Faible'),
        ('MEDIUM', 'Modéré'),
        ('HIGH', 'Élevé'),
    ]
    
    GENDER_CHOICES = [
        (0, 'Féminin'),
        (1, 'Masculin'),
        (2, 'Autre'),
    ]

    SMOKING_CHOICES = [
        (0, 'Aucune information'),
        (1, 'Fumeur actuel'),
        (2, 'A déjà fumé'),
        (3, 'Ancien fumeur'),
        (4, 'Jamais fumé'),
        (5, 'Plus fumeur'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='predictions'
    )
    
    # Input features matching XGBoost model (8 features)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0)
    age = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(120.0)])
    hypertension = models.IntegerField(choices=[(0, 'Non'), (1, 'Oui')], default=0)
    heart_disease = models.IntegerField(choices=[(0, 'Non'), (1, 'Oui')], default=0)
    smoking_history = models.IntegerField(choices=SMOKING_CHOICES, default=0)
    bmi = models.FloatField(validators=[MinValueValidator(10.0), MaxValueValidator(100.0)])
    HbA1c_level = models.FloatField(validators=[MinValueValidator(3.0), MaxValueValidator(15.0)], default=5.0)
    blood_glucose_level = models.FloatField(validators=[MinValueValidator(50.0), MaxValueValidator(500.0)], default=100.0)
    
    # Output
    risk_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    risk_level = models.CharField(
        max_length=10,
        choices=RISK_LEVEL_CHOICES
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Prédiction'
        verbose_name_plural = 'Prédictions'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['risk_level']),
        ]
    
    def __str__(self):
        return f"Prédiction pour {self.user.email} - {self.get_risk_level_display()} ({self.risk_score:.2%})"
    
    def get_risk_percentage(self):
        """Return risk score as percentage"""
        return round(self.risk_score * 100, 2)
    
    def get_recommendation(self):
        """Return medical recommendation based on risk level"""
        recommendations = {
            'LOW': 'Continuez à maintenir un mode de vie sain et faites des bilans réguliers.',
            'MEDIUM': 'Consultez un professionnel de santé pour un suivi régulier.',
            'HIGH': 'Consultez un professionnel de santé rapidement.',
        }
        return recommendations.get(self.risk_level, '')
