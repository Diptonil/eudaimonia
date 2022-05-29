from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from authentication.models import Profile
from .models import Post
from .forms import EntrySearchForm, PostForm


@login_required
def dashboard_page_view(request):
    entry_search_form = EntrySearchForm()
    post_model = Post.objects.all()
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
    return render(request, 'dashboard/dashboard.html', {'profile': profile_model, 'page_obj': page_obj, 'form': entry_search_form})


@login_required
def story_page_view(request, id):
    story = Post.objects.get(id=id)
    profile_model = Profile.objects.get(user=request.user)
    return render(request, 'dashboard/story.html', {'story': story, 'profile': profile_model})


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
    return render(request, 'dashboard/dashboard.html', {'profile': profile_model, 'page_obj': page_obj, 'form': entry_search_form})
