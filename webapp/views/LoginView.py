from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.checks import messages
from django.shortcuts import redirect
from django.shortcuts import render
from knox.models import AuthToken


# views.py


def logout_view(request):
    logout(request)
    return redirect('login')


#
# def login_view(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             # Extract username and password from the validated form
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#
#             # Authenticate the user
#             user = authenticate(request, username=username, password=password)
#
#             if user is not None:
#                 # User is authenticated, so log them in
#                 login(request, user)
#
#                 # Generate Knox token
#                 instance, token = AuthToken.objects.create(user)
#
#                 # Prepare the response
#                 response = JsonResponse({"message": "Logged in successfully!"})
#
#                 # Set the token in an HttpOnly cookie
#                 expiration = datetime.utcnow() + timedelta(hours=10)  # adjust as needed
#                 response.set_cookie(
#                     key='token',
#                     value=token,
#                     expires=expiration,
#                     httponly=True,
#                     secure=True  # Ensure cookie is only sent over HTTPS (omit if working locally without HTTPS)
#                 )
#                 return redirect('dashboard')
#             else:
#                 # Authentication failed
#                 return render(request, 'utility_pages/login.html', {'error': 'Invalid credentials'})
#     else:
#         # If it's a GET request or any other method, show the form
#         form = LoginForm()
#
#     return render(request, 'utility_pages/login.html', )


from django.urls import reverse


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Generate Knox token
                instance, token = AuthToken.objects.create(user)

                # Set the token in an HttpOnly cookie
                response = redirect(reverse('dashboard'))  # assuming 'dashboard' is the name of your URL pattern
                expiration = datetime.utcnow() + timedelta(hours=10)  # adjust as needed
                response.set_cookie(
                    key='token',
                    value=token,
                    expires=expiration,
                    httponly=True,
                    secure=True  # Ensure cookie is only sent over HTTPS (omit if working locally without HTTPS)
                )
                return response
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')

    form = AuthenticationForm()
    return render(request, 'utility_pages/login.html', {'form': form})

#
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:  # If the user exists and the credentials were correct
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             # If authentication failed, you can notify the user.
#             return render(request, 'utility_pages/login.html', {'error': 'Invalid credentials'})
#
#     return render(request, 'utility_pages/login.html')
