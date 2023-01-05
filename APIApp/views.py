from django.shortcuts import render
from django.http import HttpResponse
import json
import os
from google.cloud import language
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"eudaimonia-372006-413e2d2c4899.json"
# Exempting the csrf token
@csrf_exempt
def sentimentAnalysis(request):
    if request.method == "POST":
        text = request.POST["text"]
        client = language.LanguageServiceClient()
        document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
        response = client.analyze_sentiment(document=document)
        sentiment = response.document_sentiment
        results = dict(
            text=text,
            score=f"{sentiment.score:.1%}",
            magnitude=f"{sentiment.magnitude:.1%}",
        )
        if "-" in results["score"]:
            return HttpResponse(json.dumps(f"Negative Sentiment with Score: {results['score']}")) 
        return HttpResponse(json.dumps(f"Positive Sentiment with Score: {results['score']}"))
