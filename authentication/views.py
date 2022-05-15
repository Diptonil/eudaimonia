from authentication.models import Profile
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import SignupForm, LoginForm, ProfileForm
from .tokens import account_activation_token


def index_page_view(request):
    return render(request, 'authentication/index.html')


def login_page_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            use_username = None
            if str(form.cleaned_data['username']).find('@') >= 0:
                use_username = False
            else:
                use_username = True
            if use_username:
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            else:
                user = get_user_model().objects.get(email=form.cleaned_data['username'])
                user = authenticate(username=user.username, password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('journal')
            else:
                messages.warning(request, 'The given combination of credentials do not exist. Please recheck your entry.')
        else:
            print(form.errors)
    return render(request, 'authentication/login.html', {'form': form})


def signup_page_view(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('emails/account-activation-email.txt', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage("Activate your Eudaimonia Account", message, settings.DEFAULT_FROM_EMAIL, [form.cleaned_data['email']])
            email.send(fail_silently=False)
            messages.success(request, 'An activation link has been sent to your email. Be sure to check your spam folder as well.')
        else:
            print(form.errors)
    return render(request, 'authentication/signup.html', {'form': form})


def services_page_view(requests):
    return render(requests, 'extras/services.html')


def activate_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        message = render_to_string('emails/account-activated-email.txt')
        email = EmailMessage("Welcome to Eudaimonia!", message, settings.DEFAULT_FROM_EMAIL, [user.email])
        email.send(fail_silently=False)
        return redirect('journal')
    else:
        return render(request, 'authentication/account_activation_invalid.html')


def account_activation_sent_page_view(request):
    return render(request, 'authentication/account_activation_sent.html')


def password_reset_page_view(request):
    password_reset_form = PasswordResetForm()
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = get_user_model().objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    message = render_to_string('emails/password_reset_email.txt', c)
                    email = EmailMessage("Reset Password for your Eudaimonia Account", message, settings.DEFAULT_FROM_EMAIL, [user.email])
                    email.send(fail_silently=False)
                    return redirect("/password_reset/done/")
    return render(request, 'authentication/password_reset.html', {"password_reset_form": password_reset_form})


@login_required
def password_change_page_view(request):
    form = PasswordChangeForm(request.user)
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('journal')
        else:
            messages.error(request, 'Please correct the error below.')
    return render(request, 'authentication/password_change.html', {'form': form})


@login_required
def logout_page_view(request):
    logout(request)
    return redirect('index')


@login_required
def settings_page_view(request):
    return render(request, 'extras/settings.html')


@login_required
def profile_page_view(request):
    profile = Profile.objects.get(user=request.user)
    if profile.bio is None:
        profile.bio = ''
    if profile.birth_date is None:
        profile.birth_date = '-'
    return render(request, 'authentication/profile.html', {'profile': profile})


@login_required
def profile_edit_page_view(request):
    form = ProfileForm()
    profile = Profile.objects.get(user=request.user)
    model_bio = profile.bio
    model_birth_date = profile.birth_date
    if model_bio is not None:
        form.fields['bio'].widget.attrs['placeholder'] = model_bio
    if model_birth_date is not None:
        form.fields['birth_date'].widget.attrs['placeholder'] = model_birth_date
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            bio = form.cleaned_data['bio']
            if bio == '':
                bio = None
            birth_date = form.cleaned_data['birth_date']
            image = form.cleaned_data.get('image')
            if bio is not None:
                profile.bio = bio
            if image is not None:
                profile.image = image
            if birth_date is not None:
                profile.birth_date = birth_date
            profile.save()
            return redirect('profile')
    return render(request, 'authentication/profile_edit.html', {'form': form, 'profile': profile})


def demo_page_view(request):
    return render(request, 'authentication/demo.html')


def handler404(request, exception, template_name="extras/404.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response


def handler403(request, exception, template_name="extras/403.html"):
    response = render(request, template_name)
    response.status_code = 403
    return response


def handler400(request, exception, template_name="extras/400.html"):
    response = render(request, template_name)
    response.status_code = 400
    return response


def handler500(request, *args, **argv):
    return render(request, 'extras/500.html', status=500)
