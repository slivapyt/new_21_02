from django.utils import timezone
from rest_framework.exceptions import ValidationError
from .models import Booking, Meeting


class MeetingValidator:

    @staticmethod
    def meeting_time_validate(start_time, end_time):
        if start_time >= end_time:
            raise ValidationError('Время окончания должно быть позже начала')

        if start_time < timezone.now():
            raise ValidationError('Время начала должно быть в будущем')

    @staticmethod
    def max_participants_validate(meeting: Meeting):
        current_participants = meeting.booking.count()
        if current_participants >= meeting.max_participants:
            raise ValidationError('Встреча заполнена')

    @staticmethod
    def no_double_booking_validate(user, meeting):
        if Booking.objects.filter(user=user, meeting=meeting).exists():
            raise ValidationError('Вы уже забронировали это место')

    @staticmethod
    def no_time_overlap_validate(user, start_time, end_time):
        overlapping = Booking.objects.filter(
            user=user,
            meeting_start_time__lte=end_time,
            meeting_end_time__gte=start_time,
        ).exists()
        if overlapping.exists():
            raise ValidationError('У вас уже есть встреча в это время')


class BookingValidator:

    @staticmethod
    def booking_time_validate(meeting, booking_start, booking_end):
        if booking_start < meeting.start_time or booking_end > meeting.end_time: # noqa
            raise ValidationError('Время бронирования должно быть в пределах времени встречи') # noqa
