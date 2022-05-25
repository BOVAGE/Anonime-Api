from email import message
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Message(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    message_text = models.CharField(max_length=256)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message_text