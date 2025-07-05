from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm , identifyForm
from django.core.mail import send_mail
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.utils import timezone
import datetime
from .utils import get_otp,enc_uname,dec_uname
from django.contrib.auth.forms import SetPasswordForm

def identifyuserview(request):
    if request.method == 'POST':
        form = identifyForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                user=User.objects.get(username=username)
                otp = get_otp()
                time = timezone.now() + datetime.timedelta(minutes=10)
                user.otp_verified = False
                user.otp = otp
                user.otp_expired = time
                email=user.email
                user.save()
                send_mail(
                    'OTP Verification',
                    f'your otp is {otp} enter otp to reset the password',
                    'amalendugame110@gmail.com',
                    [email],
                    fail_silently=True
                )
                messages.success(request,'user otp send your register email')
                en_uname = enc_uname(user.username)
                url = f'/register/OTPView/{en_uname}/'
                return redirect(url)
            messages.error(request,'user not found')
        else:
            print("Form is invalid:", form.errors)
    else:
        form = identifyForm()

    return render(request,'accounts/identify.html',{'form': form})


def OTPView(request,en_uname):
    username = dec_uname(en_uname)
    if User.objects.filter(username=username).exists():
        if request.method== 'POST':
            otp = int(request.POST['otp'])
            user = User.objects.get(username=username)
            if timezone.now() <= user.otp_expired:
                if not user.otp_verified:
                    if otp == user.otp:
                        user.otp_verified=True
                        user.save()
                        messages.success(request,'otp verified')
                        url = f'/register/resetpassword/{en_uname}/'
                        return redirect(url)
                    else:
                        messages.error(request,'invalid otp')
                        return redirect('identifyuser')
                messages.error(request,'otp already exist')
                return redirect('identifyuser')
            messages.error(request,'otp expire')
            return redirect('identifyuser')            
        return render(request,'accounts/otp.html')
    messages.error(request,'invalid request')
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            fname = form.cleaned_data.get('first_name')
            lname = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')

            send_mail(
                'Registration Successful',
                f'Hello {fname} {lname},\n\nThank you for registering!',
                'amalendugame110@gmail.com',
                [email],
                fail_silently=True
            )
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
        else:
            print(form.errors)  # Log form errors
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})



def Loginview(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'You are Login successfully {user.first_name}.')
                return redirect('movies')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


def Logoutview(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')



def resetpassword(request,en_uname):
    try:
        username = dec_uname(en_uname)
    except:
        messages.error(request,'invalid request')
        return redirect('login')
    if User.objects.filter(username=username).exists():
        user=User.objects.get(username=username)
        if request.method == 'POST':
            form = SetPasswordForm(user=user,data=request.POST)
            if form.is_valid():
                messages.success(request,'password reset successfully')
                form.save()
                return redirect('login')
            else:
                messages.error(request,'Password not matching')
        context = {
            'form' : SetPasswordForm(user=user)
        }
        return render(request, 'accounts/reset_password.html',context)
    messages.error(request,'user not exists')
    return redirect('login') 
