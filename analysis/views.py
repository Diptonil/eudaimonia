from django.shortcuts import redirect, render
from django.db.models import Sum

from authentication.models import Profile
from analysis.models import EmotionsStat, RegularityStat
from analysis.forms import QuestionnaireForm


def stats_page_view(request):
    emotion_data = dict()
    emotion_data_last = dict()
    emotion_data_weekly = dict()
    emotion_data_monthly = dict()
    total_entries = EmotionsStat.objects.filter(user=request.user).count()
    regularity_model = RegularityStat.objects.filter(user=request.user)
    regularity_model_x, regularity_model_y = list(), list()
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
    context = {'emotion_data': emotion_data, 'emotion_data_weekly': emotion_data_weekly, 'emotion_data_monthly': emotion_data_monthly, 'emotion_data_last': emotion_data_last, 'regularity_model_len': regularity_model_len, 'regularity_model': regularity_model, 'regularity_model_x': regularity_model_x, 'regularity_model_y': regularity_model_y}
    return render(request, 'analysis/stats.html', context=context)


def quiz_page_view(request):
    profile_model = Profile.objects.get(user=request.user)
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
            profile_model.personality = personality
            profile_model.save()
            return redirect('profile_edit')
    return render(request, 'analysis/quiz.html', {'profile_model': profile_model, 'form': question_form})


def suggestions_page_view(request):
    pass
