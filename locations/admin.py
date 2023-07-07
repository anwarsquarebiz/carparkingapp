from django.contrib import admin
from .models import ParkingSpot, Reservation, CustomUser
    
admin.site.register(CustomUser)

@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'parking_spot', 'hours', 'price')