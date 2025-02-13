import unittest
import sys
import argparse
import chromedriver_autoinstaller  # Automatically installs ChromeDriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the Flask app URL
FLASK_URL = "http://127.0.0.1:8081"  # Local Flask instance
# FLASK_URL = "http://app:5000"  # If running in Docker Compose

# Parse CLI arguments **before** unittest starts
parser = argparse.ArgumentParser()
parser.add_argument("--headless", action="store_true", help="Run tests in headless mode")
parser.add_argument("--extensions", nargs="+", help="List of Chrome extensions to load", default=[])
args, unknown = parser.parse_known_args()

# Remove unknown args to prevent unittest errors
sys.argv = [sys.argv[0]] + unknown

class AppSeleniumTest(unittest.TestCase):
    def setUp(self):
        """Initialize WebDriver with options."""
        # Automatically install the correct version of ChromeDriver
        chromedriver_autoinstaller.install()

        chrome_options = Options()

        # Enable headless mode if passed via CLI
        if args.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")  # Prevents issues in headless mode
            chrome_options.add_argument("--no-sandbox")  # Helps in CI environments
            chrome_options.add_argument("--disable-dev-shm-usage")  # Helps in containerized environments

        # Load Chrome extensions if provided
        for extension in args.extensions:
            chrome_options.add_extension(extension)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(5)  # Implicit wait for elements to load

    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()

    def test_home_page_true(self):
        """Positive test - Submitting a valid location."""
        self.driver.get(FLASK_URL)

        try:
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

        except Exception as e:
            self.fail(f"Test failed due to unexpected error: {e}")

    def test_home_page_false(self):
        """Negative test - Submitting an invalid location."""
        self.driver.get(FLASK_URL)

        try:
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

        except Exception as e:
            self.fail(f"Test failed due to unexpected error: {e}")

if __name__ == '__main__':
    unittest.main()
