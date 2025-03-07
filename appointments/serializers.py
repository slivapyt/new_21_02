from appointments.models import Booking, Meeting
from rest_framework import serializers
from appointments.validators import MeetingValidator, BookingValidator


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'
        read_only_fields = ('creator',)

    def validate(self, data):
        MeetingValidator.meeting_time_validate(
            data['start_time'], data['end_time'])
        return data


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('created_at',)

    def validate(self, data):
        meeting = data['meeting']
        user = data['user']

        MeetingValidator.validate_max_participants(
            meeting)

        MeetingValidator.validate_no_double_booking(
            user, meeting)

        MeetingValidator.validate_no_time_overlap(
            user, meeting.start_time, meeting.end_time)

        BookingValidator.validate_booking_time(
            meeting, data['start_time'], data['end_time'])

        return data
