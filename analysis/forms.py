from django import forms


class QuestionnaireForm(forms.Form):

    q1 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q2 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q3 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q4 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q5 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q6 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q7 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q8 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q9 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q10 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q11 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q12 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q13 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q14 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q15 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q16 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q17 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q18 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q19 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
    q20 = forms.ChoiceField(choices=((1, 1), (2, 2)), required=True)
