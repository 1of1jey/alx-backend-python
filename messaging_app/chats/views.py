from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import (
    IsParticipantOfConversation,
    CanCreateConversation,
    CanSendMessage
)


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, CanCreateConversation]
    
    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'messages', 'add_participant']:
            permission_classes = [IsAuthenticated, IsParticipantOfConversation]
        else:
            permission_classes = [IsAuthenticated, CanCreateConversation]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user
        ).distinct().order_by('-created_at')
    
    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        messages = conversation.messages.all().order_by('sent_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {"error": "user_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(id=user_id)
            conversation.participants.add(user)
            return Response(
                {"message": f"User {user.username} added to conversation"},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, CanSendMessage]
    
    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'mark_as_read']:
            permission_classes = [IsAuthenticated, IsParticipantOfConversation]
        else:
            permission_classes = [IsAuthenticated, CanSendMessage]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = Message.objects.all()
        conversation_id = self.request.query_params.get('conversation_id')
        
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        else:
            # Only show messages from conversations the user is part of
            queryset = queryset.filter(
                conversation__participants=self.request.user
            )
        
        return queryset.order_by('-sent_at')
    
    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation_id')
        
        if not conversation_id:
            raise serializers.ValidationError(
                {"conversation_id": "This field is required"}
            )
        
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        # Check if user is a participant in the conversation
        if not conversation.participants.filter(id=self.request.user.id).exists():
            raise PermissionDenied(
                "You must be a participant in this conversation to send messages"
            )
        
        serializer.save(
            sender=self.request.user,
            conversation=conversation
        )
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        unread_messages = self.get_queryset().filter(
            is_read=False
        ).exclude(sender=request.user)
        
        serializer = self.get_serializer(unread_messages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        # Assuming you have an 'is_read' field
        message.is_read = True
        message.save()
        
        return Response(
            {"message": "Message marked as read"},
            status=status.HTTP_200_OK
        )
