import hashlib
import json
import io
from reportlab.pdfgen import canvas
from django.http import FileResponse, JsonResponse
from .encryption import encrypt, decrypt
from django.shortcuts import redirect, render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from authentication.models import Profile
from .forms import EntrySearchForm
from .models import Entry


@login_required
def journal_page_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'journal/journal.html', {'profile': profile})


@login_required
def entry_page_view(request):
    profile = Profile.objects.get(user=request.user)
    # Hide 53 and 69 as environment variables!
    if request.POST.get('content') is not None and (request.method == 'POST'):
        title = str(request.POST.get('title'))
        content = str(request.POST.get('content'))
        content.replace('&nbsp;', '')
        key = get_user_model().objects.get(username=request.user.username).password[53:69]
        key = hashlib.sha256(key.encode()).digest()
        content = encrypt(content, key)
        Entry.objects.create(user=request.user, entry=content, title=title).save()
        print(content)
        print(decrypt(content, key))
        return HttpResponse(json.dumps(1), content_type='application/json')
    return render(request, 'journal/entry.html', {'profile': profile})


@login_required
def post_page_view(request, id):
    entry = Entry.objects.get(id=id)
    star = entry.starred
    content = entry.entry[2:-1]
    key = get_user_model().objects.get(username=request.user.username).password[53:69]
    key = hashlib.sha256(key.encode()).digest()
    content = decrypt(content, key)
    entry.entry = content
    if request.method == 'POST':
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, features='html5lib')
        print(soup.get_text().replace('    ', '').replace('\n', ''))
        return redirect('pdf', text=soup.get_text().replace('\t', ' ').replace('\n', ''), filename='{0}.pdf'.format(entry.title))
    return render(request, 'journal/post.html', {'entry': entry, 'star': star})


@login_required
def all_entries_page_view(request, star=None):
    form = EntrySearchForm()
    entries = Entry.objects.filter(user=request.user).filter(activated=True)
    if star is not None:
        entries = entries.filter(starred=True)
    profile = Profile.objects.get(user=request.user)
    results = None
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
        form = EntrySearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search is not None:
                results = Entry.objects.filter(title__icontains=search)
                if star is not None:
                    results = results.filter(starred=True)
    return render(request, 'journal/all_entries.html', {'entries': entries, 'profile': profile, 'results': results, 'form': form, 'star': star})


@login_required
def pdf_convert(request, text, filename):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 100, text)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=filename)


@login_required
def disable_view(request, id):
    entry = Entry.objects.get(id=id)
    entry.activated = False
    entry.save()
    return redirect('all_entries')


@login_required
def star_view(request, id):
    entry = Entry.objects.get(id=id)
    entry.starred = not entry.starred
    entry.save()
    return redirect('post', id=id)


def autocomplete(request):
    if 'term' in request.GET:
        qs = Entry.objects.filter(title__icontains=request.GET.get('term'))
        titles = list()
        for q in qs:
            titles.append(q.title)
        # JsonResponse expects a dict but since it gets a list, safe is False
        return JsonResponse(titles, safe=False)
    return render(request, 'journal/all_entries.html')


def journal_navbar(request):
    display = ('journal/' in request.path) or ('profile/' in request.path) or ('settings/' in request.path)
    key = None
    if 'signup/' in request.path:
        key = settings.RECATCHA_PUBLIC_KEY
    return {'display': display, 'user': request.user, 'key': key}
