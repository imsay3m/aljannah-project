from django.contrib import admin
from .models import NewsPost, Event, Announcement


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    summernote_fields = ("content",)
    list_display = ("title", "date", "is_published")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "start_time", "location")
    list_filter = ("date",)
    # This allows the admin to see the slug generated as they type,
    # but the model save() method handles it if they leave it empty.
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_active")
    list_filter = ("is_active", "created_at")
    list_editable = ("is_active",)  # Quick toggle switch in list view
    search_fields = ("title", "content")
