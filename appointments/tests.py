from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Meeting, Booking
from .validators import MeetingValidator
from rest_framework.exceptions import ValidationError


User = get_user_model()


class BaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass1',
            email='testuser1@example.com',
        )
        cls.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass2',
            email='testuser2@example.com',
        )
        cls.meeting = cls.create_meeting()

    @classmethod
    def create_meeting(cls, **kwargs):
        defaults = {
            'title': 'Test Meeting',
            'start_time': timezone.now() + timezone.timedelta(hours=1),
            'end_time': timezone.now() + timezone.timedelta(hours=2),
            'creator': cls.user1,
        }
        defaults.update(kwargs)
        return Meeting.objects.create(**defaults)

    @classmethod
    def create_booking(cls, **kwargs):
        defaults = {
            'meeting': cls.meeting,
            'user': cls.user1,
        }
        defaults.update(kwargs)
        return Booking.objects.create(**defaults)


class ModelTests(BaseTest):
    def test_meeting_creation(self):
        self.assertEqual(str(self.meeting), 'Test Meeting')

    def test_booking_creation(self):
        booking = Booking.objects.create(
            meeting=self.meeting,
            user=self.user2,
        )
        self.assertEqual(str(booking), 'testuser2 - Test Meeting')


class ValidatorsTest(BaseTest):
    def test_validate_meeting_time_start_in_past(self):
        past_time = timezone.now() - timedelta(hours=1)
        with self.assertRaisesMessage(ValidationError,
                                      'Время начала должно быть в будущем'):
            MeetingValidator.validate_meeting_time(past_time, timezone.now())

    def test_validate_max_participants_limit_is_enforced_correctly(self):
        meeting = self.create_meeting(max_participants=1)
        Booking.objects.create(user=self.user1, meeting=meeting)
        MeetingValidator.validate_max_participants(meeting)

    def test_validate_max_participants_limit_is_exceeded(self):
        meeting = self.create_meeting(max_participants=1)
        Booking.objects.create(user=self.user1, meeting=meeting)
        Booking.objects.create(user=self.user2, meeting=meeting)

        with self.assertRaisesMessage(ValidationError, 'Встреча заполнена'):
            MeetingValidator.validate_max_participants(meeting)

    def test_validate_time_overlap(self):
        Booking.objects.create(meeting=self.meeting, user=self.user1)

        overlapping_start = self.meeting.start_time + timedelta(minutes=30)
        overlapping_end = self.meeting.end_time + timedelta(hours=1)

        with self.assertRaisesMessage(ValidationError,
                                      'У вас уже есть встреча в это время'):
            MeetingValidator.validate_no_time_overlap(
                user=self.user1,
                start_time=overlapping_start,
                end_time=overlapping_end,
            )

    def test_validate_time_non_overlap(self):
        Booking.objects.create(meeting=self.meeting, user=self.user1)

        new_start = self.meeting.end_time
        new_end = new_start + timedelta(hours=1)
        MeetingValidator.validate_no_time_overlap(
            user=self.user1,
            start_time=new_start,
            end_time=new_end,
            )

        new_start = self.meeting.start_time - timedelta(hours=1)
        new_end = self.meeting.start_time
        MeetingValidator.validate_no_time_overlap(
            user=self.user1,
            start_time=new_start,
            end_time=new_end,
            )
