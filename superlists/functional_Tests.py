from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

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
        self.browser.get('http://localhost:8000')

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

        #When she hits enter the list is update with 1: item
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: foo')
        #there is still a textbox inviting her to enter items she enters another
        #item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('bar')
        inputbox.send_keys(Keys.ENTER)

        #the page updates with her new item so the list is now "1: foo 2: bar"
        self.check_for_row_in_list_table('1: foo')
        self.check_for_row_in_list_table('2: bar')
        #she reads that the site has generated a unique URL for her

        #she visits that url her to do list is still there

if __name__ == '__main__':
    unittest.main(warnings='ignore')
