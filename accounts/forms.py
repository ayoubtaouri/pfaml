from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password (min. 8 characters)'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'username', 'password1', 'password2')
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        # Commented out to allow passwords like "azerty123"
        # if not any(char.isupper() for char in password):
        #     raise forms.ValidationError('Password must contain at least one uppercase letter.')
        # if not any(char.isdigit() for char in password):
        #     raise forms.ValidationError('Password must contain at least one digit.')
        # if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?' for char in password):
        #     raise forms.ValidationError('Password must contain at least one special character.')
        return password
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered.')
        return email


class CustomAuthenticationForm(AuthenticationForm):
    """Form for user login"""
    username = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    


INPUT_CLASS = 'vitalis-input w-full bg-surface-container-lowest border border-outline-variant text-on-surface rounded-DEFAULT focus:ring-2 focus:ring-primary focus:border-primary transition-colors py-2 px-3'


class ProfileUpdateForm(forms.ModelForm):
    """Form to update user profile info (name, email)"""

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Nom'}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': "Nom d'utilisateur"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Cet email est déjà utilisé par un autre compte.')
        return email


class PasswordChangeCustomForm(PasswordChangeForm):
    """Styled password change form"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': INPUT_CLASS})
        self.fields['old_password'].widget.attrs['placeholder'] = 'Mot de passe actuel'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Nouveau mot de passe'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirmer le nouveau mot de passe'
