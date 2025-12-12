from django.db.models.signals import post_save
from django.db.models import signals as django_signals
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        # Create notification for the receiver
        notification_content = f"You have a new message from {instance.sender.username}"
        
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            notification_type='message',
            content=notification_content
        )
        
        print(f"Notification created for {instance.receiver.username}: New message from {instance.sender.username}")


@receiver(post_save, sender=Message)
def log_message_creation(sender, instance, created, **kwargs):
    if created:
        print(f"[LOG] Message created: {instance.sender.username} -> {instance.receiver.username}")