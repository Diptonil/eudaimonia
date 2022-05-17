from django.test import TestCase
from authentication.forms import SignupForm, LoginForm, ProfileForm
from django.contrib.auth import get_user_model
from pathlib import Path
from django.core.files import File
import sys
sys.path.append("..")


class SignupFormTest(TestCase):

    def setUp(self):
        self.form = SignupForm(data={'username': 'TestUser', 'email': 'test@user.com', 'first_name': 'Test', 'last_name': 'User', 'password1': 'Password%420', 'password2': 'Password%420'})

    def test_form_validity(self):
        self.assertTrue(self.form.is_valid())

    def test_form_invalidity_by_no_entries(self):
        wrong_form = SignupForm(data={'username': '', 'email': '', 'first_name': '', 'last_name': '', 'password1': '', 'password2': ''})
        self.assertEqual(len(wrong_form.errors), 6)
        self.assertFalse(wrong_form.is_valid())

    def test_form_invalidity_by_spaces_in_username(self):
        self.form.data['username'] = 'Test User'
        self.assertEqual(len(self.form.errors), 1)
        self.assertFalse(self.form.is_valid())
        self.assertIn('Enter a valid username.', str(self.form.errors['username'].as_data()))

    def test_form_invalidity_by_at_in_email(self):
        self.form.data['email'] = 'test@test'
        self.assertEqual(len(self.form.errors), 1)
        self.assertFalse(self.form.is_valid())
        self.assertIn('Enter a valid email address.', str(self.form.errors['email'].as_data()))


class LoginFormTest(TestCase):

    def setUp(self):
        get_user_model().objects.create_user('TestUser', email='test@user.com', password='Password%420')
        self.form1 = LoginForm(data={'user_identifier': 'TestUser', 'password': 'Password%420'})
        self.form2 = LoginForm(data={'user_identifier': 'test@user.com', 'password': 'Password%420'})

    def test_form_validity(self):
        self.assertTrue(self.form1.is_valid())
        self.assertTrue(self.form2.is_valid())

    def test_form_invalidity_by_no_entries(self):
        wrong_form = LoginForm(data={'user_identifier': '', 'password': ''})
        self.assertEqual(len(wrong_form.errors), 2)
        self.assertFalse(wrong_form.is_valid())

    def test_form_invalidity_by_wrong_entries(self):
        pass


class ProfileFormTest(TestCase):

    def setUp(self):
        path = Path('C:/Users/rupam/Desktop/Wayne.private/Programming/Python/Projects/Django/eudaimonia/tests/Test Resources/Leonard Cohen.webp')
        get_user_model().objects.create_user('TestUse', email='test@user.com', password='Password%420')
        f = path.open('rb')
        image = File(f, name=path.name)
        f.close()
        self.form1 = ProfileForm(data={'bio': 'TestUser', 'birth_date': '01/01/2000', 'image': image})
        self.form2 = ProfileForm(data={'bio': None, 'birth_date': None, 'image': None})
        self.form3 = ProfileForm(data={'bio': 'TestUser', 'birth_date': '01/01/20000', 'image': image})

    def test_form_validity(self):
        self.assertTrue(self.form1.is_valid())
        self.assertTrue(self.form2.is_valid())

    def test_form_invalidity_by_wrong_entries(self):
        self.assertFalse(self.form3.is_valid())
