import random
import json

import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
from django.shortcuts import redirect, render
from django.db.models import Sum

from authentication.models import Profile
from analysis.models import EmotionsStat, RegularityStat, Incentive
from journal.models import Zen
from analysis.forms import QuestionnaireForm


def stats_page_view(request):
    emotion_data = dict()
    emotion_data_last = dict()
    emotion_data_weekly = dict()
    emotion_data_monthly = dict()
    total_entries = EmotionsStat.objects.filter(user=request.user).count()
    regularity_model = RegularityStat.objects.filter(user=request.user)
    regularity_model_x, regularity_model_y = list(), list()
    zen_model = Zen.objects.get(user=request.user)
    for x in regularity_model.iterator():
        regularity_model_x.append(x.date.day)
    for y in regularity_model.iterator():
        regularity_model_y.append(float(y.time_spent))
    regularity_model_len = regularity_model.count()
    if total_entries > 0:
        emotion_queryset = EmotionsStat.objects.filter(user=request.user)
        emotion_data['Happy'] = float(emotion_queryset.aggregate(Sum('happy'))['happy__sum'])
        emotion_data['Angry'] = float(emotion_queryset.aggregate(Sum('angry'))['angry__sum'])
        emotion_data['Sad'] = float(emotion_queryset.aggregate(Sum('sad'))['sad__sum'])
        emotion_data['Surprise'] = float(emotion_queryset.aggregate(Sum('surprise'))['surprise__sum'])
        emotion_data['Fear'] = float(emotion_queryset.aggregate(Sum('fear'))['fear__sum'])
        emotion_queryset_last = EmotionsStat.objects.filter(user=request.user).first()
        emotion_data_last['Happy'] = float(emotion_queryset_last.happy)
        emotion_data_last['Angry'] = float(emotion_queryset_last.angry)
        emotion_data_last['Sad'] = float(emotion_queryset_last.sad)
        emotion_data_last['Surprise'] = float(emotion_queryset_last.surprise)
        emotion_data_last['Fear'] = float(emotion_queryset_last.fear)
        print(emotion_data_last)
    if total_entries >= 3:
        emotion_queryset_weekly = EmotionsStat.objects.filter(user=request.user)[:7]
        emotion_data_weekly['Happy'] = float(emotion_queryset_weekly.aggregate(Sum('happy'))['happy__sum'])
        emotion_data_weekly['Angry'] = float(emotion_queryset_weekly.aggregate(Sum('angry'))['angry__sum'])
        emotion_data_weekly['Sad'] = float(emotion_queryset_weekly.aggregate(Sum('sad'))['sad__sum'])
        emotion_data_weekly['Surprise'] = float(emotion_queryset_weekly.aggregate(Sum('surprise'))['surprise__sum'])
        emotion_data_weekly['Fear'] = float(emotion_queryset_weekly.aggregate(Sum('fear'))['fear__sum'])
    if total_entries >= 7:
        emotion_queryset_monthly = EmotionsStat.objects.filter(user=request.user)[:30]
        emotion_data_monthly['Happy'] = float(emotion_queryset_monthly.aggregate(Sum('happy'))['happy__sum'])
        emotion_data_monthly['Angry'] = float(emotion_queryset_monthly.aggregate(Sum('angry'))['angry__sum'])
        emotion_data_monthly['Sad'] = float(emotion_queryset_monthly.aggregate(Sum('sad'))['sad__sum'])
        emotion_data_monthly['Surprise'] = float(emotion_queryset_monthly.aggregate(Sum('surprise'))['surprise__sum'])
        emotion_data_monthly['Fear'] = float(emotion_queryset_monthly.aggregate(Sum('fear'))['fear__sum'])
    context = {'zen_model': zen_model, 'emotion_data': emotion_data, 'emotion_data_weekly': emotion_data_weekly, 'emotion_data_monthly': emotion_data_monthly, 'emotion_data_last': emotion_data_last, 'regularity_model_len': regularity_model_len, 'regularity_model': regularity_model, 'regularity_model_x': regularity_model_x, 'regularity_model_y': regularity_model_y}
    return render(request, 'analysis/stats.html', context=context)


