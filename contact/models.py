from django.db import models


class ContactMessage(models.Model):
    """Model to store contact form messages"""
    
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('technical', 'Technical Support'),
        ('feedback', 'Feedback'),
        ('other', 'Other'),
    ]
    
    sender_name = models.CharField(max_length=150)
    sender_email = models.EmailField()
    subject = models.CharField(
        max_length=100,
        choices=SUBJECT_CHOICES,
        default='general'
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_read']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender_name} ({self.sender_email}) - {self.get_subject_display()}"
    
    def mark_as_read(self):
        """Mark message as read"""
        self.is_read = True
        self.save()
