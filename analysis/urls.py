from django.urls import path

from analysis import views

urlpatterns = [
    path('', view=views.stats_page_view, name='stats'),
    path('quiz/', view=views.quiz_page_view, name='quiz'),
]