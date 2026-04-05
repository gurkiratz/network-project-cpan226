from django.db import models
from django.contrib.auth.models import User


class SentEmail(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emails')
    to = models.TextField()
    cc = models.TextField(blank=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} → {self.to} ({self.sent_at:%Y-%m-%d %H:%M})"

    class Meta:
        ordering = ['-sent_at']
