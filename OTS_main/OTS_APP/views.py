from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *
# Home page view
def home(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = UserRegistrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            new_user = None
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            f_name = form.cleaned_data['first_name']
            l_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            user_type = form.cleaned_data['usertype']
            # Create a new user
            if user_type == "User":
                new_user = User.objects.create_user(username=username, email=email, password=password)
                
            if user_type == "Manager":
                base_user = User.objects.create_user( username=username,email=email,password=password)
                new_user = Manager.objects.create(user_ptr=base_user)
               
            # set other attributes 
            if new_user:
                new_user.first_name = f_name
                new_user.last_name = l_name
                new_user.age = age
                new_user.save()
            
            
            # redirect to a new URL:
            return HttpResponseRedirect("/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserRegistrationForm()
    
    return render(request, "home.html", {"registration_form": form})
