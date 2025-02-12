import unittest
from project import app  # נייבא את Flask מהאפליקציה שלך

class AppUnitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """הגדרת סביבת Flask לבדיקה"""
        cls.client = app.test_client()
        cls.client.testing = True

    def test_homepage(self):
        """בודק אם דף הבית מחזיר 200"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()