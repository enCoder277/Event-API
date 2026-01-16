import django_filters
from .models import Event

class EventFilter(django_filters.FilterSet):
    date_from = django_filters.IsoDateTimeFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.IsoDateTimeFilter(field_name='date', lookup_expr='lte')

    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')

    # фильтр по организатору (по username)
    organizer = django_filters.CharFilter(field_name='organizer__username', lookup_expr='iexact')

    class Meta:
        model = Event
        fields = [
            'location',
            'organizer',
        ]
