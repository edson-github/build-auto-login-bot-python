from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import platform
import os
import time  # Add this import

def setup_driver():
    """
    Configure and initialize the Chrome WebDriver with appropriate options for Mac M1
    """
    # Set up Chrome options
    chrome_options = Options()
    
    # Add common options for better automation
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-popup-blocking')
    
    # Add specific options for Mac M1
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    try:
        # Use ChromeDriverManager with specific version matching your Chrome
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set implicit wait time
        driver.implicitly_wait(10)
        
        return driver
    except Exception as e:
        print(f"Error setting up ChromeDriver: {str(e)}")
        raise

def login_to_github():
    try:
        driver = setup_driver()
        
        # Get credentials from environment variables
        username = os.getenv('GITHUB_USERNAME')
        password = os.getenv('GITHUB_PASSWORD')
        
        if not username or not password:
            raise ValueError("GitHub credentials not found in environment variables")
        
        # Navigate to GitHub login page
        driver.get("https://github.com/login")
        
        # Find and fill username field
        username_field = driver.find_element(By.ID, "login_field")
        username_field.send_keys(username)
        
        # Find and fill password field
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        
        # Click login button
        login_button = driver.find_element(By.NAME, "commit")
        login_button.click()
        
        print("Login attempt completed")
        
        # Add delay after successful login (10 seconds)
        time.sleep(10)
        
    except Exception as e:
        print(f"An error occurred during login: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    login_to_github()


