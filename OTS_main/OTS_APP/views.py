from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

# Home page view
def home(request):
    current_user = request.user
    context = {
        'user': current_user,
    } 
    return render(request, "home.html", context)

def login_view(request):
     # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        
        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
        
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect('/')
        
    current_user = request.user
    context = {
        'user': current_user,
    }
    # Render the login page template (GET request)
    return render(request, 'login.html', context)

def register(request):
      # Check if the HTTP request method is POST (form submission)
      
    if request.method == 'POST':
        # Get form data
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        age = request.POST.get('age')
        user_type = request.POST.get('user_type')
        
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register/')
        
        try:
            # Create a new User object with the provided information
            if user_type == "user":
                new_user = User.objects.create_user(
                                username=username,
                                email=email,
                                password=password,
                                age=age,
                                first_name=f_name,
                                last_name=l_name,
                                user_type=user_type
                            )
            elif user_type == "manager":
                new_user = Manager.objects.create_superuser(
                                username=username,
                                email=email,
                                password=password,
                                age=age,
                                first_name=f_name,
                                last_name=l_name,
                                total_tickets_sold=0,
                                num_current_events=0,
                                num_past_events=0,
                                total_income=0.0,
                                user_type=user_type
                            )
            else:
                    raise ValueError("Invalid user type")
        except Exception as e:
            messages.error(request, f'An error occurred during registration: {str(e)}')
            return render(request, 'register.html')
               
        
        # Set the user's password and save the user object
        new_user.set_password(password)
        new_user.save()
        
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('/login/')
    
    current_user = request.user
    context = {
        'user': current_user,
    }
    # Render the registration page template (GET request)
    return render(request, 'register.html', context)


def logout_view(request):
    current_user = request.user
    context = {
        'user': current_user,
    }
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return render(request, 'logout.html', context)


@login_required(login_url='login')
def upcoming(request):
    if request.method == "POST":
        user = request.user
        event_id = request.POST.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        action_type = request.POST.get('action_type')
        
        # --- BOOK EVENT ---
        if action_type == "book_event":
            seats = 1
            if seats > event.available_seats:
                messages.error(request, "Not enough seats available.")
                return redirect("upcoming")
            
             # Create the booking
             
            Booking.objects.create(
            user=user,
            event=event,
            seats_booked=seats
            )
            
            Event.objects.filter(id=event.id).update(  
                available_seats=event.available_seats - seats
            )
            
             # Success message
            messages.success(request, f"Successfully booked {seats} seat(s) for {event.event_title}!")
  
            return redirect("upcoming")
        
        if action_type == "cancel_event":
            # Cancel booking
            booking = Booking.objects.filter(user=user, event=event).first()
            if booking:
                booking.delete()
                messages.success(request, f"Successfully canceled booking for {event.event_title}.")
                Event.objects.filter(id=event.id).update(  
                available_seats=event.available_seats + 1
                )
            else:
                messages.error(request, "No booking found to cancel.")
            return redirect("upcoming")
            
        
    current_user = request.user
    events = Event.objects.all().order_by('event_date').order_by('event_time')
    bookings = Booking.objects.filter(user=request.user)
    booking_ids = bookings.values_list('event_id', flat=True)
    context = {
        'user': current_user,
        'events': events,
        'booking_ids': booking_ids
    }
    
    return render(request, "upcoming.html", context)

@login_required(login_url='login')
def current(request):
    
    if request.method == "POST":
        user = request.user
        event_id = request.POST.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        action_type = request.POST.get('action_type')
        
        if action_type == "cancel_event":
            # Cancel booking
            booking = Booking.objects.filter(user=user, event=event).first()
            if booking:
                booking.delete()
                messages.success(request, f"Successfully canceled booking for {event.event_title}.")
                Event.objects.filter(id=event.id).update(  
                    available_seats=event.available_seats + 1
                )
            else:
                messages.error(request, "No booking found to cancel.")
            return redirect("current")

            
    current_user = request.user
    events = Event.objects.all().order_by('event_date').order_by('event_time')
    bookings = Booking.objects.filter(user=request.user)
    
    context = {
        'user': current_user,
        'events': events,
        'bookings': bookings
    }
    
    return render(request, "current.html", context)


@login_required(login_url='login')
def createEvent(request):
    if request.method == "POST":
        event_title = request.POST.get("event_title")
        event_subtitle = request.POST.get("event_subtitle")
        event_date = request.POST.get("event_date")
        event_time = request.POST.get("event_time")
        event_price = request.POST.get("event_price")
        event_location = request.POST.get("event_location")
        available_seats = request.POST.get("available_seats")

        # Validate required fields
        if not event_title or not event_date:
            messages.error(request, "Event name and date are required.")
            return render(request, "createEvent.html")

        try:
            # Try creating the event
            Event.objects.create(
                event_title=event_title,
                event_subtitle=event_subtitle,
                event_date=event_date,
                event_time=event_time,
                event_price=float(event_price) if event_price else 0.0,
                event_location=event_location,
                available_seats=int(available_seats) if available_seats else 0,
                creator=request.user
            )

            messages.success(request, "Event created successfully!")
            return redirect("/upcoming_events/")

        except ValueError:
            # Handle invalid conversions (e.g., non-numeric price/seats)
            messages.error(request, "Please enter valid numbers for price and seats.")
            return render(request, "createEvent.html")
        except Exception as e:
            # Catch-all for unexpected errors
            messages.error(request, f"An unexpected error occurred: {e}")
            return render(request, "createEvent.html")

    return render(request, "createEvent.html")

@login_required
def editEvent(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Only creator can edit
    if request.user != event.creator:
        return redirect('/')

    if request.method == 'POST':
        # Get values from the form
        event.event_title = request.POST.get('event_title', event.event_title)
        event.event_subtitle = request.POST.get('event_subtitle', event.event_subtitle)
        event.event_date = request.POST.get('event_date', event.event_date)
        event.event_time = request.POST.get('event_time', event.event_time)
        event.event_price = request.POST.get('event_price', event.event_price)
        event.event_location = request.POST.get('event_location', event.event_location)
        event.available_seats = request.POST.get('available_seats', event.available_seats)

        # Convert date and time strings to proper objects
        try:
            event.event_date = datetime.strptime(request.POST['event_date'], '%Y-%m-%d').date()
            event.event_time = datetime.strptime(request.POST['event_time'], '%H:%M').time()
            event.event_price = float(request.POST['event_price'])
            event.available_seats = int(request.POST['available_seats'])
        except (ValueError, KeyError):
            pass  # optionally handle errors

        event.save()
        return redirect('/upcoming_events/')

    return render(request, "editEvent.html", {'event': event})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Only the creator can delete their own event
    if event.creator != request.user:
        return HttpResponseForbidden("You are not allowed to delete this event.")

    if request.method == "POST":
        event.delete()
        return redirect("/upcoming_events/")  # or wherever you want to send them after deletion

    # optional: confirm deletion page
    return render(request, "confirmDelete.html", {"event": event})
