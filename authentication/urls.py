from django.urls import path

from authentication import views

urlpatterns = [
    path('', view=views.index_page_view, name='index'),
    path('signup/', view=views.signup_page_view, name='signup'),
    path('login/', view=views.login_page_view, name='login'),
    path('logout/', view=views.logout_page_view, name='logout'),
    path('services/', view=views.services_page_view, name='services'),
    path('help/', view=views.help_page_view, name='help'),
    path('demo/', view=views.demo_page_view, name='demo'),
    path('profile/', view=views.profile_page_view, name='profile'),
    path('profile/edit/', view=views.profile_edit_page_view, name='profile_edit'),
    path('profile/edit/recommendations/<pk>/', view=views.RecommendationPageView.as_view(), name='recommendations_edit'),
    path('profile/settings/', view=views.settings_page_view, name='settings'),
    path("password_reset/", view=views.password_reset_page_view, name="password_reset"),
    path('password_change/', view=views.password_change_page_view, name='password_change'),
    path('account_activation_sent/', view=views.account_activation_sent_page_view, name='account_activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>/', view=views.activate_view, name='activate'),
]
