import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
class AppSeleniumTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
    def tearDown(self):
        self.driver.quit()
    def test_home_page_true(self):
        self.driver.get("http://nginx/")
        # POSITIVE
        element = self.driver.find_element(By.TAG_NAME, 'h1')

        self.assertIn('Here is a form', element.text)
        element2 = self.driver.find_element(By.NAME, 'location')
        element2.send_keys("new york")
        element3 = self.driver.find_element(By.TAG_NAME, 'button')
        element3.click()
        element3_1 = self.driver.find_element(By.TAG_NAME, 'body')
        print(element3_1.text)
        self.assertIn('New York', element3_1.text)
        time.sleep(2)



    def test_home_page_false(self):
        # NEGATIVE
        self.driver.get("http://nginx/")
        element5 = self.driver.find_element(By.NAME, 'location')
        element5.send_keys("asdf")
        element7 = self.driver.find_element(By.TAG_NAME, 'button')
        element7.click()
        element6 = self.driver.find_element(By.TAG_NAME, 'body')
        self.assertIn('bad location', element6.text)
        time.sleep(2)

if __name__ == '__main__':
    unittest.main()
