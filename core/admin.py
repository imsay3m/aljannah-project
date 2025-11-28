from django.contrib import admin
from .models import (
    SiteConfiguration,
    Service,
    Testimonial,
    PageContent,
    StaffMember,
    GalleryAlbum,
    GalleryImage,
    ContactSubmission,
)


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    # Prevent creating more than one configuration
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    summernote_fields = ("content",)
    list_display = ("section_name", "page", "title")
    list_filter = ("page",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("parent_name", "is_active")


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order")
    list_editable = ("order",)


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 3


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]
    list_display = ("title", "created_at")


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "submitted_at")
    readonly_fields = ("submitted_at",)
