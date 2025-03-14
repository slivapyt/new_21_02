from django.utils import timezone
from rest_framework.exceptions import ValidationError
from .models import Booking, Meeting


class MeetingValidator:

    @staticmethod
    def validate_meeting_time(start_time, end_time):
        if start_time < timezone.now():
            raise ValidationError('Время начала должно быть в будущем')

        if start_time >= end_time:
            raise ValidationError('Время окончания должно быть позже начала')

    @staticmethod
    def validate_max_participants(meeting: Meeting):
        current_participants = meeting.bookings.count()
        if current_participants > meeting.max_participants:
            raise ValidationError('Встреча заполнена')

    @staticmethod
    def validate_no_double_booking(user, meeting):
        if Booking.objects.filter(user=user, meeting=meeting).exists():
            raise ValidationError('Вы уже забронировали это место')

    @staticmethod
    def validate_no_time_overlap(user, start_time, end_time):
        overlapping = Booking.objects.filter(
            user=user,
            meeting__start_time__lt=end_time,
            meeting__end_time__gt=start_time,
        ).exists()

        if overlapping:
            raise ValidationError('У вас уже есть встреча в это время')
