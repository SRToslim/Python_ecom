from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from helpbazar import settings
from .models import User, Profile
from .utils import *


def register_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('index'))
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password1 = request.POST.get('password1')
            special_characters = '!@#$%^&*()_+[]{}|;:,.<>?'

            if password == password1:
                if len(password) < 8 or len(password) > 64:
                    messages.warning(request, 'Password Must Be Between 8 to 64 character!')
                    return redirect('register')
                elif not any(char in special_characters for char in password):
                    messages.warning(request, 'Password must be contain special characters')
                else:
                    if User.objects.filter(username=name).exists():
                        messages.warning(request, 'Username Already Taken!')
                        return redirect('register')
                    elif User.objects.filter(email=email).exists():
                        messages.warning(request, 'Email Already Taken!')
                        return redirect('register')
                    else:
                        user = User.objects.create(username=name, email=email, password=password)
                        user.set_password(password)
                        user.is_active = False
                        user.ip = get_client_ip(request)
                        user.client_os_info = get_client_os_info(request)
                        user.client_browser_info = get_client_browser_info(request)
                        user.save()

                        activateEmail(request, user, email)
                        return render(request, 'auth/register-email.html', {'name': name, 'email': email})
            else:
                messages.warning(request, 'Password and Confirm Password not matched.')
    return render(request, 'auth/register.html')


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('auth/email_confirmation.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    try:
        email.send()
    except Exception as e:
        messages.error(
            request,
            f'Problem sending confirmation email to {to_email}. Error: {str(e)}'
        )


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if user.is_active:
            messages.warning(request, 'Your account is already activated. Please log in.')
        else:
            user.is_active = True
            user.is_verify = True
            user.save()
            Profile.objects.create(user=user)

            messages.success(request, 'Thank you for your email confirmation. Now you can log in to your account.')
    else:
        messages.error(request, 'Activation link is invalid or has expired.')

    return redirect('login') if user.is_active else HttpResponseRedirect(reverse('index'))


def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, f'Hey you are already Logged In')
        return HttpResponseRedirect(reverse('index'))

    else:
        if request.method.upper() == 'POST':
            username = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(
                request=request,
                username=username,
                password=password,
            )
            if user:
                user.last_ip = get_client_ip(request)
                user.client_os_info = get_client_os_info(request)
                user.client_browser_info = get_client_browser_info(request)
                user.client_device_info = get_client_device_info(request)
                user.is_online = True
                user.save()
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.error(request, f'User does not exist or the password is incorrect.')

    return render(request, 'auth/login.html')


def password_reset_request(request):
    if request.method == 'post' or request.method == 'POST':
        identifier = request.POST.get('email')
        try:
            user = User.objects.get(Q(username__iexact=identifier) |
                                    Q(email__iexact=identifier) |
                                    Q(membership_no__iexact=identifier))
            passwordEmail(request, user)
            return render(request, 'auth/password-email.html', {'user': user})
        except User.DoesNotExist:
            return redirect('register')

    return render(request, 'auth/forgot-password.html')


def passwordEmail(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    activation_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})

    mail_subject = 'Reset your account password.'
    message = render_to_string('auth/password_reset_email.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'activation_url': activation_url,
        'protocol': 'https' if request.is_secure() else 'http'
    })
    send_mail(mail_subject, message, settings.EMAIL_FROM, [user.email])


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                password = request.POST.get('password')
                password1 = request.POST.get('password1')
                if password == password1:
                    if user.check_password(password):
                        messages.error(request, f'New password is same as Old Password. Try new one.')
                        return render(request, 'auth/reset-password.html', {'user': user})
                    else:
                        user.set_password(password)
                        user.save()
                        messages.success(request, f'Password reset is successfully.')
                        return redirect('login')
                else:
                    messages.error(request, f'Password and Confirm Password dose not match.')
            else:
                return render(request, 'auth/reset-password.html', {'user': user})
        else:
            messages.error(request, 'Token has expired. Please request a new one.')
            return redirect('login')
    except Exception as e:
        messages.error(
            request, f'Something is wrong. Error: {str(e)}'
        )


def logout_view(request):
    user = request.user
    user.is_online = False
    user.save()
    logout(request)
    messages.success(request, 'You are successfully logged out from your account.')
    return redirect('login')
