from django.urls import path
from .views import sentimentAnalysis
urlpatterns = [
    path('sentimentAnalysis', sentimentAnalysis, name="sentimentAnalysis")
]