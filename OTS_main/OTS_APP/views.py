from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
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

def landingPage(request):
    return render(request, "landingPage.html")

def upcoming(request):
    return render(request, "upcoming.html")

def current(request):
    return render(request, "current.html")

def individualEvent(request):
    return render(request, "individualEvent.html")

def createEvent(request):
    return render(request, "createEvent.html")

def editEvent(request):
    return render(request, "editEvent.html")


