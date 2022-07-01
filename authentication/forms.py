from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from authentication.models import Profile


class SignupForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].widget.attrs.update({'name': "username", 'placeholder': "Username", "autocomplete": "false"})
        self.fields['first_name'].widget.attrs.update({'name': "first_name", 'placeholder': "First Name", "autocomplete": "false"})
        self.fields['last_name'].widget.attrs.update({'name': "last_name", 'placeholder': "Last Name", "autocomplete": "false"})
        self.fields['email'].widget.attrs.update({'name': "email", 'placeholder': "Email", "autocomplete": "false"})
        self.fields['password1'].widget.attrs.update({'name': "password", 'placeholder': "Password", "autocomplete": "off", 'data-toggle': 'password'})
        self.fields['password2'].widget.attrs.update({'name': "rpassword", 'placeholder': "Repeat Password", "autocomplete": "off", 'data-toggle': 'password'})

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if username is not None:
            if '@' in username:
                self.add_error('username', 'The \'@\' character is not allowed.')
            if (username[0] == ('.' or '_')) or (username[-1] == ('.' or '_')):
                self.add_error('username', "Usernames cannot have periods or underscores at the beginning or end.")
            if User.objects.filter(username=username).exists():
                self.add_error('username', 'Username already exists. Please try something else.')
        if email is not None:
            if User.objects.filter(email=email).exists():
                self.add_error('email', 'Email already exists. Please log in instead.')


class LoginForm(forms.Form):

    user_identifier = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'name': "password", 'placeholder': "Password", "autocomplete": "false"})
        self.fields['user_identifier'].widget.attrs.update({'name': "username", 'placeholder': "Username or Email", "autocomplete": "off"})


class ProfileForm(forms.Form):

    image = forms.ImageField(required=False)
    birth_date = forms.DateField(required=False, input_formats=['%d/%m/%Y'])
    bio = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs.update({'id': "bio", 'placeholder': "Tell us about yourself...", "autocomplete": "false"})
        self.fields['birth_date'].widget.attrs.update({'id': "birth-date", "autocomplete": "off"})
        self.fields['image'].widget.attrs.update({'style': "margin-top: 30px"})


class RecommendationForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['hobby', 'fav_movie', 'fav_movie_genres', 'unfav_movie_genres', 'fav_music_genres', 'unfav_music_genres']
