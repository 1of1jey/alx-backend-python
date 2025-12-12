from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="User who sent the message"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        help_text="User who receives the message"
    )
    content = models.TextField(help_text="Message content")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="When the message was created")
    is_read = models.BooleanField(default=False, help_text="Whether the message has been read")

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['receiver', '-timestamp']),
            models.Index(fields=['sender', '-timestamp']),
        ]

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('message', 'New Message'),
        ('system', 'System Notification'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="User who receives the notification"
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
        help_text="Related message (if applicable)"
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='message',
        help_text="Type of notification"
    )
    content = models.TextField(help_text="Notification content/message")
    is_read = models.BooleanField(default=False, help_text="Whether the notification has been read")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="When the notification was created")

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['user', 'is_read']),
        ]

    def __str__(self):
        return f"Notification for {self.user.username}: {self.content[:50]}"

    def mark_as_read(self):
        self.is_read = True
        self.save(update_fields=['is_read'])
