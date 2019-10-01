from django.contrib import admin
from app.models import CodeReference, Customer
from django.http import HttpResponse
from django import forms
import csv


class CustomerExportAdmin(admin.ModelAdmin):
    def admin_action(self, request, queryset):
        actions = ["export_as_csv"]


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = csv.reader(csv_file)

            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("customer_code", "customer_first_name", "customer_last_name", "delivery_address", "status_code")
    list_filter = ("status_code", "delivery_address",)
    actions = ["export_as_csv"]

@admin.register(CodeReference)
class CustomerAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("status_code", "status_description")