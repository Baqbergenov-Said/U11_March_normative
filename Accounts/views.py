from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from django.contrib import messages
from .forms import RegisterForm, ForgotPasswordForm, NewPasswordForm, CodeVerifyForm
from .models import VerificationCode

from .utils import send_email_threading

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('Accounts:login')
    return render(request, 'accounts/logout.html')

# Validation for password reset forms

def forgot_password_view(request):
    form = ForgotPasswordForm()

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, "User not found!")
                return render(request, 'accounts/forgot_password.html', {'form': form})

            VerificationCode.objects.filter(user=user).delete()

            verification = VerificationCode.objects.create(user=user)

            send_email_threading(
                subject="Password Reset Verification Code",
                message=f"Your verification code: {verification.code}\n"
                        f"The code will expire in 2 minutes.",
                recipient_email=user.email
            )

            request.session['reset_username'] = username
            messages.success(request, f"{user.email} verification code has been sent to your email.")
            return redirect('Accounts:verify-code')

    return render(request, 'accounts/forgot_password.html', {'form': form})

def restore_password_view(request):
    username = request.session.get('reset_username')

    if not username:
        messages.error(request, "Please enter your username first!")
        return redirect('Accounts:forgot-password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('Accounts:forgot-password')

    form = NewPasswordForm(user=user)

    if request.method == 'POST':
        form = NewPasswordForm(request.POST, user=user)  

        if form.is_valid():
            new_password = form.cleaned_data['new_password']

            user.set_password(new_password)
            user.save()

            del request.session['reset_username']
            messages.success(request, "Password updated successfully! Please login.")
            return redirect('Accounts:login')

    return render(request, 'accounts/restore_password.html', {'form': form})

def verify_code_view(request):
    form = CodeVerifyForm()
    username = request.session.get('reset_username')

    if not username:
        messages.error(request, "Please enter your username first!")
        return redirect('Accounts:forgot-password')

    if request.method == 'POST':
        form = CodeVerifyForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['code']

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return redirect('Accounts:forgot-password')

            try:
                verification = VerificationCode.objects.get(
                    user=user,
                    code=entered_code
                )
            except VerificationCode.DoesNotExist:
                messages.error(request, "Verification code not valid!")
                return render(request, 'accounts/code.html', {'form': form})

            if verification.is_expired():
                verification.delete()
                messages.error(request, "Code has expired! Please try again.")
                return redirect('Accounts:forgot-password')

            verification.delete()
            request.session['code_verified'] = True
            return redirect('Accounts:restore-password')  

    return render(request, 'accounts/code.html', {'form': form})
