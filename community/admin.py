from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    summernote_fields = ("description",)
    list_display = ("title", "contact_person", "order")
    list_editable = ("order",)
