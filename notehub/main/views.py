import os
import json
import uuid
from os.path import join
from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth import authenticate as authenticate_user
from django.contrib.auth import login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

from .models import UserProfile
from .utils import generate_verification_code, upload_to_drive, send_email

def index(request):
    return render(request, 'main/index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if not user.has_usable_password():
                messages.add_message(request, 40, f"Password is not set for {username}", extra_tags="warning")
                return redirect('login')
        except:
            messages.add_message(request, 40, f"User with {username} does not exists!", extra_tags="danger")
            return redirect('login')
        user = authenticate_user(request, username=username, password=password)
        if user:
            backend = 'django.contrib.auth.backends.ModelBackend'
            login_user(request, user, backend=backend)
            return redirect('index')
        messages.add_message(request, 40, f"Invalid Password for {username}!", extra_tags="danger")
        return redirect('login')
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'main/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            if User.objects.get(email=username):
                messages.add_message(request, 40, f"User with {username} already exists", extra_tags="danger")
                return redirect('register')
        except:
            pass
        password = make_password(request.POST['password'])
        user = User.objects.create(username=username, password=password, email=username)
        backend = 'django.contrib.auth.backends.ModelBackend'
        login_user(request, user, backend=backend)
        return render(request, 'main/register_intermediate.html')
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'main/register.html')

@login_required(login_url='/login')
def register_int(request):
    if request.method == 'POST' and request.user.is_authenticated:
        fname = request.POST['fname']
        lname = request.POST['lname']
        user = User.objects.get(id=request.user.id)
        user.first_name = fname
        user.last_name = lname
        user.save()
    return redirect('index')

@login_required
def upload_profile_image(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            user = User.objects.get(id=request.user.id)
        except:
            return JsonResponse({'message': f"{request.user.email} is not a registered user email", "success": False})
        random_id = str(uuid.uuid1())
        image = request.FILES['profile_image']
        fs = FileSystemStorage()
        filename = fs.save(f"{random_id}_{image.name}", image)
        file_path = fs.path(filename)
        file_id = upload_to_drive(file_path, f"{random_id}_{image.name}")

        profile_url = f"https://drive.google.com/file/d/{file_id}/view"
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.profile_url = profile_url
            user_profile.updated_at = datetime.now()
        except:
            user_profile = UserProfile(user=request.user, profile_url=profile_url, created_at = datetime.now(), updated_at=datetime.now())
        user_profile.save()

        return JsonResponse({'message': 'File uploaded successfully!', 'success': True}, status=201)
    return redirect('index')

def logout(request):
    logout_user(request)
    return redirect('index')

def set_pasword_for_social_account(request):
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return render(request, 'main/set_password_social_account.html')
    return redirect('index')

@csrf_exempt
def send_verification_code(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except:
            return JsonResponse({'message': f"{email} is not a registered user email", "success": False})
        # Generate code and send it to email
        verification_code = generate_verification_code()
        cache.set(f"verification_code:{user.email}", verification_code, timeout=300)
        subject = 'Welcome Onboard !'
        template = 'welcome_and_verification_template.html'
        recipient = [user.email]
        metadata = {'user': user, 'ver_code': verification_code}
        sent = send_email(recipient, subject, template, metadata)
        if sent:
            return JsonResponse({'message': f"Verification code is sent to {user.email} !", "success": True})
        else:
            return JsonResponse({'message': f"Some error ocurred while sending email to {user.email} !", "success": False})

    return redirect('index')

@csrf_exempt
def validate_verification_code(request):
    if request.method == 'POST':
        email = request.POST['email']
        ver_code = request.POST['code']
        try:
            user = User.objects.get(email=email)
        except:
            return JsonResponse({'message': f"{email} is not a registered user email", "success": False})
        code = cache.get(f"verification_code:{user.email}")
        if not code:
            return JsonResponse({'message': f"Entered verification code is expired!", "success": False})
        elif code == ver_code:
            return JsonResponse({'message': f"Your verification is successful!", "success": True})
        else:
            return JsonResponse({'message': f"Entered code is incorrect!", "success": False})
    return redirect('index')

def update_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['cpassword']
        if not (password1 == password2):
            messages.add_message(request, 40, f"Passwords did not match!", extra_tags="danger")
            return redirect('set-password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.add_message(request, 40, f"User with {email} does not exits", extra_tags="danger")
            return redirect('set-password')
        hashed_password = make_password(password1)
        user.password = hashed_password
        user.save()
        print('password-updated')
        messages.add_message(request, 40, f"Password has been changed successfully!", extra_tags="success")
        return redirect('login')
    return redirect('index')

@login_required
def profile(request):
    return redirect('index')

@login_required
def feed(request):
    return redirect('index')

def test_url(request):
    return render(request, 'main/set_password_social_account.html')
