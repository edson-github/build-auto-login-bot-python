import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import setup_driver, login_to_github

class TestGitHubLogin(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        load_dotenv()
        self.driver = setup_driver()
        
    def tearDown(self):
        """Clean up after each test"""
        if hasattr(self, 'driver'):
            self.driver.quit()
            
    def test_login_page_loads(self):
        """Test if GitHub login page loads correctly"""
        self.driver.get("https://github.com/login")
        self.assertIn("Sign in to GitHub", self.driver.title)
        
    def test_login_fields_present(self):
        """Test if login form fields are present"""
        self.driver.get("https://github.com/login")
        username_field = self.driver.find_element(By.ID, "login_field")
        password_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.NAME, "commit")
        
        self.assertTrue(username_field.is_displayed())
        self.assertTrue(password_field.is_displayed())
        self.assertTrue(login_button.is_displayed())
        
    def test_invalid_credentials(self):
        """Test login with invalid credentials"""
        self.driver.get("https://github.com/login")
        username_field = self.driver.find_element(By.ID, "login_field")
        password_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.NAME, "commit")
        
        username_field.send_keys("invalid_username")
        password_field.send_keys("invalid_password")
        login_button.click()
        
        # Wait for error message
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flash-error"))
        )
        self.assertTrue(error_message.is_displayed())

if __name__ == '__main__':
    unittest.main()