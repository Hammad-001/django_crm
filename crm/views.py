from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegistrationForm, CustomerForm
from .models import Customer


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
        if request.user.is_authenticated:

            # fetch all customer records
            records = Customer.objects.all()

            # if user is just accessing the homepage
            return render(request, 'home.html', {'records': records})

        else:

            # if user is not authenticated and not requesting for login
            return render(request, 'home.html', {})


def logout_user(request):
    # if user is logged in
    if request.user.is_authenticated:
        # logout user
        logout(request)
        messages.success(request, "You have been logged out successfully!")
    else:
        # if user is not logged in then redirect to home
        messages.success(request, "You are not logged in!")

    return redirect('home')


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


def view_record(request, customer):
    # Check if user is already authenticated
    if request.user.is_authenticated:

        # if request has customer id
        if customer is not None:

            try:
                # getting the record from Customer Model
                customer = Customer.objects.get(pk=customer)
                return render(request, 'customer.html', {'customer': customer})

            except Customer.DoesNotExist:

                # if customer ID is not valid
                messages.success(request, "Requested customer is not a valid customer!")
                return redirect('home')

        else:
            messages.success(request, 'Please select a valid customer!')

    else:
        # if user is not logged in then redirect to home
        messages.success(request, "You are authorized to view customers!")
    return redirect('home')


def delete_record(request, customer):
    # Check if user is signed in
    if request.user.is_authenticated:

        # if request has customer id
        if customer is not None:

            try:
                # getting the record from Customer Model
                customer = Customer.objects.get(pk=customer)

            except Customer.DoesNotExist:

                # if customer ID is not valid
                messages.success(request, "Requested Record is not a valid customer!")
                return redirect('home')

            # if Customer found successfully, then delete customer
            customer.delete()
            messages.success(request, "Customer Record deleted successfully!")

        else:
            # if customer ID is not valid
            messages.success(request, 'Please select a valid customer!')

    else:
        # if user is not logged in then redirect to home
        messages.success(request, "You are authorized to delete customers!")
    return redirect('home')


def add_record(request):
    # Checking if user is logged in
    if request.user.is_authenticated:

        form = CustomerForm(request.POST or None)

        # checking if user wants to save data of customer
        if request.method == "POST":

            # checking if customer data is valid
            if form.is_valid():
                form.save()
                messages.success(request, "Customer is successfully registered!")
                return redirect("home")

        return render(request, 'add_customer.html', {'form': form})
    else:
        # if user is not logged in then redirect to home
        messages.success(request, "You are authorized to delete customers!")
        return redirect('home')


def update_record(request, customer):
    # Checking if user is logged in
    if request.user.is_authenticated:

        # if request has customer id
        if customer is not None:

            try:
                # getting the record from Customer Model
                customer = Customer.objects.get(pk=customer)

            except Customer.DoesNotExist:

                # if customer ID is not valid
                messages.success(request, "Requested Record is not a valid customer!")
                return redirect('home')

            # if Customer found successfully, then return form of that customer
            form = CustomerForm(request.POST or None, instance=customer)

            if request.method == "POST":
                if form.is_valid():
                    form.save()
                    messages.success(request, "Customer Record updated successfully!")
            else:
                return render(request, 'update_record.html', {'form': form})
        else:
            # if customer ID is not valid
            messages.success(request, 'Please select a valid customer!')
    else:
        # if user is not logged in then redirect to home
        messages.success(request, "You are authorized to delete customers!")

    return redirect('home')
