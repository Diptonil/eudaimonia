import datetime

from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from authentication.models import Profile
from dashboard.models import Post, Story
from dashboard.forms import EntrySearchForm, PostForm
from analysis.models import RegularityStat, Incentive


@login_required
def dashboard_page_view(request):
    recent_regularity = RegularityStat.objects.filter(user=request.user)
    incentive_model = Incentive.objects.get(user=request.user)
    # Streak break logic
    if len(recent_regularity) != 0:
        if recent_regularity.first().date != datetime.date.today():
            RegularityStat.objects.create(user=request.user, streak=recent_regularity.first().streak + 1, date=datetime.date.today())
        streak = recent_regularity.first().streak
        if streak > 2 and streak < 7:
            incentive_model.logger1 = True
            incentive_model.save()
        elif streak > 6 and streak < 14:
            incentive_model.logger2 = True
            incentive_model.save()
        elif streak > 13 and streak < 30:
            incentive_model.logger3 = True
            incentive_model.save()
        elif streak > 29 and streak < 90:
            incentive_model.logger4 = True
            incentive_model.save()
        elif streak == 91:
            incentive_model.logger5 = True
            incentive_model.save()
    else:
        RegularityStat.objects.create(user=request.user, streak=1, date=datetime.date.today())
    entry_search_form = EntrySearchForm()
    post_model = Post.objects.all()
    post_model_self = Post.objects.filter(user=request.user).count()
    if post_model_self == 1:
        incentive_model.storyteller1 = True
        incentive_model.save()
    if post_model_self == 3:
        incentive_model.storyteller2 = True
        incentive_model.save()
    paginator = Paginator(post_model, 5)
    page_obj = paginator.get_page(request.GET.get('page'))
    profile_model = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        entry_search_form = EntrySearchForm(request.POST)
        if entry_search_form.is_valid():
            search = entry_search_form.cleaned_data['search']
            if search is not None:
                results = Post.objects.filter(title__icontains=search)
                paginator = Paginator(results, 5)
                page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/dashboard.html', {'profile': profile_model, 'page_obj': page_obj, 'form': entry_search_form, 'my_shares': False})


@login_required
def share_page_view(request):
    post_form = PostForm()
    profile_model = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            title = post_form.cleaned_data['title']
            post = post_form.cleaned_data['post']
            image = post_form.cleaned_data.get('image')
            if image is None:
                Post.objects.create(user=request.user, post=post, title=title).save()
            else:
                Post.objects.create(user=request.user, post=post, title=title, image=image).save()
            return redirect('dashboard')
    return render(request, 'dashboard/share.html', {'profile': profile_model, 'form': post_form})


@login_required
def my_share_page_view(request):
    entry_search_form = EntrySearchForm()
    post_model = Post.objects.filter(user=request.user)
    paginator = Paginator(post_model, 5)
    page_obj = paginator.get_page(request.GET.get('page'))
    profile_model = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        entry_search_form = EntrySearchForm(request.POST)
        if entry_search_form.is_valid():
            search = entry_search_form.cleaned_data['search']
            if search is not None:
                results = Post.objects.filter(title__icontains=search)
                paginator = Paginator(results, 5)
                page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/dashboard.html', {'profile': profile_model, 'page_obj': page_obj, 'form': entry_search_form, 'my_shares': True})


@login_required
def story_page_view(request):
    entry_model = Story.objects.all()
    return render(request, 'dashboard/story.html', {'entry_model': entry_model})
