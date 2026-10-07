from django import forms
from contact.models import ContactMessage


class ContactForm(forms.ModelForm):
    """Form for contact messages"""
    
    class Meta:
        model = ContactMessage
        fields = ['sender_name', 'sender_email', 'subject', 'message']
        widgets = {
            'sender_name': forms.TextInput(attrs={
                'class': 'vitalis-input w-full bg-surface-container-lowest border border-outline-variant text-on-surface rounded-DEFAULT focus:ring-2 focus:ring-primary focus:border-primary transition-colors py-2 px-3',
                'placeholder': 'Your name'
            }),
            'sender_email': forms.EmailInput(attrs={
                'class': 'vitalis-input w-full bg-surface-container-lowest border border-outline-variant text-on-surface rounded-DEFAULT focus:ring-2 focus:ring-primary focus:border-primary transition-colors py-2 px-3',
                'placeholder': 'Your email address'
            }),
            'subject': forms.Select(attrs={
                'class': 'vitalis-input w-full bg-surface-container-lowest border border-outline-variant text-on-surface rounded-DEFAULT focus:ring-2 focus:ring-primary focus:border-primary transition-colors py-2 px-3'
            }),
            'message': forms.Textarea(attrs={
                'class': 'vitalis-input w-full bg-surface-container-lowest border border-outline-variant text-on-surface rounded-DEFAULT focus:ring-2 focus:ring-primary focus:border-primary transition-colors py-2 px-3',
                'placeholder': 'Your message',
                'rows': 6
            }),
        }
    
    # Honeypot field for anti-spam
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label='Leave this field empty'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        honeypot = cleaned_data.get('honeypot')
        
        if honeypot:
            raise forms.ValidationError('Invalid submission detected.')
        
        return cleaned_data
