from django.urls import path

from analysis import views

urlpatterns = [
    path('', view=views.stats_page_view, name='stats'),
    path('quiz/', view=views.quiz_page_view, name='quiz'),
    path('incentives/', view=views.incentives_page_view, name='incentives'),
    path('suggestions/', view=views.suggestions_page_view, name='suggestions'),
]
