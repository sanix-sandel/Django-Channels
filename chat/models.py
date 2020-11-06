from django.db import models
from django.conf import settings
import uuid

class Conversation(models.Model):
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    users=models.ManyToManyField(settings.AUTH_USER_MODEL,
                                related_name='conversation',
                                blank=True)    
    code=models.CharField(max_length=255, blank=True, null=True)    

    def __str__(self):
        return f"{self.code}"

class Message(models.Model):
    id=models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
    )
    content=models.TextField()
    author=models.ForeignKey(settings.AUTH_USER_MODEL, 
        related_name='messages', on_delete=models.CASCADE)
    conversation=models.ForeignKey(Conversation, related_name='message',
     on_delete=models.CASCADE)     
     
    sent_on=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('sent_on',)

    def __str__(self):
        return f"message from {self.author.username}"