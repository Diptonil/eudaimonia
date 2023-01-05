import hashlib
import json
import random

import requests
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings

import constants
from authentication.models import Profile
from journal.forms import EntrySearchForm
from journal.models import Entry, Zen
from analysis.models import EmotionsStat, Incentive


@login_required
def journal_page_view(request):
    profile_model = Profile.objects.get(user=request.user)
    entry_model = Entry.objects.filter(user=request.user).first()
    count = Entry.objects.filter(user=request.user).count()
    return render(request, 'journal/journal.html', {'profile': profile_model, 'entry_model': entry_model, 'quotes': constants.QUOTES[random.randint(0, 9)], 'count': count})


@login_required
def entry_page_view(request):
    profile_model = Profile.objects.get(user=request.user)
    # Hide 53 and 69 as environment variables!
    if request.POST.get('content') is not None and (request.method == 'POST'):
        title = str(request.POST.get('title'))
        content = str(request.POST.get('content'))
        # content.replace('&nbsp;', '')
        content.replace( '/(<([^>]+)>)/ig', '');
        Entry.objects.create(user=request.user, entry=content, title=title).save()
        print(content)
        return HttpResponse(json.dumps(1), content_type='application/json')
    return render(request, 'journal/entry.html', {'profile': profile_model})


@login_required
def post_page_view(request, id):
    profile_model = Profile.objects.get(user=request.user)
    entry_model = Entry.objects.get(id=id)
    star = entry_model.starred
    if request.POST.get('content') is not None and (request.method == 'POST'):
        content = str(request.POST.get('content'))
    # content.replace( '/(<([^>]+)>)/ig', '');
    # content = entry_model.entry[2:-1]
        entry_model.entry = content
    return render(request, 'journal/post.html', {'entry': entry_model, 'star': star, 'profile': profile_model})


@login_required
def all_entries_page_view(request, star=None):
    entry_search_form = EntrySearchForm()
    incentive_model = Incentive.objects.get(user=request.user)
    entries = Entry.objects.filter(user=request.user).filter(activated=True)
    if star is not None:
        entries = entries.filter(starred=True)
    profile_model = Profile.objects.get(user=request.user)
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
    return redirect('all_entries')


@login_required
def star_view(request, id):
    entry_model = Entry.objects.get(id=id)
    entry_model.starred = not entry_model.starred
    entry_model.save()
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
