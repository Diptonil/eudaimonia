from django.test import TestCase
from journal.models import Entry
from django.contrib.auth import get_user_model
import sys
sys.path.append("..")


class EntryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(username='test_name', password='test_password')
        Entry.objects.create(user=user, title='test title', entry='test entry')

    def test_field_verbosity(self):
        entry = Entry.objects.last()
        user_verbosity = entry._meta.get_field('user').verbose_name
        title_verbosity = entry._meta.get_field('title').verbose_name
        entry_verbosity = entry._meta.get_field('entry').verbose_name
        date_verbosity = entry._meta.get_field('date').verbose_name
        image_verbosity = entry._meta.get_field('image').verbose_name
        activated_verbosity = entry._meta.get_field('activated').verbose_name
        starred_verbosity = entry._meta.get_field('starred').verbose_name
        self.assertEqual(title_verbosity, 'title')
        self.assertEqual(user_verbosity, 'user')
        self.assertEqual(entry_verbosity, 'entry')
        self.assertEqual(date_verbosity, 'date')
        self.assertEqual(image_verbosity, 'image')
        self.assertEqual(starred_verbosity, 'starred')
        self.assertEqual(activated_verbosity, 'activated')

    def test_user(self):
        self.assertEqual(Entry.objects.first().user, get_user_model().objects.first())

    def test_default_fields(self):
        activated = Entry.objects.first().activated
        starred = Entry.objects.first().starred
        self.assertFalse(starred)
        self.assertTrue(activated)

    def test_entered_fields(self):
        entry = Entry.objects.first()
        self.assertEqual(entry.title, 'test title')
        self.assertEqual(entry.entry, 'test entry')

    def test_title_length(self):
        max_length = Entry.objects.first()._meta.get_field('title').max_length
        self.assertEqual(max_length, 64)

    def test_str_return(self):
        entry = Entry.objects.first()
        self.assertEqual(str(entry), 'test title')

    def test_table_sequence(self):
        user = get_user_model().objects.create(username='test_name_2', password='test_password')
        e1 = Entry.objects.create(user=user, title='test title last', entry='test entry last')
        e2 = Entry.objects.create(user=user, title='test title first', entry='test entry first')
        self.assertEqual(e2.title, 'test title first')
        self.assertEqual(e1.title, 'test title last')
