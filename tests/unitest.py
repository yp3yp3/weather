import unittest
import requests
APP_ADDR = "http://127.0.0.1:5000"
# Asserts a 200 response code from the weather web app using requests module
class AppConectivityTest(unittest.TestCase):
    def test_connection(self):
        try:
            response = requests.get(APP_ADDR, timeout=10).status_code
        except:
            response = 201
        self.assertEqual(response, 200)
if __name__ == "main":
    unittest.main()