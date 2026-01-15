from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Event, EventRegistration

User = get_user_model()

class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source='organizer.username')

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'organizer', 'created_at', 'updated_at',]


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location',]


class EventRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    event = serializers.ReadOnlyField(source='event.id')

    class Meta:
        model = EventRegistration
        fields = ['id', 'user', 'event', 'registered_at',]


class EventRegistrationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = []

    def validate(self, attrs):
        user = self.context['request'].user
        event = self.context['event']  #<-------- передать во вьюхе руками!!!

        if EventRegistration.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError('You are already registered for this event.')

        return attrs
