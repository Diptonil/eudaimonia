from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('journal/', include('journal.urls')),
    path('analysis/', include('analysis.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authentication/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'authentication.views.handler404'
handler500 = 'authentication.views.handler500'
handler403 = 'authentication.views.handler403'
handler400 = 'authentication.views.handler400'
