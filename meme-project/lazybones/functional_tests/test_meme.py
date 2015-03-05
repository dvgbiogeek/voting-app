from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import unittest
from unittest import skip


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_body_text(self, body_text):
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn(body_text, body)

    def check_title_text(self, title_text):
        header = self.browser.find_element_by_id('id_greeting').text
        self.assertIn(title_text, header)

    def click_button(self, button_id):
        self.browser.find_element_by_id(button_id).click()

    def login_user(self):
        user_inputbox = self.browser.find_element_by_id('id_username')
        password_inputbox = self.browser.find_element_by_id('id_password')
        user_inputbox.send_keys('danielleglick')
        # need non-hashed password to enter the site
        password_inputbox.send_keys('aw3edr5')
        self.click_button('id_submit')
        self.check_title_text('Logged in as danielleglick')

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=10).until(
            lambda b: b.find_element_by_id(element_id),
            'Could not find element with id {}. Page text was {}'.format(
                element_id, self.browser.find_element_by_tag_name('body').text
            )
        )

    def retry_Webdriver_click(self, link_text):
        attempts = 0
        while attempts < 2:
            try:
                self.browser.find_element_by_link(link_text).click()
                break
            except StaleElementReferenceException:
                print('StaleElementReferenceException')
            attempts += 1


class MemeTests(FunctionalTest):
    fixtures = ['users.json', 'memes.json']

    def test_login_and_out(self):
        # go to home page
        self.browser.get('http://127.0.0.1:8000/')
        # go to login form
        import time
        time.sleep(3)
        self.browser.find_element_by_link_text('Login').click()
        self.wait_for_element_with_id('id_username')
        self.check_body_text('Login')
        # login user
        self.login_user()
        # check redirects to main site
        self.check_body_text('Vote Shenanigans!')
        self.browser.find_element_by_link_text('Logout').click()
        # self.wait_for_element_with_id('id_login')
        self.check_body_text('Login')

    def test_can_enter_a_meme(self):
        self.browser.get('http://127.0.0.1:8000/')
        self.assertIn('Vote Shenanigans!', self.browser.title)
        # check the body title
        body_title = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Vote Shenanigans!', body_title)
        # First login to add a meme
        self.browser.find_element_by_link_text('Login').click()
        self.login_user()
        # the user wants to enter a meme into the database
        self.browser.find_element_by_link_text('Add Content').click()
        import time
        time.sleep(3)
        title_inputbox = self.browser.find_element_by_id('id_new_title')
        self.assertEqual(
                title_inputbox.get_attribute('placeholder'), 'Title')
        title_inputbox.send_keys('Buns')
        url_inputbox = self.browser.find_element_by_id('id_new_url')
        self.assertEqual(
                url_inputbox.get_attribute('placeholder'), 'Image URL')
        url_inputbox.send_keys(
                'https://farm8.staticflickr.com/7525/16310590982_59ca46dafa_b.jpg')
        self.check_body_text('title = Buns')
        self.check_body_text('Image thumbnail')
        # submit meme
        submit_button = self.browser.find_element_by_id('id_new_submit')
        submit_button.click()
        # check if the submit was successful
        self.check_body_text('Success! Add another!')

    def test_unauthenticated_user_cannot_add_memes(self):
        self.browser.get('http://127.0.0.1:8000/')
        # Navigate to add meme view
        self.browser.find_element_by_link_text('Add Content').click()
        # Input title and image_url then submit
        title_inputbox = self.browser.find_element_by_id('id_new_title')
        title_inputbox.send_keys('Buns')
        url_inputbox = self.browser.find_element_by_id('id_new_url')
        url_inputbox.send_keys(
                'https://farm8.staticflickr.com/7525/16310590982_59ca46dafa_b.jpg')
        submit_button = self.browser.find_element_by_id('id_new_submit')
        submit_button.click()
        import time
        time.sleep(3)
        # Expect an error telling you to login
        self.check_body_text('Please login to add content.')

    def test_add_new_user(self):
        self.browser.get('http://127.0.0.1:8000/')
        self.wait_for_element_with_id('id_image')
        self.browser.find_element_by_link_text('Add Content').click()
        # Check for new account text and link
        self.wait_for_element_with_id('id_new_title')
        self.check_body_text('I want a')
        self.browser.find_element_by_link_text('new').click()
        # Check navigation to url to make a new account
        # new_url = self.live_server_url + '/new_account/'
        # current_url = self.browser.current_url
        # self.assertEqual(new_url, current_url)
        # enter in new account information
        self.wait_for_element_with_id('id_password1')
        self.check_body_text('New Account')
        username_inputbox = self.browser.find_element_by_id('id_username')
        username_inputbox.send_keys('danielleg')
        email_inputbox = self.browser.find_element_by_id('id_email')
        email_inputbox.send_keys('danielle@some.com')
        password1_inputbox = self.browser.find_element_by_id('id_password1')
        password1_inputbox.send_keys('cilantro')
        password2_inputbox = self.browser.find_element_by_id('id_password2')
        password2_inputbox.send_keys('cilantro')
        submit_button = self.browser.find_element_by_id('id_submit')
        submit_button.click()
        self.wait_for_element_with_id('id_password')
        # Redirects to login page after new account is made
        # login_url = self.live_server_url + '/login/'
        # current_url = self.browser.current_url
        # self.assertEqual(login_url, current_url)
        self.check_body_text('Login')
