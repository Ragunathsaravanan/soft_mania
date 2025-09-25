from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UploadedFile
from django.http import FileResponse, Http404
import os

ALLOWED_EXT = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        address = request.POST.get('address')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            user = User.objects.create_user(
                name=name, age=age, address=address,
                email=email, mobile=mobile, password=password
            )
            messages.success(request, "Signup successful! Please login.")
            return redirect('login')

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "User not found! Please sign up first.")
    return render(request, 'login.html')


def dashboard(request):
    if not request.session.get('user_id'):
        return redirect('login')
    files = UploadedFile.objects.filter(user_id=request.session['user_id'])
    
    for f in files:
        username = f.user.name
        filename = os.path.basename(f.file.name)
        f.display_name = f"{username}/{filename}"  
    
    return render(request, 'dashboard.html', {'files': files})

def upload_file(request):
    if not request.session.get('user_id'):
        return redirect('login')
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            messages.error(request, "No file uploaded.")
            return redirect('upload_file')

        ext = uploaded_file.name.rsplit('.', 1)[-1].lower() if '.' in uploaded_file.name else ''
        if ext not in ALLOWED_EXT:
            messages.error(request, "Invalid file type. Only PDF/PNG/JPEG allowed.")
            return redirect('upload_file')

        if uploaded_file.size > MAX_UPLOAD_SIZE:
            messages.error(request, "File too large. Max size is 10 MB.")
            return redirect('upload_file')

        file_instance = UploadedFile(
            user=User.objects.get(id=request.session['user_id']),
            file=uploaded_file,
            file_type=ext
        )
        file_instance.save()
        messages.success(request, "File uploaded successfully")
        return redirect('dashboard')
    return render(request, 'upload.html')


def download_file(request, file_id):
    try:
        f = UploadedFile.objects.get(id=file_id, user_id=request.session['user_id'])
        path = f.file.path
        return FileResponse(open(path, 'rb'), as_attachment=True, filename=os.path.basename(path))
    except UploadedFile.DoesNotExist:
        raise Http404
