from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# views.py

from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:  # If the user exists and the credentials were correct
            login(request, user)
            return redirect('dashboard')
        else:
            # If authentication failed, you can notify the user.
            return render(request, 'utility_pages/login.html', {'error': 'Invalid credentials'})

    return render(request, 'utility_pages/login.html')

