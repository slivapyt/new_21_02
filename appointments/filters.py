from django_filters import rest_framework as filters
from .models import Meeting
import datetime


class MeetingFilter(filters.FilterSet):
    class Meta:
        model = Meeting
        fields = ['title', 'creator']

    title = filters.CharFilter(lookup_expr='icontains')
    is_upcoming = filters.BooleanFilter(method='filter_upcoming')

    def filter_upcoming(self, queryset, name, value):
        if value:
            return queryset.filter(start_time__gt=datetime.datetime.now())

        return queryset
