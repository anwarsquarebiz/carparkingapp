from django.urls import path
from . import views

urlpatterns = [
    # Authentication urls
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Car Parking app urls
    # Homepage, Shows All Parking and Search results
    path('', views.get_all_parking_spots, name='home'),

    # POST url to reserve the parking 
    path('reserve/', views.reserve_parking_spot, name='reserve_parking_spot'),
    
    # Shows all reserved parkings
    path('reservations/', views.view_reservations, name='view_reservations'),
]