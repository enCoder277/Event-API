from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters

from .models import Event, EventRegistration
from .serializers import (EventSerializer, EventCreateUpdateSerializer, EventRegistrationSerializer, EventRegistrationCreateSerializer,)
from .permissions import IsOrganizerOrReadOnly
from .filters import EventFilter


User = get_user_model()

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-date')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    serializer_class = EventSerializer

    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = EventFilter
    search_fields = ['title', 'description', 'location', 'organizer__username']
    ordering_fields = ['date', 'created_at', 'title']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return EventCreateUpdateSerializer
        return EventSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()
        serializer = EventRegistrationCreateSerializer(
            data=request.data,
            context={'request': request, 'event': event}
        )
        serializer.is_valid(raise_exception=True)

        registration, created = EventRegistration.objects.get_or_create(
            user=request.user,
            event=event
        )
        if not created:
            return Response(
                {'detail': 'You are already registered for this event.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        out = EventRegistrationSerializer(registration)
        return Response(out.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def unregister(self, request, pk=None):
        event = self.get_object()
        registration = EventRegistration.objects.filter(user=request.user, event=event).first()
        if not registration:
            return Response({'detail': 'Registration not found.'}, status=status.HTTP_404_NOT_FOUND)
        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_registrations(self, request):
        regs = EventRegistration.objects.filter(user=request.user).select_related('event')
        serializer = EventRegistrationSerializer(regs, many=True)
        return Response(serializer.data)


from rest_framework import serializers

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
