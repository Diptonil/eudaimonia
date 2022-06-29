from django.shortcuts import redirect, render

from authentication.models import Profile
from analysis.forms import QuestionnaireForm


def stats_page_view(request):
    return render(request, 'analysis/stats.html')


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
            I, E, S, N, T, F, J, P = 0, 0, 0, 0, 0, 0, 0, 0
            for e in [q1, q5, q9, q13, q17]:
                print(type(e))
                if e == '1':
                    E += 1
                else:
                    I += 1
                print(I, E)
            for e in [q2, q6, q10, q14, q18]:
                if e == '1':
                    S += 1
                else:
                    N += 1
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
            personality = str('I' if I > E else 'E') + str('S' if S > N else 'N') + str('T' if T > F else 'F') + str('J' if J > P else 'P')
            print(personality)
            profile_model.personality = personality
            profile_model.save()
            return redirect('profile_edit')
    return render(request, 'analysis/quiz.html', {'profile_model': profile_model, 'form': question_form})


def suggestions_page_view(request):
    pass
