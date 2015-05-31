from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_list_and_retrieve_later(self):
    
        #Edith comes to our site yay traffic!
        self.browser.get(self.live_server_url)

        #She notices the page title and header mention to do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to do list right away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )
        #She types something like "foo"  into the textbox
        inputbox.send_keys('foo')

        #When she hits enter she is taken to a new url and the list is
        #updated with 1: item
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: foo')
        #there is still a textbox inviting her to enter items she enters another
        #item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('bar')
        inputbox.send_keys(Keys.ENTER)

        #the page updates with her new item so the list is now "1: foo 2: bar"
        self.check_for_row_in_list_table('1: foo')
        self.check_for_row_in_list_table('2: bar')
        
        #Another user called Francis comes along to our site

        #We use a new browser session to make sure none of edith's 
        #info comes through
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #Francis vists the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('foo', page_text)
        self.assertNotIn('bar', page_text)

        #Francis starts a new list by entering a new item. He works in sales
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy Rolex')
        inputbox.send_keys(Keys.ENTER)

        #Francis gets his own unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        #There should be no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Buy milk', page_text)

        #Satisfied, they go there seperate ways
