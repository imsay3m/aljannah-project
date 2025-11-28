from django.contrib import admin
from .models import Policy, DailySchedule, Level, Book, PurchaseLink,BookOrder

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(DailySchedule)
class DailyScheduleAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'activity', 'order')
    list_editable = ('order',)


@admin.register(BookOrder)
class BookOrderAdmin(admin.ModelAdmin):
    list_display = (
        "student_name",
        "student_class",
        "parent_name",
        "reason",
        "submitted_at",
        "is_processed",
    )
    list_filter = ("student_class", "reason", "is_processed")
    search_fields = ("student_name", "parent_name", "parent_email")
    list_editable = ("is_processed",)


class PurchaseLinkInline(admin.TabularInline):
    model = PurchaseLink
    extra = 1

class BookInline(admin.TabularInline):
    model = Book
    extra = 1

# CHANGED: Registered Level instead of Subject
@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    inlines = [BookInline]
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [PurchaseLinkInline]
    # Added 'price' to list display
    list_display = ("title", "level", "price", "author")
    list_filter = ("level",)
