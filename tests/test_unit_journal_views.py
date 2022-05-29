from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
import sys
sys.path.append("..")


class JournalPageTest(TestCase):

    def test_request_is_valid(self):
        response = self.client.get(reverse('journal'))
        self.assertEqual(response.status_code, 302)
        # deepcode ignore NoHardcodedPasswords/test: <Test>
        user = get_user_model().objects.create_user('Test User', password='Test Password')
        self.client.force_login(user=user)
        response = self.client.get(reverse('journal'))
        self.assertEqual(response.status_code, 200)
