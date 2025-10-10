from django.db import models

# Create your models here.
class TgUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username or self.first_name or self.telegram_id}"
    
class Message(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg from {self.user} at {self.created_at}"