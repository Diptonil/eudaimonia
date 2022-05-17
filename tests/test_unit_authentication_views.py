from django.http import HttpRequest
from django.test import TestCase, SimpleTestCase, Client
from django.urls import resolve, reverse
from django.contrib.auth import get_user_model
from importlib import import_module
from django.conf import settings
from django.contrib import messages
from authentication import views
import sys

from authentication.models import Profile
sys.path.append("..")


class IndexPageTest(SimpleTestCase):

    def setUp(self):
        self.client = Client()

    def test_url_maps_to_view(self):
        view = resolve('/')
        self.assertEqual(view.func, views.index_page_view)

    def test_view_maps_to_template(self):
        response = self.client.get(reverse('index'), follow=True)
        self.assertTemplateUsed(response, 'authentication/index.html')

    def test_get_request_is_valid(self):
        response = self.client.get(reverse('index'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_request_is_valid(self):
        pass


class ServicesPageTest(SimpleTestCase):

    def setUp(self):
        self.client = Client()

    def test_url_maps_to_view(self):
        view = resolve('/services/')
        self.assertEqual(view.func, views.services_page_view)

    def test_view_maps_to_template(self):
        response = self.client.get(reverse('services'), follow=True)
        self.assertTemplateUsed(response, 'extras/services.html')

    def test_get_request_is_valid(self):
        response = self.client.get(reverse('services'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_request_is_valid(self):
        pass


class LoginPageTest(TestCase):

    def setUp(self):
        self.client = Client()
        # deepcode ignore NoHardcodedPasswords/test: <Test>
        get_user_model().objects.create_user('TestUsername', email='test@user.com', password='TestPassword%420')

    def test_url_maps_to_view(self):
        view = resolve('/login/')
        self.assertEqual(view.func, views.login_page_view)

    def test_view_maps_to_template(self):
        response = self.client.get(reverse('login'), follow=True)
        self.assertTemplateUsed(response, 'authentication/login.html')

    def test_get_request_is_valid(self):
        response = self.client.get(reverse('login'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_request_is_valid(self):
        request = HttpRequest()
        request._messages = messages.storage.default_storage(request)
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        request.method = 'POST'
        request.POST['username'] = 'TestUsername'
        request.POST['password'] = 'TestPassword%420'
        request.user = 'TestUsername'
        request.META['HTTP_HOST'] = 'localhost'
        response = views.login_page_view(request)
        self.assertEqual(response.status_code, 200)
        request.POST['username'] = 'test@user.com'
        response = views.login_page_view(request)
        self.assertEqual(response.status_code, 200)
        request.POST['username'] = 'something invalid'
        response = views.login_page_view(request)
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'The given combination of credentials do not exist. Please recheck your entry.', response.content)


class SignupPageTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_url_maps_to_view(self):
        view = resolve('/signup/')
        self.assertEqual(view.func, views.signup_page_view)

    def test_view_maps_to_template(self):
        response = self.client.get(reverse('signup'), follow=True)
        self.assertTemplateUsed(response, 'authentication/signup.html')

    def test_get_request_is_valid(self):
        response = self.client.get(reverse('signup'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_request_is_valid(self):
        request = HttpRequest()
        request._messages = messages.storage.default_storage(request)
        request.method = 'POST'
        request.POST['username'] = 'TestUsername'
        request.POST['email'] = 'test@email.com'
        request.POST['first_name'] = 'Test'
        request.POST['last_name'] = 'Username'
        request.POST['password1'] = 'TestPassword%420'
        request.POST['password2'] = 'TestPassword%420'
        request.user = 'AnonymousUser'
        request.META['HTTP_HOST'] = 'localhost'
        response = views.signup_page_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.first().username, 'TestUsername')
        self.assertEqual(get_user_model().objects.first().email, 'test@email.com')
        self.assertEqual(get_user_model().objects.first().first_name, 'Test')
        self.assertEqual(get_user_model().objects.first().last_name, 'Username')


class ActivationTest(SimpleTestCase):

    def setUp(self):
        self.client = Client()

    def test_url_maps_to_view(self):
        view = resolve('/activate/wrong/url/')
        self.assertEqual(view.func, views.activate_view)

    def test_view_maps_to_template(self):
        response = self.client.get(reverse('activate', args=['wrong', 'url']), follow=True)
        self.assertTemplateUsed(response, 'authentication/account_activation_invalid.html')

    def test_get_request_is_valid(self):
        response = self.client.get(reverse('activate', args=['wrong', 'url']), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_request_is_valid(self):
        pass


class LogoutPageTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_url_maps_to_view(self):
        view = resolve('/logout/')
        self.assertEqual(view.func, views.logout_page_view)

    def test_view_maps_to_template(self):
        response = self.client.get(reverse('logout'), follow=True)
        self.assertTemplateUsed(response, 'extras/404.html')
        # deepcode ignore NoHardcodedPasswords/test: <Test>
        user = get_user_model().objects.create_user('Test User', password='Test Password')
        self.client.force_login(user=user)
        response = self.client.get(reverse('logout'), follow=True)
        self.assertTemplateUsed(response, 'authentication/index.html')

    def test_get_request_is_valid(self):
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 404)
        # deepcode ignore NoHardcodedPasswords/test: <Test>
        user = get_user_model().objects.create_user('Test User', password='Test Password')
        self.client.force_login(user=user)
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_request_is_valid(self):
        pass


class ProfilePageTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_url_maps_to_view(self):
        view = resolve('/profile/')
        self.assertEqual(view.func, views.profile_page_view)

    def test_view_maps_to_template(self):
        response = self.client.get(reverse('profile'), follow=True)
        self.assertTemplateUsed(response, 'extras/404.html')
        # deepcode ignore NoHardcodedPasswords/test: <Test>
        user = get_user_model().objects.create_user('TestUser', email='test@user.com', password='TestPassword%420')
        self.client.force_login(user=user)
        response = self.client.get(reverse('profile'), follow=True)
        self.assertTemplateUsed(response, 'authentication/profile.html')

    def test_get_request_is_valid(self):
        response = self.client.get(reverse('profile'), follow=True)
        self.assertEqual(response.status_code, 404)
        # deepcode ignore NoHardcodedPasswords/test: <Test>
        user = get_user_model().objects.create_user('TestUser', email='test@user.com', password='TestPassword%420')
        self.client.force_login(user=user)
        response = self.client.get(reverse('profile'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_request_is_valid(self):
        pass


class ProfileEditPageTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_url_maps_to_view(self):
        view = resolve('/profile/edit/')
        self.assertEqual(view.func, views.profile_edit_page_view)

    def test_view_maps_to_template(self):
        response = self.client.get(reverse('profile_edit'), follow=True)
        self.assertTemplateUsed(response, 'extras/404.html')
        # deepcode ignore NoHardcodedPasswords/test: <Test>
        user = get_user_model().objects.create_user('TestUser', email='test@user.com', password='TestPassword%420')
        self.client.force_login(user=user)
        response = self.client.get(reverse('profile_edit'), follow=True)
        self.assertTemplateUsed(response, 'authentication/profile_edit.html')

    def test_get_request_is_valid(self):
        response = self.client.get(reverse('profile_edit'), follow=True)
        self.assertEqual(response.status_code, 404)
        # deepcode ignore NoHardcodedPasswords/test: <Test>
        user = get_user_model().objects.create_user('TestUser', email='test@user.com', password='TestPassword%420')
        self.client.force_login(user=user)
        response = self.client.get(reverse('profile_edit'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_request_is_valid(self):
        # deepcode ignore NoHardcodedPasswords/test: <Test>
        user = get_user_model().objects.create_user('TestUser', email='test@user.com', password='TestPassword%420')
        self.client.force_login(user=user)
        self.client.post('/profile/edit/', data={})
        profile = Profile.objects.first()
        self.assertEqual(profile.bio, None)
        self.assertEqual(profile.birth_date, None)
        self.client.post('/profile/edit/', data={'bio': 'Test Bio', 'birth_date': '01/01/2000'})
        profile = Profile.objects.first()
        self.assertEqual(profile.bio, 'Test Bio')


class PasswordChangePageTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_url_maps_to_view(self):
        view = resolve('/password_change/')
        self.assertEqual(view.func, views.password_change_page_view)

    def test_view_maps_to_template(self):
        response = self.client.get(reverse('password_change'), follow=True)
        self.assertTemplateUsed(response, 'extras/404.html')
        # deepcode ignore NoHardcodedPasswords/test: <Test>
        user = get_user_model().objects.create_user('TestUser', email='test@user.com', password='TestPassword%420')
        self.client.force_login(user=user)
        response = self.client.get(reverse('password_change'), follow=True)
        self.assertTemplateUsed(response, 'authentication/password_change.html')

    def test_get_request_is_valid(self):
        response = self.client.get(reverse('password_change'), follow=True)
        self.assertEqual(response.status_code, 404)
        # deepcode ignore NoHardcodedPasswords/test: <Test>
        user = get_user_model().objects.create_user('TestUser', email='test@user.com', password='TestPassword%420')
        self.client.force_login(user=user)
        response = self.client.get(reverse('password_change'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_request_is_valid(self):
        # deepcode ignore NoHardcodedPasswords/test: <Test>
        user = get_user_model().objects.create_user('TestUser', email='test@user.com', password='TestPassword%420')
        self.client.force_login(user=user)
        password = get_user_model().objects.first().password
        self.client.post('/password_change/', data={'old_password': 'TestPassword%420', 'new_password1': 'TESTING#13', 'new_password2': 'TESTING#13'})
        test_password = get_user_model().objects.first().password
        self.assertNotEqual(password, test_password)
        password = test_password
        self.client.post('/password_change/', data={'old_passwor': 'TESTING#13', 'new_password1': 'TestPassword%420', 'new_password2': 'TestPassword%420'})
        test_password = get_user_model().objects.first().password
        self.assertEqual(password, test_password)
        password = test_password
        self.client.post('/password_change/', data={'old_password': 'TESTING#13', 'new_password1': 'TestPassword%42', 'new_password2': 'TestPassword%420'})
        test_password = get_user_model().objects.first().password
        self.assertEqual(password, test_password)
        password = test_password
        self.client.post('/password_change/', data={'old_password': 'JunkTestValue', 'new_password1': 'TestPassword%420', 'new_password2': 'TestPassword%420'})
        test_password = get_user_model().objects.first().password
        self.assertEqual(password, test_password)


class PasswordChangePageTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_url_maps_to_view(self):
        view = resolve('/settings/')
        self.assertEqual(view.func, views.settings_page_view)

    def test_view_maps_to_template(self):
        response = self.client.get(reverse('settings'), follow=True)
        self.assertTemplateUsed(response, 'extras/404.html')
        # deepcode ignore NoHardcodedPasswords/test: <Test>
        user = get_user_model().objects.create_user('TestUser', email='test@user.com', password='TestPassword%420')
        self.client.force_login(user=user)
        response = self.client.get(reverse('settings'), follow=True)
        self.assertTemplateUsed(response, 'extras/settings.html')

    def test_get_request_is_valid(self):
        response = self.client.get(reverse('settings'), follow=True)
        self.assertEqual(response.status_code, 404)
        # deepcode ignore NoHardcodedPasswords/test: <Test>
        user = get_user_model().objects.create_user('TestUser', email='test@user.com', password='TestPassword%420')
        self.client.force_login(user=user)
        response = self.client.get(reverse('settings'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_request_is_valid(self):
        pass
