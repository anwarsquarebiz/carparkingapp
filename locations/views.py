from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ParkingSpot, Reservation, CustomUser
import requests, json
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

import environ
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

def signup_view(request):
    # Check if user is aready logged in and then redirect
    if request.user.is_authenticated:
        return redirect('home')
        
    User = get_user_model()
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            error_message = 'Passwords do not match. Please try again.'
            return render(request, 'signup.html', {'error_message': error_message})
        
        if len(CustomUser.objects.filter(email = email)) > 0:
            error_message = 'Email id already used!'
            return render(request, 'signup.html', {'error_message': error_message})
        
        # Create a new user
        user = User(email=email, username=email)
        user.set_password(password1)
        user.save()

        # success message
        messages.success(request, 'Registration successful. Please log in.')  
        return redirect('login')  # Redirect to the login page after successful sign-up
    
    return render(request, 'signup.html')


def login_view(request):
    # Check if user is aready logged in and then redirect
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            # Handle invalid login credentials
            error_message = 'Invalid email or password. Please try again.'
            return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)

    return redirect('login')


# Home Page and Search Page
@login_required
def get_all_parking_spots(request):
    allParkingSpots = ParkingSpot.objects.all()
    show_results = []

    # If request method is post i.e. someone is searching for exact 
    # location then calculate the distance of the result as per set radius 
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        radius = request.POST.get('radius')
        
        for p in allParkingSpots:
            distance = calculate_distance(float(latitude), float(longitude), p.latitude, p.longitude)
            if distance <= int(radius):
                show_results.append(p)

    # If request method is not post then show all results 
    else:
        show_results = allParkingSpots
        
    context = {'show_results' : show_results}
    return render(request, 'index.html', context)

def calculate_distance(origin_latitude, origin_longitude, destination_latitude, destination_longitude):    
    api_key = env('GOOGLE_MAPS_API')  # Google Maps API key
    print(api_key)
    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin_latitude},{origin_longitude}&destination={destination_latitude},{destination_longitude}&key={api_key}'

    try:
        response = requests.get(url)
        response_json = response.json()

        if response_json['status'] == 'OK':
            distance_value = response_json['routes'][0]['legs'][0]['distance']['value']
            return distance_value
        else:
            raise Exception(response_json['error_message'])
    
    except requests.exceptions.RequestException as e:
        raise Exception(str(e))

@csrf_exempt
def reserve_parking_spot(request):
    if request.method == 'POST':
        try:
            # Implement the logic to find and reserve a parking spot based on the provided hours
            # Calculate the price and create a reservation record
            parkingspot_name = request.POST.get('parkingspot_name')
            user = request.user
            parking_spot = ParkingSpot.objects.filter(name = parkingspot_name).first()            
            hours = request.POST.get('hours')
            price =  int(hours) * int(parking_spot.price_per_hour)
            Reservation.objects.create(
                user = user,
                parking_spot = parking_spot,
                hours = hours,
                price = price
            )
            return redirect('home')        
        except user.DoesNotExist:            
            return JsonResponse({'status': 'error', 'message': 'User not found.'})        
    return JsonResponse({'status': 'error', 'message': 'Incorrect request method. Only post method is allowed'})

def view_reservations(request):
    show_results = Reservation.objects.all()
                
    context = {'show_results' : show_results}
    return render(request, 'reservations.html', context)