from django.db import models
from django.contrib.auth import get_user_model
from users.models import optional_field
User = get_user_model()


class Meeting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TimeField(**optional_field)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_participants = models.PositiveIntegerField(default=10)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_meetings')
    participants = models.ManyToManyField(
        User, related_name='meetings', blank=True)

    def __ster__(self):
        return self.title


class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    meeting = models.ForeignKey(
        Meeting, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings')

    def __str__(self):
        return f'{self.user.username} - {self.meeting.title}'
