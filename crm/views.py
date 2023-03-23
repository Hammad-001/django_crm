from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegistrationForm


def home(request):
    # Check if user is trying to log in
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Checking if user has valid credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # if user is authenticated successfully
            login(request, user)
            messages.success(request, "You have been logged in successfully!")
            return redirect('home')
        else:
            # if credentials are not valid
            messages.success(
                request, "Username or password is incorrect! Please try again.")
            return redirect('home')
    else:
        # if user is just accessing the homepage
        return render(request, 'home.html', {})


def logout_user(request):
    # if user is logged in
    if request.user.is_authenticated:
        # logout user
        logout(request)
        messages.success(request, "You have been logged out successfully!")
        return redirect('home')
    else:
        # if user is not logged in then redirect to home
        messages.success(request, "You are not logged in!")
        redirect('home')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # checking if user is submitting data
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # if data is valid, then save it
            form.save()
            # getting username, password to authenticate and login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # if user authentication succeeded
                login(request, user)
                messages.success(request, "You have successfully registered!")
                return redirect("home")
            else:
                messages.success(request, "Registration failed!!")
                return redirect("register")
    else:
        # if user want to register then Registration form
        form = RegistrationForm()
        return render(request, "register.html", {'form': form})
    return render(request, "register.html", {'form': form})
