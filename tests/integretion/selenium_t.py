import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Define the Flask app URL (update according to your setup)
FLASK_URL = "http://127.0.0.1:8001"  # For local Flask instance
# FLASK_URL = "http://app:5000"  # If running in Docker Compose

class AppSeleniumTest(unittest.TestCase):
    def setUp(self):
        """Initialize WebDriver using webdriver-manager."""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(5)  # Implicit wait for elements to load

    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()

    def test_home_page_true(self):
        """Positive test - Submitting a valid location."""
        self.driver.get(FLASK_URL)

        # Ensure the main heading is loaded
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )
        self.assertIn('Here is a form', element.text)

        # Locate the input field and enter a valid location
        location_input = self.driver.find_element(By.NAME, 'location')
        location_input.send_keys("new york")

        # Click the submit button
        submit_button = self.driver.find_element(By.TAG_NAME, 'button')
        submit_button.click()

        # Check if the response page contains the entered location
        body_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        print(body_text.text)
        self.assertIn('New York', body_text.text)

    def test_home_page_false(self):
        """Negative test - Submitting an invalid location."""
        self.driver.get(FLASK_URL)

        # Locate the input field and enter an invalid location
        location_input = self.driver.find_element(By.NAME, 'location')
        location_input.send_keys("asdf")

        # Click the submit button
        submit_button = self.driver.find_element(By.TAG_NAME, 'button')
        submit_button.click()

        # Check if an error message appears
        body_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        self.assertIn('bad location', body_text.text)

if __name__ == '__main__':
    unittest.main()
