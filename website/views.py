from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    #check to see if logging in
    if request.method == 'POST':
        Username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=Username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been log in !")
            return redirect("home")
        else:
            messages.success(request, "Pleas try  again...")
            return redirect("home")
    else:
        return render(request, "home.html", {})

# def login_user(request):
    # pass

def logout_user(request):
    logout(request)
    messages.success(request, "you have been logged out...")
    return redirect("home")

def register_user(request):
    return render(request, "register.html", {})