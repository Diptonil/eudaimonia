from django.test import TestCase
from authentication.models import Profile
from django.contrib.auth import get_user_model
from datetime import date
import sys
sys.path.append("..")


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create(username='test_name', password='test_password')

    def test_field_verbosity(self):
        profile = Profile.objects.last()
        user_verbosity = profile._meta.get_field('user').verbose_name
        bio_verbosity = profile._meta.get_field('bio').verbose_name
        birth_date_verbosity = profile._meta.get_field('birth_date').verbose_name
        join_date_verbosity = profile._meta.get_field('join_date').verbose_name
        image_verbosity = profile._meta.get_field('image').verbose_name
        purpose_verbosity = profile._meta.get_field('purpose').verbose_name
        self.assertEqual(user_verbosity, 'user')
        self.assertEqual(bio_verbosity, 'bio')
        self.assertEqual(birth_date_verbosity, 'birth date')
        self.assertEqual(join_date_verbosity, 'join date')
        self.assertEqual(image_verbosity, 'image')
        self.assertEqual(purpose_verbosity, 'purpose')

    def test_default_fields(self):
        bio = Profile.objects.first().bio
        purpose = Profile.objects.first().purpose
        image = Profile.objects.first().image
        join_date = Profile.objects.first().join_date
        birth_date = Profile.objects.first().birth_date
        self.assertEqual(bio, None)
        self.assertEqual(purpose, 'Personal')
        self.assertEqual(image, 'profiles/default_zayg9d.jpg')
        self.assertEqual(repr(join_date), repr(date.today()))
        self.assertEqual(birth_date, None)

    def test_user(self):
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first().user.username, 'test_name')

    def test_purpose_length(self):
        max_length = Profile.objects.first()._meta.get_field('purpose').max_length
        self.assertEqual(max_length, 16)

    def test_str_return(self):
        entry = Profile.objects.first()
        self.assertEqual(str(entry), 'test_name')
