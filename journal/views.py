import hashlib
import json
import io
import random

import requests
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

import constants
from authentication.models import Profile
from journal.encryption import encrypt, decrypt
from journal.forms import EntrySearchForm
from journal.models import Entry, Zen
from analysis.models import EmotionsStat, Incentive

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@login_required
def journal_page_view(request):
    profile_model = Profile.objects.get(user=request.user)
    entry_model = Entry.objects.filter(user=request.user).first()
    count = Entry.objects.filter(user=request.user).count()
    return render(request, 'journal/journal.html', {'profile': profile_model, 'entry_model': entry_model, 'quotes': constants.QUOTES[random.randint(0, 9)], 'count': count})


@login_required
def entry_page_view(request):
    cache.delete(constants.ALL_ENTRIES_UNFILTERED_CACHE_KEY)
    profile_model = Profile.objects.get(user=request.user)
    # Hide 53 and 69 as environment variables!
    if request.POST.get('content') is not None and (request.method == 'POST'):
        title = str(request.POST.get('title'))
        content = str(request.POST.get('content'))
        content.replace('&nbsp;', '')
        headers = {'Authorization': 'Api-Key %s' % 'WNTDnKHs.bd9VaRno8zsc2S6r4l4owTFgLBnijakI'}
        response = requests.post('http://127.0.0.1:7000/api/v1/get_mood/', json={'CORPUS': content}, headers=headers).json()
        emotion = 'Happy' if response['Happy'] > response['Sad'] else 'Sad'
        print(response, content)
        happy = response.get('Happy', 0)
        sad = response.get('Sad', 0)
        surprise = response.get('Surprise', 0)
        fear = response.get('Fear', 0)
        angry = response.get('Angry', 0)
        EmotionsStat.objects.create(user=request.user, happy=happy, sad=sad, surprise=surprise, fear=fear, angry=angry, emotion=emotion)
        encryption_key = get_user_model().objects.get(username=request.user.username).password[53:69]
        encryption_key = hashlib.sha256(encryption_key.encode()).digest()
        content = encrypt(content, encryption_key)
        Entry.objects.create(user=request.user, entry=content, title=title).save()
        print(content)
        print(decrypt(content, encryption_key))
        return HttpResponse(json.dumps(1), content_type='application/json')
    return render(request, 'journal/entry.html', {'profile': profile_model})


@login_required
def post_page_view(request, id):
    profile_model = Profile.objects.get(user=request.user)
    entry_model = Entry.objects.get(id=id)
    star = entry_model.starred
    content = entry_model.entry[2:-1]
    encryption_key = get_user_model().objects.get(username=request.user.username).password[53:69]
    encryption_key = hashlib.sha256(encryption_key.encode()).digest()
    content = decrypt(content, encryption_key)
    entry_model.entry = content
    emotion_data = dict()
    headers = {'Authorization': 'Api-Key %s' % 'WNTDnKHs.bd9VaRno8zsc2S6r4l4owTFgLBnijakI'}
    request0 = requests.post('http://127.0.0.1:7000/api/v1/get_mood/', json={'CORPUS': content}, headers=headers).json()
    emotion = 'Happy' if request0['Happy'] > request0['Sad'] else 'Sad'
    print(emotion)
    model_favourite_movie_genres = [obj[0] for obj in profile_model.fav_movie_genres.values_list('field')]
    model_unfavourite_movie_genres = [obj[0] for obj in profile_model.unfav_movie_genres.values_list('field')]
    # model_favourite_music_genres = [obj[0] for obj in profile_model.fav_music_genres.values_list('field')]
    # model_unfavourite_music_genres = [obj[0] for obj in profile_model.unfav_music_genres.values_list('field')]
    favourites = ['No Country for Old Men', 'The Dark Knight']
    json_data = {'LIKED_MOVIE_GENRES': model_favourite_movie_genres, 'DISLIKED_MOVIE_GENRES': model_unfavourite_movie_genres, 'FAVOURITE_MOVIES': favourites, 'CORPUS': emotion}
    model_movie = requests.post('http://127.0.0.1:7000/api/v1/get_movie/', json=json_data, headers=headers)
    emotion_data['Happy'] = request0.get('Happy', 0)
    emotion_data['Angry'] = request0.get("Angry", 0)
    emotion_data['Sad'] = request0.get("Sad", 0)
    emotion_data['Surprise'] = request0.get("Surprise", 0)
    emotion_data['Fear'] = request0.get("Fear", 0)
    if request.method == 'POST':
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, features='html5lib')
        return redirect('pdf', text=soup.get_text().replace('\t', ' ').replace('\n', ''), filename='{0}.pdf'.format(entry_model.title))
    return render(request, 'journal/post.html', {'entry': entry_model, 'star': star, 'profile': profile_model, 'emotion_data': emotion_data, 'model_movie': model_movie})


