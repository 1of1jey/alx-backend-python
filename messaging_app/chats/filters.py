import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    conversation = django_filters.UUIDFilter(field_name='conversation__conversation_id')
    sender = django_filters.UUIDFilter(field_name='sender__user_id')
    sent_at_min = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_at_max = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'sent_at_min', 'sent_at_max']
