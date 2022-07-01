import decimal
import logging
import json

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
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
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.generic import UpdateView

import constants
from authentication.models import Profile
from authentication.forms import SignupForm, LoginForm, ProfileForm, RecommendationForm
from authentication.tokens import account_activation_token
from analysis.models import RegularityStat

logout_time = 0
login_time = 0
logger = logging.getLogger('main')
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def index_page_view(request):
    return render(request, 'authentication/index.html')


def login_page_view(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            use_username = None
            if str(login_form.cleaned_data['user_identifier']).find('@') >= 0:
                use_username = False
            else:
                use_username = True
            if use_username:
                user = authenticate(username=login_form.cleaned_data['user_identifier'], password=login_form.cleaned_data['password'])
            else:
                user = get_user_model().objects.get(email=login_form.cleaned_data['user_identifier'])
                user = authenticate(username=user.username, password=login_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.warning(request, 'The given combination of credentials do not exist. Please recheck your entry.')
                logger.warning('Login unsuccesful.')
        else:
            print(login_form.errors)
    return render(request, 'authentication/login.html', {'form': login_form})


def signup_page_view(request):
    signup_form = SignupForm()
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_message = render_to_string('emails/account-activation-email.txt', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage("Activate your Eudaimonia Account", email_message, settings.DEFAULT_FROM_EMAIL, [signup_form.cleaned_data['email']])
            email.send(fail_silently=False)
            messages.success(request, 'An activation link has been sent to your email. Be sure to check your spam folder as well.')
        else:
            print(signup_form.errors)
            logger.warning('Signup unsuccesful.')
    return render(request, 'authentication/signup.html', {'form': signup_form})


def services_page_view(requests):
    return render(requests, 'extras/services.html')


def activate_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
        logger.warning('New user account not activated.')
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        email_message = render_to_string('emails/account_activated_email.txt')
        email = EmailMessage("Welcome to Eudaimonia!", email_message, settings.DEFAULT_FROM_EMAIL, [user.email])
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
                    email_parameters = {
                        'email': user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email_message = render_to_string('emails/password_reset_email.txt', email_parameters)
                    email = EmailMessage("Reset Password for your Eudaimonia Account", email_message, settings.DEFAULT_FROM_EMAIL, [user.email])
                    email.send(fail_silently=False)
                    return redirect("/password_reset/done/")
            else:
                logger.warning('User with specified credentials doesn\'t exist. Password not changed.')
    return render(request, 'authentication/password_reset.html', {"password_reset_form": password_reset_form})


@login_required
def password_change_page_view(request):
    password_change_form = PasswordChangeForm(request.user)
    if request.method == "POST":
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('journal')
        else:
            messages.error(request, 'Please correct the error below.')
            logger.warning('Typed in passwords don\'t match. Password not changed.')
    return render(request, 'authentication/password_change.html', {'form': password_change_form})


@login_required
def logout_page_view(request):
    cache.delete(constants.CURRENT_USER_CACHE_KEY)
    if request.POST.get('time_spent') is not None and (request.method == 'POST'):
        print('ass')
        time_spent = decimal.Decimal(request.POST.get('time_spent'))
        model = RegularityStat.objects.filter(user=request.user).first()
        model.time_spent += time_spent
        model.save()
        logout(request)
        return HttpResponse(json.dumps(1), content_type='application/json')


@login_required
def settings_page_view(request):
    profile_model = Profile.objects.get(user=request.user)
    return render(request, 'extras/settings.html', {'profile': profile_model})


@login_required
def profile_page_view(request):
    if cache.get(constants.CURRENT_USER_CACHE_KEY):
        profile_model = cache.get(constants.CURRENT_USER_CACHE_KEY)
    else:
        profile_model = Profile.objects.get(user=request.user)
        cache.set(constants.CURRENT_USER_CACHE_KEY, profile_model)
    if profile_model.bio is None:
        profile_model.bio = ''
    if profile_model.birth_date is None:
        profile_model.birth_date = '-'
    return render(request, 'authentication/profile.html', {'profile': profile_model})


@login_required
def profile_edit_page_view(request):
    profile_form = ProfileForm()
    if cache.get(constants.CURRENT_USER_CACHE_KEY):
        profile_model = cache.get(constants.CURRENT_USER_CACHE_KEY)
    else:
        profile_model = Profile.objects.get(user=request.user)
        cache.set(constants.CURRENT_USER_CACHE_KEY, profile_model)
    model_bio = profile_model.bio
    model_birth_date = profile_model.birth_date
    model_favourite_movie_genres = [obj[0] for obj in profile_model.fav_movie_genres.values_list('field')]
    model_disliked_movie_genres = [obj[0] for obj in profile_model.unfav_movie_genres.values_list('field')]
    model_favourite_music_genres = [obj[0] for obj in profile_model.fav_music_genres.values_list('field')]
    model_disliked_music_genres = [obj[0] for obj in profile_model.unfav_music_genres.values_list('field')]
    print(model_favourite_movie_genres)
    print(model_favourite_music_genres)
    if model_bio is not None:
        profile_form.fields['bio'].widget.attrs['placeholder'] = model_bio
    if model_birth_date is not None:
        profile_form.fields['birth_date'].widget.attrs['placeholder'] = model_birth_date
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            bio = profile_form.cleaned_data['bio']
            if bio == '':
                bio = None
            birth_date = profile_form.cleaned_data['birth_date']
            image = profile_form.cleaned_data.get('image')
            if bio is not None:
                profile_model.bio = bio
            if image is not None:
                profile_model.image = image
            if birth_date is not None:
                profile_model.birth_date = birth_date
            profile_model.save()
            return redirect('profile')
    return_dict = {'form': profile_form, 'profile': profile_model, 'fav_mov': model_favourite_movie_genres, 'unfav_mov': model_disliked_movie_genres, 'fav_mus': model_favourite_music_genres, 'unfav_mus': model_disliked_music_genres}
    return render(request, 'authentication/profile_edit.html', return_dict)


class RecommendationPageView(UpdateView):

    model = Profile
    form_class = RecommendationForm
    template_name = 'authentication/recommendation_edit.html'

    def get_success_url(self):
        return reverse('profile_edit')


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
