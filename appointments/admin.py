from django.contrib import admin
from .models import Meeting, Booking
from django.contrib.auth import get_user_model


User = get_user_model()


class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    fields = ('user', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    inlines = (BookingInline,)
    list_display = (
        'title',
        'creator',
        'start_time',
        'end_time',
        'participants_count',
    )
    list_filter = ('start_time', 'creator')
    search_fields = ('title', 'creator__username')

    @admin.display(description='Участники', ordering='participants__count')
    def participants_count(self, obj):
        return obj.participants.count()


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('meeting_title', 'user', 'created_at')
    list_filter = ('created_at', 'meeting__title')
    search_fields = ('user__username', 'meeting__title')

    @admin.display(description='Встреча', ordering='meeting__title')
    def meeting_title(self, obj):
        return obj.meeting.title