def quiz_page_view(request):
    profile_model = Profile.objects.get(user=request.user)
    incentive_model = Incentive.objects.get(user=request.user)
    question_form = QuestionnaireForm()
    if request.method == 'POST':
        question_form = QuestionnaireForm(request.POST)
        if question_form.is_valid():
            q1 = question_form.cleaned_data['q1']
            q2 = question_form.cleaned_data['q2']
            q3 = question_form.cleaned_data['q3']
            q4 = question_form.cleaned_data['q4']
            q5 = question_form.cleaned_data['q5']
            q6 = question_form.cleaned_data['q6']
            q7 = question_form.cleaned_data['q7']
            q8 = question_form.cleaned_data['q8']
            q9 = question_form.cleaned_data['q9']
            q10 = question_form.cleaned_data['q10']
            q11 = question_form.cleaned_data['q11']
            q12 = question_form.cleaned_data['q12']
            q13 = question_form.cleaned_data['q13']
            q14 = question_form.cleaned_data['q14']
            q15 = question_form.cleaned_data['q15']
            q16 = question_form.cleaned_data['q16']
            q17 = question_form.cleaned_data['q17']
            q18 = question_form.cleaned_data['q18']
            q19 = question_form.cleaned_data['q19']
            q20 = question_form.cleaned_data['q20']
            IN, E, S, N, T, F, J, P = 0, 0, 0, 0, 0, 0, 0, 0
            for e in [q1, q5, q9, q13, q17]:
                if e == '1':
                    E += 1
                else:
                    IN += 1
            for e in [q2, q6, q10, q14, q18]:
                if e == '1':
                    S += 1
                else:
                    IN += 1
            for e in [q3, q7, q11, q15, q19]:
                if e == '1':
                    T += 1
                else:
                    F += 1
            for e in [q4, q8, q12, q16, q20]:
                if e == '1':
                    J += 1
                else:
                    P += 1
            personality = str('I' if IN > E else 'E') + str('S' if S > N else 'N') + str('T' if T > F else 'F') + str('J' if J > P else 'P')
            print(personality)
            incentive_model.registrar = True
            profile_model.personality = personality
            profile_model.save()
            incentive_model.save()
            return redirect('profile_edit')
    return render(request, 'analysis/quiz.html', {'profile_model': profile_model, 'incentive_model': incentive_model, 'form': question_form})


def incentives_page_view(request):
    incentives_model = Incentive.objects.get(user=request.user)
    return render(request, 'analysis/incentives.html', {'incentives_model': incentives_model})


