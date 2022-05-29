from django.urls import path

from . import views

urlpatterns = [
    path('', view=views.dashboard_page_view, name='dashboard'),
    path('story/<id>', view=views.story_page_view, name='story'),
    path('share/', view=views.share_page_view, name='share'),
    path('share/mine/', view=views.my_share_page_view, name='my_share'),
]
