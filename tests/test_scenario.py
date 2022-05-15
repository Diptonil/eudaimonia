from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
import time
import sys


class IndexPageTest(LiveServerTestCase):
    port = 8001

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service('tests/Test Resources/chromedriver.exe')
        self.browser = webdriver.Chrome(service=service, options=options)
        self.browser.implicitly_wait(5)

    def test_page_title(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Welcome', self.browser.title)

    def test_page_contents(self):
        self.browser.get(self.live_server_url)
        quote = self.browser.find_element_by_id('showcase-text-quote').text
        quote_by = self.browser.find_element_by_id('showcase-text-quote-by').text
        features = list()
        for i in range(1, 5):
            features.append(self.browser.find_element_by_id('feature' + str(i)).text)
        self.assertEqual(features[0], "A Personal Diary...")
        self.assertEqual(features[1], "... that is also a Collage...")
        self.assertEqual(features[2], "... that nobody on earth can break into...")
        self.assertEqual(features[3], "... and comes for free.")
        self.assertEqual(quote, '"I write because I don\'t know what I think until I read what I say."')
        self.assertEqual(quote_by, "- Flannery O'Connor")

    def test_page_functionality(self):
        pass

    def test_url_redirections(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text('Sign Up').click()
        time.sleep(3)
        self.assertEqual(self.browser.current_url, self.live_server_url + '/signup/')
        self.browser.back()
        self.browser.find_element_by_link_text('Feature Description').click()
        time.sleep(3)
        self.assertEqual(self.browser.current_url, self.live_server_url + '/services/')
        self.browser.back()
        self.browser.find_element_by_link_text('Log in.').click()
        time.sleep(3)
        self.assertEqual(self.browser.current_url, self.live_server_url + '/login/')
        self.browser.back()
        self.browser.find_element_by_xpath("//button[text()='Get Started']").click()
        time.sleep(3)
        self.assertEqual(self.browser.current_url, self.live_server_url + '/signup/')

    def tearDown(self):
        self.browser.quit()

'''
class SignupPageTest(LiveServerTestCase):
    port = 8001

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service('tests/Test Resources/chromedriver.exe')
        self.browser = webdriver.Chrome(service=service, options=options)
        self.browser.implicitly_wait(5)

    def test_page_title(self):
        self.browser.get(self.live_server_url + '/signup/')
        self.assertIn('Sign Up', self.browser.title)

    def test_page_contents(self):
        self.browser.get(self.live_server_url + '/signup/')
        username = self.browser.find_element_by_id('id_username')
        firstname = self.browser.find_element_by_id('id_first_name')
        lastname = self.browser.find_element_by_id('id_last_name')
        email = self.browser.find_element_by_id('id_email')
        password1 = self.browser.find_element_by_id('id_password1')
        password2 = self.browser.find_element_by_id('id_password2')
        guideline = self.browser.find_element_by_id('guideline-text').text
        elements = len(self.browser.find_elements_by_class_name('form-control'))
        self.assertEqual(guideline, "Usernames must not have special characters except periods or underscores.")
        self.assertEqual(elements, 6)
        self.assertEqual(username.get_attribute('placeholder'), 'Username')
        self.assertEqual(firstname.get_attribute('placeholder'), 'First Name')
        self.assertEqual(lastname.get_attribute('placeholder'), 'Last Name')
        self.assertEqual(email.get_attribute('placeholder'), 'Email')
        self.assertEqual(password1.get_attribute('placeholder'), 'Password')
        self.assertEqual(password2.get_attribute('placeholder'), 'Repeat Password')

    def test_url_redirections(self):
        self.browser.get(self.live_server_url + '/signup/')
        self.browser.find_element_by_link_text('Log in now!').click()
        time.sleep(3)
        self.assertEqual(self.browser.current_url, self.live_server_url + '/login/')

    def test_page_functionality(self):
        self.browser.get(self.live_server_url + '/signup/')
        username = self.browser.find_element_by_id('id_username')
        firstname = self.browser.find_element_by_id('id_first_name')
        lastname = self.browser.find_element_by_id('id_last_name')
        email = self.browser.find_element_by_id('id_email')
        password1 = self.browser.find_element_by_id('id_password1')
        password2 = self.browser.find_element_by_id('id_password2')
        username.send_keys('TestUser')
        firstname.send_keys('Test')
        lastname.send_keys('User')
        email.send_keys('t@u.com')
        password1.send_keys('TestPassword%420')
        password2.send_keys('TestPassword%420')
        self.browser.find_element_by_class_name('btn').click()
        time.sleep(5)
        self.assertEqual(self.browser.find_element_by_tag_name('li').text, 'An activation link has been sent to your email. Be sure to check your spam folder as well.')

    def tearDown(self):
        self.browser.quit()


class LoginPageTest(LiveServerTestCase):
    port = 8001

    def setUp(self):
        get_user_model().objects.create_user('TestUser', email='t@u.com', password='TestPassword%420')
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service('tests/Test Resources/chromedriver.exe')
        self.browser = webdriver.Chrome(service=service, options=options)
        self.browser.implicitly_wait(5)

    def test_page_title(self):
        self.browser.get(self.live_server_url + '/login/')
        self.assertIn('Log In', self.browser.title)

    def test_page_contents(self):
        self.browser.get(self.live_server_url + '/login/')
        username = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')
        self.assertEqual(username.get_attribute('placeholder'), 'Username or Email')
        self.assertEqual(password.get_attribute('placeholder'), 'Password')
        elements = len(self.browser.find_elements_by_class_name('form-control'))
        self.assertEqual(elements, 2)

    def test_url_redirections(self):
        self.browser.get(self.live_server_url + '/login/')
        self.browser.find_element_by_link_text('Forgot Password?').click()
        time.sleep(3)
        self.assertEqual(self.browser.current_url, self.live_server_url + '/password_reset/')
        self.browser.back()
        self.browser.find_element_by_link_text('Sign Up here!').click()
        time.sleep(3)
        self.assertEqual(self.browser.current_url, self.live_server_url + '/signup/')

    def test_page_functionality(self):
        self.browser.get(self.live_server_url + '/login/')
        username = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')
        username.send_keys('TestUser')
        password.send_keys('TestPassword%420')
        self.browser.find_element_by_class_name('btn').click()
        time.sleep(5)
        self.assertEqual(self.browser.current_url, self.live_server_url + '/journal/')

    def tearDown(self):
        self.browser.quit()


class ServicesPageTest(LiveServerTestCase):
    port = 8001

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service('tests/Test Resources/chromedriver.exe')
        self.browser = webdriver.Chrome(service=service, options=options)
        self.browser.implicitly_wait(5)

    def test_page_title(self):
        self.browser.get(self.live_server_url + '/services')
        self.assertIn('Feature Description', self.browser.title)

    def test_page_contents(self):
        self.browser.get(self.live_server_url + '/services')
        headings = self.browser.find_elements_by_class_name('test-heading')
        test_headings = ('About Us', 'Utilities', 'Storage', 'Security', 'Limits')
        for heading in headings:
            self.assertEqual(heading.text, test_headings[headings.index(heading)])

    def test_page_functionality(self):
        pass

    def test_url_redirections(self):
        self.browser.get(self.live_server_url + '/services')
        self.browser.find_element_by_link_text('Home').click()
        time.sleep(3)
        self.assertEqual(self.browser.current_url, 'http://localhost:8001/services/#home')

    def tearDown(self):
        self.browser.quit()



class ProfileTest(LiveServerTestCase):
    port = 8001

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        get_user_model().objects.create_user('TestUser', email='t@u.com', password='TestPassword%420')
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service('tests/Test Resources/chromedriver.exe')
        self.browser = webdriver.Chrome(service=service, options=options)
        self.browser.get(self.live_server_url + '/login/')
        username = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')
        username.send_keys('TestUser')
        password.send_keys('TestPassword%420')
        self.browser.find_element_by_class_name('btn').click()
        self.browser.implicitly_wait(5)

    def test_page_title(self):
        self.browser.get(self.server_url + '/profile/')
        self.assertIn('Your Profile', self.browser.title)
        self.browser.get(self.server_url + '/profile/edit')
        self.assertIn('Edit Profile', self.browser.title)

    def test_page_contents(self):
        self.browser.get(self.server_url + '/profile')
        bio = self.browser.find_element_by_tag_name('h3').text
        name = self.browser.find_element_by_tag_name('h5').text
        username = self.browser.find_element_by_tag_name('h4').text
        self.assertEqual('', bio)
        self.assertEqual('TestUser', username)
        self.assertEqual('', name)
        self.browser.find_element_by_link_text('Edit Details').click()
        birth_date = self.browser.find_element_by_id('birth-date').get_attribute('placeholder')
        bio = self.browser.find_element_by_id('bio').get_attribute('placeholder')
        image = self.browser.find_elements_by_tag_name('img')[-1].get_attribute('src')
        self.assertEqual('Tell us about yourself...', bio)
        self.assertEqual('https://res.cloudinary.com/yourmomscloud/image/upload/v1/media/profiles/default_zayg9d.jpg', image)
        self.assertEqual('', birth_date)

    def test_page_functionality(self):
        self.browser.get(self.server_url + '/profile/edit')
        birth_date = self.browser.find_element_by_id('birth-date')
        bio = self.browser.find_element_by_id('bio')
        birth_date.send_keys('01/01/2000')
        bio.send_keys('This is a functional scenario testing bio.')
        self.browser.find_element_by_id('btn').click()
        time.sleep(3)
        bio = self.browser.find_element_by_tag_name('h3').text
        name = self.browser.find_element_by_tag_name('h5').text
        username = self.browser.find_element_by_tag_name('h4').text
        self.assertEqual('This is a functional scenario testing bio.', bio)
        self.assertEqual('TestUser', username)
        self.assertEqual('', name)
        self.browser.find_element_by_link_text('Edit Details').click()
        birth_date = self.browser.find_element_by_id('birth-date').get_attribute('placeholder')
        bio = self.browser.find_element_by_id('bio').get_attribute('placeholder')
        image = self.browser.find_elements_by_tag_name('img')[-1].get_attribute('src')
        labels = self.browser.find_elements_by_class_name('labels')
        test_labels = ('Birthday', 'Bio')
        for label in labels:
            self.assertEqual(label.text, test_labels[labels.index(label)])
        self.assertEqual('This is a functional scenario testing bio.', bio)
        self.assertEqual('https://res.cloudinary.com/yourmomscloud/image/upload/v1/media/profiles/default_zayg9d.jpg', image)
        self.assertEqual('2000-01-01', birth_date)

    def test_url_redirections(self):
        pass

    def tearDown(self):
        self.browser.quit()


class PasswordResetTest(LiveServerTestCase):
    pass
'''
