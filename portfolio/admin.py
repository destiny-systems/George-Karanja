from django.contrib import admin
from .models import Property, UnitType, RoomImage, Floor, GalleryImage, LocationAdvantage, PortfolioOwner, Enquiry, Payment


class UnitTypeInline(admin.TabularInline):
    model = UnitType
    extra = 1


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'location_name', 'starting_price']
    inlines = [UnitTypeInline, GalleryImageInline]


@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ['unit_type', 'room_type', 'order']
    list_filter = ['room_type', 'unit_type']


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ['property', 'floor_number', 'unit_label', 'unit_type', 'price', 'is_available']
    list_filter = ['property', 'is_available']


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'property', 'email', 'phone', 'created_at', 'is_contacted']
    list_filter = ['property', 'is_contacted']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['floor', 'customer_email', 'amount', 'status', 'created_at']
    list_filter = ['status']


@admin.register(LocationAdvantage)
class LocationAdvantageAdmin(admin.ModelAdmin):
    list_display = ['property', 'category', 'order']
    list_filter = ['property', 'category']


@admin.register(PortfolioOwner)
class PortfolioOwnerAdmin(admin.ModelAdmin):
    list_display = ['name']
