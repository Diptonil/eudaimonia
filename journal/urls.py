from django.urls import path

from journal import views

urlpatterns = [
    path('', view=views.journal_page_view, name='journal'),
    path('stats', view=views.stats_page_view, name='stats'),
    path('entry/', view=views.entry_page_view, name='entry'),
    path('entry/pdf/<text>/<filename>/', view=views.pdf_convert, name='pdf'),
    path('entry/delete/<id>/', view=views.disable_view, name='disable'),
    path('entry/star/<id>/', view=views.star_view, name='star'),
    path('entry/all/', view=views.all_entries_page_view, name='all_entries'),
    path('entry/all/<star>/', view=views.all_entries_page_view, name='star_entries'),
    #path('entry/recommendations', view=views.recommendation_page_view, name='recommendations'),
    path('entry/<id>/', view=views.post_page_view, name='post'),
    #path('entry/<id>/recommendations', view=views.recommendation_page_view, name='recommendations'),
    path('autocomplete/', view=views.autocomplete, name='autocomplete'),
]
