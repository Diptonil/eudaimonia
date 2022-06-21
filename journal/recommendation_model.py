import random
import re

from bs4 import BeautifulSoup as SOUP
import requests as HTTP


def predict_movies(liked, disliked, mood):
    if 'negative' in mood:
        emotion_sadness = mood.get('sadness')
        emotion_disgust = mood.get('disgust')
        emotion_anger = mood.get('anger')
        emotion_fear = mood.get('fear')
        emotion_list_raw = sorted([rate for rate in [emotion_sadness, emotion_anger, emotion_disgust, emotion_fear] if rate is not None], reverse=True)
        print(emotion_list_raw)
    elif 'positive' in mood:
        emotion_joy = mood['joy']
        emotion_trust = mood['trust']
        emotion_list_raw = sorted([rate for rate in [emotion_joy, emotion_trust] if rate is not None], reverse=True)
    genres = ['Western', 'Musical', 'Action', 'Thriller', 'Romance', 'Mystery', 'Horror', 'Fantasy', 'Drama', 'Comedy']
    final_genre = list()
    for genre in genres:
        if genre not in disliked:
            final_genre.append(genre)
    genre = final_genre
    for genre in genres:
        if genre in liked:
            final_genre.append(genre)
    if emotion_list_raw[0] == 'sadness':
        try:
            final_genre.remove('Drama')
            final_genre.remove('Horror')
        except ValueError:
            pass
    genre_chosen = random.choice(final_genre)
    url = 'http://www.imdb.com/search/title?genres=%s&title_type=feature&sort=moviemeter, asc' % (genre_chosen)

    response = HTTP.get(url)
    data = response.text
    soup = SOUP(data, "lxml")
    titles = soup.find_all("a", attrs={"href": re.compile(r'\/title\/tt+\d*\/')}, limit=7)
    list_of_inner_text = [x.text for x in titles]
    final_text = list()
    for text in list_of_inner_text:
        if ('X' != text):
            final_text.append(text)
        elif (' \n' != text):
            final_text.append(text)
    return final_text


def predict_music(liked, disliked, mood):
    if 'negative' in mood:
        emotion_sadness = mood.get('sadness')
        emotion_disgust = mood.get('disgust')
        emotion_anger = mood.get('anger')
        emotion_fear = mood.get('fear')
        emotion_list_raw = sorted([rate for rate in [emotion_sadness, emotion_anger, emotion_disgust, emotion_fear] if rate is not None], reverse=True)
        print(emotion_list_raw)
    elif 'positive' in mood:
        emotion_joy = mood['joy']
        emotion_trust = mood['trust']
        emotion_list_raw = sorted([rate for rate in [emotion_joy, emotion_trust] if rate is not None], reverse=True)
    genres = ['country', 'classical', 'dance', 'blues', 'drill', 'dubstep', 'electronic', 'folk', 'funk', 'garage', 'indie',
              'hiphop', 'house', 'metal', 'jazz', 'kpop', 'pop', 'punk', 'psychedelic', "rap", 'rock', 'reggae', 'soul']
    final_genre = list()
    for genre in genres:
        if genre not in disliked:
            final_genre.append(genre)
    genre = final_genre
    for genre in genres:
        if genre in liked:
            final_genre.append(genre)
    genre_chosen = random.choice(final_genre)
    url = 'https://musicstax.com/search/advanced?genres%5B%5D=' + genre_chosen + '&min_bpm=&max_bpm=&key=-1'
    response = HTTP.get(url)
    data = response.text
    soup = SOUP(data, "lxml")
    titles = soup.find_all("u", limit=50)
    list_of_inner_text = [x.text for x in titles]
    list_of_inner_text = list_of_inner_text[15:20]
    final_text = list()
    for text in list_of_inner_text:
        if ('X' != text):
            final_text.append(text)
        elif (' \n' != text):
            final_text.append(text)
    print(final_text)
    print(genre_chosen)
    return final_text


test = {'disgust': 0.2,  'negative': 0.2, 'fear': 0.2, 'anger': 0.2, 'response': 'Success'}
predict_music(['pop', 'rock', 'dance', 'dubstep', 'jazz'], ['metal', 'comedy', 'horror'], test)