@login_required
def all_entries_page_view(request, star=None):
    entry_search_form = EntrySearchForm()
    incentive_model = Incentive.objects.get(user=request.user)
    if cache.get(constants.ALL_ENTRIES_UNFILTERED_CACHE_KEY):
        entries = cache.get(constants.ALL_ENTRIES_UNFILTERED_CACHE_KEY)
    else:
        entries = Entry.objects.filter(user=request.user).filter(activated=True)
        cache.set(constants.ALL_ENTRIES_UNFILTERED_CACHE_KEY, entries)
    if star is not None:
        if cache.get(constants.ALL_ENTRIES_STARRED_CACHE_KEY):
            entries = cache.get(constants.ALL_ENTRIES_STARRED_CACHE_KEY)
        else:
            entries = entries.filter(starred=True)
            cache.set(constants.ALL_ENTRIES_STARRED_CACHE_KEY, entries)
    if cache.get(constants.CURRENT_USER_CACHE_KEY):
        profile_model = cache.get(constants.CURRENT_USER_CACHE_KEY)
    else:
        profile_model = Profile.objects.get(user=request.user)
        cache.set(constants.CURRENT_USER_CACHE_KEY, profile_model)
    results = None
    if entries.count() > 0 and entries.count() < 2:
        incentive_model.diarist1 = True
        incentive_model.save()
    elif entries.count() > 1 and entries.count() < 8:
        incentive_model.diarist2 = True
        incentive_model.save()
    elif entries.count() > 7 and entries.count() < 15:
        incentive_model.diarist3 = True
        incentive_model.save()
    elif entries.count() > 14 and entries.count() < 30:
        incentive_model.diarist4 = True
        incentive_model.save()
    if request.POST.get('stars') is not None and (request.method == 'POST'):
        cache.delete(constants.ALL_ENTRIES_STARRED_CACHE_KEY)
        entry = Entry.objects.get(id=request.POST.get('id'))
        if(str(request.POST.get('favourite')) == 'true'):
            entry.starred = True
        else:
            entry.starred = False
        entry.save()
        print(entry.starred)
        return JsonResponse({'result': 1})
    elif request.method == 'POST':
        entry_search_form = EntrySearchForm(request.POST)
        if entry_search_form.is_valid():
            search = entry_search_form.cleaned_data['search']
            if search is not None:
                results = Entry.objects.filter(title__icontains=search)
                if star is not None:
                    results = results.filter(starred=True)
    return render(request, 'journal/all_entries.html', {'entries': entries, 'profile': profile_model, 'results': results, 'form': entry_search_form, 'star': star})


@login_required
def zen_page_view(request):
    if request.POST.get('hours') is not None and (request.method == 'POST'):
        print('zen')
        zen_model = Zen.objects.get(user=request.user)
        zen_model.time += request.POST.get('time')
        zen_model.save()
        return HttpResponse(json.dumps(1), content_type='application/json')
    return render(request, 'journal/zen.html')


@login_required
def disable_view(request, id):
    entry_model = Entry.objects.get(id=id)
    entry_model.activated = False
    entry_model.save()
    cache.delete(constants.ALL_ENTRIES_UNFILTERED_CACHE_KEY)
    cache.delete(constants.ALL_ENTRIES_STARRED_CACHE_KEY)
    return redirect('all_entries')


@login_required
def star_view(request, id):
    entry_model = Entry.objects.get(id=id)
    entry_model.starred = not entry_model.starred
    entry_model.save()
    cache.delete(constants.ALL_ENTRIES_STARRED_CACHE_KEY)
    return redirect('post', id=id)


def autocomplete(request):
    if 'term' in request.GET:
        queries = Entry.objects.filter(title__icontains=request.GET.get('term'))
        titles = list()
        for query in queries:
            titles.append(query.title)
        # JsonResponse expects a dict but since it gets a list, safe is False
        return JsonResponse(titles, safe=False)
    return render(request, 'journal/all_entries.html')


def journal_navbar(request):
    display = True if str(request.user) != 'AnonymousUser' else False
    recaptcha_key = None
    if 'signup/' in request.path:
        recaptcha_key = settings.RECATCHA_PUBLIC_KEY
    return {'display': display, 'user': request.user, 'key': recaptcha_key}
