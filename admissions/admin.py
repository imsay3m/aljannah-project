
from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import AdmissionCost, ApplicationSubmission

@admin.register(AdmissionCost)
class AdmissionCostAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "order")
    list_editable = ("order",)

@admin.register(ApplicationSubmission)
class ApplicationSubmissionAdmin(admin.ModelAdmin):
    list_display = ("child_first_name", "parent_name", "phone", "submitted_at", "is_reviewed")
    list_filter = ("submitted_at", "is_reviewed")
    search_fields = ("child_first_name", "parent_name", "email")
    readonly_fields = ("submitted_at",)
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        """
        Custom admin action to download selected applications as a CSV file.
        """
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response
    
    export_as_csv.short_description = "Export Selected to CSV"