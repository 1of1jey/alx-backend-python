from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class MessageSignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username='sender_user',
            email='sender@example.com',
            password='testpass123'
        )
        self.receiver = User.objects.create_user(
            username='receiver_user',
            email='receiver@example.com',
            password='testpass123'
        )

    def test_notification_created_on_message_creation(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello, this is a test message!"
        )

        notifications = Notification.objects.filter(user=self.receiver, message=message)
        self.assertEqual(notifications.count(), 1)

        notification = notifications.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertEqual(notification.notification_type, 'message')
        self.assertIn(self.sender.username, notification.content)
        self.assertFalse(notification.is_read)

    def test_notification_not_created_on_message_update(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original content"
        )

        initial_count = Notification.objects.filter(user=self.receiver).count()

        # Update the message
        message.content = "Updated content"
        message.save()

        final_count = Notification.objects.filter(user=self.receiver).count()
        self.assertEqual(initial_count, final_count)

    def test_multiple_messages_create_multiple_notifications(self):
        num_messages = 5
        for i in range(num_messages):
            Message.objects.create(
                sender=self.sender,
                receiver=self.receiver,
                content=f"Message number {i+1}"
            )
        notifications = Notification.objects.filter(user=self.receiver)
        self.assertEqual(notifications.count(), num_messages)

    def test_notification_content_includes_sender_username(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message content"
        )

        notification = Notification.objects.get(user=self.receiver, message=message)
        self.assertIn(self.sender.username, notification.content)
        self.assertIn("new message", notification.content.lower())

    def test_notification_only_for_receiver(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message"
        )

        # Check receiver has notification
        receiver_notifications = Notification.objects.filter(user=self.receiver)
        self.assertEqual(receiver_notifications.count(), 1)

        # Check sender does not have notification for sending the message
        sender_notifications = Notification.objects.filter(user=self.sender, message=message)
        self.assertEqual(sender_notifications.count(), 0)

    def test_mark_notification_as_read(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message"
        )

        notification = Notification.objects.get(user=self.receiver, message=message)
        self.assertFalse(notification.is_read)

        # Mark as read
        notification.mark_as_read()
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)


class MessageModelTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

    def test_message_creation(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        self.assertIsNotNone(message.id)
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        self.assertFalse(message.is_read)

    def test_message_str_representation(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test"
        )
        str_repr = str(message)
        self.assertIn(self.user1.username, str_repr)
        self.assertIn(self.user2.username, str_repr)

    def test_message_ordering(self):
        msg1 = Message.objects.create(sender=self.user1, receiver=self.user2, content="First")
        msg2 = Message.objects.create(sender=self.user1, receiver=self.user2, content="Second")
        
        messages = Message.objects.all()
        self.assertEqual(messages[0], msg2)
        self.assertEqual(messages[1], msg1)


class NotificationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')

    def test_notification_creation(self):
        notification = Notification.objects.create(
            user=self.user,
            notification_type='system',
            content="System notification"
        )
        self.assertIsNotNone(notification.id)
        self.assertEqual(notification.user, self.user)
        self.assertFalse(notification.is_read)

    def test_notification_str_representation(self):
        notification = Notification.objects.create(
            user=self.user,
            content="Test notification"
        )
        str_repr = str(notification)
        self.assertIn(self.user.username, str_repr)
        self.assertIn("Test notification", str_repr)