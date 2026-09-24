from django.contrib import admin

from .models import Advantage, PickupRequest, Service, ServiceArea, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "province", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("province",)


@admin.register(Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)


@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "company", "phone", "pickup_location", "delivery_location", "needed_by", "status")
    list_filter = ("status", "service", "created_at")
    list_editable = ("status",)
    search_fields = ("name", "company", "phone", "email", "pickup_location", "delivery_location", "load_details")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Customer", {"fields": ("name", "company", "phone", "email")}),
        ("Shipment", {"fields": ("service", "pickup_location", "delivery_location", "needed_by", "load_details")}),
        ("Dispatch", {"fields": ("status", "internal_notes", "created_at")}),
    )
