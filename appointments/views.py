from rest_framework import viewsets, permissions
from .models import Meeting, Booking
from .serializers import MeetingSerializer, BookingSerializer
from .permissions import IsCreatorOrReadOnly
from .filters import MeetingFilter
from django_filters.rest_framework import DjangoFilterBackend


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]
    filterset_class = MeetingFilter
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
