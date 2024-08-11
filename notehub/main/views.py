import os
import json
import uuid
import re
import mimetypes
from os.path import join
from datetime import datetime
from elasticsearch_dsl import Q

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

from .models import UserProfile, Document, Tag
from .utils import generate_verification_code, upload_to_drive, send_email, decode_with_random_salt, send_verification_email
from .serailizers import DocumentSerializer, BasicDocumentSerializer
from .documents import DocumentDocument

AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'

# GOOGLE_CLIENT_AUTH_TOKEN_FILE = 'google-client-auth-token.json'

# with open(join(settings.BASE_DIR, GOOGLE_CLIENT_AUTH_TOKEN_FILE)) as file:
#     GOOGLE_CLIENT_AUTH_TOKEN = json.load(file)

# metadata_dict = {
#     'full_login_url': GOOGLE_CLIENT_AUTH_TOKEN['web']['full_login_url']
# }

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
            login_user(request, user, backend=AUTH_BACKEND)
            messages.add_message(request, 40, f"Logged In!", extra_tags="success")
            return redirect('index')
        messages.add_message(request, 40, f"Invalid Password for {username}!", extra_tags="danger")
        return redirect('login')
    if request.user.is_authenticated:
        messages.add_message(request, 40, f"Already logged In!", extra_tags="success")
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
        login_user(request, user, backend=AUTH_BACKEND)
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
        profile_url = upload_to_drive(file_path, f"{random_id}_{image.name}")
        fs.delete(file_path)
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.profile_url = profile_url
        except:
            user_profile = UserProfile(user=request.user, profile_url=profile_url)
        user_profile.save()

        return JsonResponse({'message': 'File uploaded successfully!', 'success': True}, status=201)
    return redirect('index')

@login_required
def logout(request):
    messages.add_message(request, 40, f"Logged out successfully!", extra_tags="success")
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
        subject = 'Your verification code!'
        template = 'verification_code.html'
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

def verify_user(request, encoded_email):
    email = decode_with_random_salt(encoded_email)
    try:
        user = User.objects.get(email=email)
    except:
        messages.add_message(request, 40, f"Something went wrong!", extra_tags="danger")
        return redirect('index')
    verified_status = cache.get(f"verification_status:{user.email}")
    if verified_status:
        if verified_status == 'pending':
            cache.delete(f"verification_status:{user.email}")
            messages.add_message(request, 40, f"User has been verified!", extra_tags="success")
    else:
        messages.add_message(request, 40, f"User is already verified!", extra_tags="success")
    login_user(request, user, backend=AUTH_BACKEND)
    return redirect('index')

@login_required
def user_verification_status(request):
    verified_status = cache.get(f"verification_status:{request.user.email}")
    if verified_status:
        return JsonResponse({'message': f"Verification Incomplete!", "success": True})
    else:
        return JsonResponse({'message': f"Verification Complete!", "success": False})

@login_required
def resend_verification_email(request):
    send_verification_email(request.user)
    messages.add_message(request, 40, f"Verification email has been sent to {request.user.email}, check inbox and click on the link!", extra_tags="success")
    return redirect('index')

@login_required
def profile(request):
    return redirect('index')

@login_required
def feed(request):
    return render(request, 'main/feed.html')

@login_required
def load_posts(request, limit, last_doc_id):
    if int(last_doc_id) == -1:
        documents = Document.objects.all().order_by('-id')[:limit]
    else:
        documents = Document.objects.filter(id__lt=last_doc_id).order_by('-id')[:limit]
    documents_serailizer = DocumentSerializer(documents, many=True)
    return JsonResponse({'data': documents_serailizer.data, 'success': True}, safe=False)

@login_required
def upload_document_file(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            user = User.objects.get(id=request.user.id)
        except:
            return JsonResponse({'message': f"{request.user.email} is not a registered user email", "success": False})
        random_id = str(uuid.uuid1())
        file = request.FILES['attached_doc']
        fs = FileSystemStorage()
        filename = fs.save(f"{random_id}_{file.name}", file)
        file_path = fs.path(filename)
        document_url = upload_to_drive(file_path, f"{random_id}_{file.name}")
        document_size = fs.size(file_path)
        document_type, _ = mimetypes.guess_type(fs.path(file_path))
        fs.delete(file_path)
        return JsonResponse({
            'message': 'File uploaded successfully!', 
            'success': True,
            'document_url': document_url,
            'document_size': document_size,
            'document_type': document_type
        }, status=201)
    return redirect('index')

@login_required
def add_notes(request):
    if request.method == 'POST':
        document_title = request.POST['document_title']
        document_desc = request.POST['document_desc']
        document_type = request.POST['document_type']
        document_size = request.POST['document_size']
        document_url = request.POST['document_url']
        
        document = Document.objects.create(
            title=document_title,
            description=document_desc,
            author=request.user,
            file_url=document_url,
            file_size=document_size,
            file_type=document_type
        )

        tags = re.findall(r'#\w[\w-]*', document_desc)
        tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags]
        document.tags.set(tags)
        document.save()

    return redirect('feed')

def search_documents(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('q', '')
        search_query = Q('bool', should=[
            Q('multi_match', query=query, fields=['title', 'description', 'tags.raw']),
            Q('match', author__username={
                'query': query.lower(),
                'fuzziness': 'AUTO'
            })
        ])
        search_results = DocumentDocument.search().query(search_query)
        results = search_results.to_queryset()
        basic_document_serailizer = BasicDocumentSerializer(results, many=True)
        return JsonResponse({'data': basic_document_serailizer.data, 'success': True})

    return JsonResponse({'data': None, 'success': False})

def posts(request, id):
    try:
        post = Document.objects.select_related('author__profile').get(id=id)
        return render(request, 'main/posts.html', {'post': post})
    except:
        data = {'content': 'The post is unavailable'}
        return render(request, 'main/404.html', data)
