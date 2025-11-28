from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from urllib.parse import urlencode
from django_ckeditor_5.fields import CKEditor5Field
import datetime


class Announcement(models.Model):
    """
    Top bar notifications (e.g., School Closures, Urgent Notices).
    """

    title = models.CharField(max_length=200, help_text="e.g., 'Notice' or 'Urgent'")
    content = models.TextField(
        help_text="Keep this short (1-2 sentences) for the top bar."
    )
    is_active = models.BooleanField(default=True, verbose_name="Published")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class NewsPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    date = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to="news/")
    content = CKEditor5Field("Content", config_name="extends")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200)
    # Slug is blank=True so it is optional in Admin, auto-filled on save
    slug = models.SlugField(unique=True, blank=True, max_length=200)

    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    location = models.CharField(max_length=200, default="Al Jannah Academy")
    description = CKEditor5Field("Description", config_name="default", blank=True)

    class Meta:
        ordering = ["date", "start_time"]

    # AUTO-SLUG LOGIC
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.date}"

    @property
    def google_calendar_url(self):
        """
        Generates a link to add event to Google Calendar.
        """
        params = {
            'action': 'TEMPLATE',
            'text': self.title,
            'details': self.description,
            'location': self.location,
        }

        fmt_time = "%Y%m%dT%H%M%S"
        fmt_date = "%Y%m%d"

        if self.start_time and self.end_time:
            start_dt = datetime.datetime.combine(self.date, self.start_time)
            end_dt = datetime.datetime.combine(self.date, self.end_time)
            dates = f"{start_dt.strftime(fmt_time)}/{end_dt.strftime(fmt_time)}"
        else:
            next_day = self.date + datetime.timedelta(days=1)
            dates = f"{self.date.strftime(fmt_date)}/{next_day.strftime(fmt_date)}"

        params['dates'] = dates
        return f"https://calendar.google.com/calendar/render?{urlencode(params)}"
