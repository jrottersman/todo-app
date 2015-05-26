from selenium import webdriver
import unittest
class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_list_and_retrieve_later(self):
    
        #Edith comes to our site yay traffic!
        self.browser.get('http://localhost:8000')

        #She notices the page title and header mention to do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # She is invited to enter a to do list right away

        #She types something into a textbox

        #When she hits enter the list is update with 1: item

        #there is still a textbox inviting her to enter items she enters another
        #item

        #the page updates with her new item so the list is now "1: foo 2: bar"

        #she reads that the site has generated a unique URL for her

        #she visits that url her to do list is still there

if __name__ == '__main__':
    unittest.main(warnings='ignore')