def suggestions_page_view(request):
    client_id = "e44153c1ff784cdba2fc350901f0e541"
    client_secret = "86bbb41614534aebb81180548c25f02f"
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 
    headers = {'Authorization': 'Api-Key %s' % 'WNTDnKHs.bd9VaRno8zsc2S6r4l4owTFgLBnijakI'}
    
    profile_model = Profile.objects.get(user=request.user)
    hobby = [obj[0] for obj in Profile.objects.get(user=request.user).hobby.values_list('field')]
    model_favourite_movie_genres = [obj[0] for obj in profile_model.fav_movie_genres.values_list('field')]
    model_unfavourite_movie_genres = [obj[0] for obj in profile_model.unfav_movie_genres.values_list('field')]
    favourites = profile_model.fav_movie
    emotion = EmotionsStat.objects.filter(user=request.user).first().emotion
    json_data = {'LIKED_MOVIE_GENRES': model_favourite_movie_genres, 'DISLIKED_MOVIE_GENRES': model_unfavourite_movie_genres, 'FAVOURITE_MOVIES': favourites, 'MOOD': emotion}
    generalized_suggestions1, generalized_suggestions2, generalized_suggestions3, generalized_suggestions4 = [], [], [], []
    response = requests.post('http://127.0.0.1:7000/api/v1/get_movie/', json=json_data, headers=headers).json()
    failure = False
    if (not profile_model.personality) or profile_model.personality == '':
        failure = True
    if emotion == 'Sad':
        if 'I' in profile_model.personality:
            generalized_suggestions1.append('The immediate thing that you might want to avoid is following the urge to \
                be in extroverted environments just because others are doing so as well. You know what makes you comfortable.\
                Better stick to that.')
            generalized_suggestions1.append('A lot of grief comes from unresolved issues that you might be putting underneath \
                some cover to avoid feeling them. Either encounter those issues head on, resolve them or try to let go.')
            generalized_suggestions1.append('If you\'re hungry, enjoy a solitary meal and watch your favourite show or try \
                watching certain movies.')
            generalized_suggestions1.append('Spend time with someone who is very close to you. Avoid people around whom you do \
                not want to be.')
            generalized_suggestions1.append('When something bad happens, almost everything seems to fall apart. You start \
                disliking yourself for more reasons than you actually were upset about in the first place. At such moments, shut \
                your mind off and do not think.')
        elif 'E' in profile_model.personality:
            generalized_suggestions1.append('Unless you are extremely upset or angry, you may not want to stay alone at such \
                times. Get together with certain close friends or a group to talk it out until it makes you feel good.')
            generalized_suggestions1.append('You might want to be around people who approve or value your sense of independence \
                and respect it.')
            generalized_suggestions1.append('Catch up with old friends.')
            generalized_suggestions1.append('Go to a place that holds good memories with the same people with whom you had been there \
                before.')
            generalized_suggestions1.append('Do something that you\'re very good or familiar with.')
        if 'S' in profile_model.personality:
            generalized_suggestions2.append('If there is an instance in which you\'re sensing disapproval from people around you, \
                talk to them to understand what is happening.')
            generalized_suggestions2.append('You might need to cut loose company that have grown undesirable and insensible towards you.')
            generalized_suggestions2.append('You might want to consider not to rethink things when they have a pretty clear outcome.')
        elif 'N' in profile_model.personality:
            generalized_suggestions2.append('Consider the worst case scenario for the actions that you are taking and weigh the pros and cons.')
            generalized_suggestions2.append('In case your instincts fail you, it is worth knowing that it is okay to make mistakes. \
                You\'re the only person knowing the best about yourself and so you should never stop trusting yourself.')
            generalized_suggestions2.append('If you\'re feeling conflicted about something, it may be better to trust your gut-feeling \
                because if you don\'t, it might result in disappointment because you didn\'t follow what you wanted to.')
        if 'T' in profile_model.personality:
            generalized_suggestions3.append('At times you may be overthinking things. Quieten down your mind and don\'t think \
                about what might take place. Focus on your present more.')
            generalized_suggestions3.append('Whatever you are thinking, try writing about it. It may make it easier for you \
                to analyse things.')
            generalized_suggestions3.append('Whatever you\'re thinking, talk about it to your close ones.')
        elif 'F' in profile_model.personality:
            generalized_suggestions3.append('Instead of keeping your feelings to yourself, try expressing it.')
            generalized_suggestions3.append('Whatever you are thinking may be just an exaggeration of how things are at present. \
                Try to not let feelings get the better of your rationality.')
            generalized_suggestions3.append('Whatever you are feeling, try writing about it. It may make it easier for you \
                to deal with it.')
        if 'J' in profile_model.personality:
            generalized_suggestions4.append('You should remind yourself that whatever you are facing would be something that \
                you can easily move past by having faith in yourself and your judgements.')
            generalized_suggestions4.append('You might want to have an open mind about things in case the people closest \
                to you have second thoughts about your decisions.')
            generalized_suggestions4.append('It might have been that your judgements were probably correct. It was just a certain \
                circumstance that made things unfavourable.')
        elif 'P' in profile_model.personality:
            generalized_suggestions4.append('A few minor setbacks shouldn\'t affect your accuracy of perception.')
            generalized_suggestions4.append('Your ability to take decisions and percieve makes you unique and therefore should \
                not discourage you to do the same.')
            generalized_suggestions4.append('It is your mistakes that would make you better and sharpen your perception skills.')
    elif emotion == 'Happy':
        if 'I' in profile_model.personality:
            generalized_suggestions1.append('Make an attempt to expand your comfort zone by trying to befriend new people.')
            generalized_suggestions1.append('Try to help people around you and appreciate their presence in your life.')
            generalized_suggestions1.append('Try to do away with piled up work and maintain productivity.')
        elif 'E' in profile_model.personality:
            generalized_suggestions1.append('Try to do away with piled up work and maintain productivity.')
            generalized_suggestions1.append('Try starting social work or community service if the workload you have is considerably low.')
            generalized_suggestions1.append('Try enjoying solitude by allowing yourself to spend time alone without much distractions.')
        if 'S' in profile_model.personality:
            generalized_suggestions2.append('Hold on to the feeling of joy & cherish it as much as you can.')
            generalized_suggestions2.append('Try re-establishing old bonds with people with whom connections have dulled.')
            generalized_suggestions2.append('Try talking or expressing whatever you are feeling in words.')
        elif 'N' in profile_model.personality:
            generalized_suggestions2.append('As obvious, your instincts hardly ever let you down. You may want to continue that.')
            generalized_suggestions2.append('Give other people in life a chance to take over the wheel to not tire yourself out completely.')
            generalized_suggestions2.append('Improve your skills to tackle conditions needing knowledge and logic.')
        if 'T' in profile_model.personality:
            generalized_suggestions3.append('You can try out hobbies such as getting into chess, solving sudokus, etc.')
            generalized_suggestions3.append('Try to expend your new-found energies into innovation and formulation of something new.')
            generalized_suggestions3.append('You should try to be as productive as you can.')
        elif 'F' in profile_model.personality:
            generalized_suggestions3.append('you can try out hobbies such as reading books, learning a new language, etc.')
            generalized_suggestions3.append('Try to expend your new-found energies into creation and design of something new.')
            generalized_suggestions3.append('Try to weigh the pros and cons of doing a certain action before excitedly pursuing it.')
        if 'J' in profile_model.personality:
            generalized_suggestions4.append('Spend time with close ones without offering much scrutiny.')
            generalized_suggestions4.append('Try out new things and experiences and gauge how they make you feel.')
            generalized_suggestions4.append('Increase your knowledge of various other topics by learning or researching more.')
        elif 'P' in profile_model.personality:
            generalized_suggestions4.append('Spend some time by letting your hair down for a bit and without much worries.')
            generalized_suggestions4.append('Give more chances to the things you\'ve been avoiding to deal with.')
            generalized_suggestions4.append('Experience more things to deepen your perception and understanding of things.')
    final_result = [generalized_suggestions1[random.randint(0, 2)], generalized_suggestions2[random.randint(0, 2)], generalized_suggestions3[random.randint(0, 2)], generalized_suggestions4[random.randint(0, 2)]]

    model_favourite_music_genres = [obj[0] for obj in profile_model.fav_music_genres.values_list('field')]
    track = sp.search(q='genre:' + model_favourite_music_genres[random.randint(0, 2)], type='track', market='GB', limit=1, offset=0)['tracks']['items'][0]['name']
    artist = sp.search(q='genre:' + model_favourite_music_genres[random.randint(0, 2)], type='track', market='GB', limit=1, offset=0)['tracks']['items'][0]['artists'][0]['name']
    return render(request, 'analysis/suggestions.html', {'profile_model': profile_model.personality, 'track': track, 'artist': artist, 'failure': failure, 'hobby': hobby, 'final_result': final_result, 'response': response})
