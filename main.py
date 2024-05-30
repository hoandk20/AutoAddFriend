from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to extract phone numbers from a string
def extract_phone_numbers(text):
    import re
    # Regular expression to match phone numbers
    pattern = r'\b\d{10}\b'
    # Find all matches of the pattern in the text
    phone_numbers = re.findall(pattern, text)
    return phone_numbers

def read_text_from_file(file_path, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print("File not found.")
        return None

file_path = 'C:/Users/k/OneDrive/Desktop/Code/AutoAddFriend/Text.txt'  # Change this to your file path
phone_numbers_str = read_text_from_file(file_path, encoding='utf-8')

# Sample string containing phone numbers

# Extract phone numbers from the input string
phone_numbers_list = extract_phone_numbers(phone_numbers_str)
print("Phone numbers:", phone_numbers_list)

# Path to your ChromeDriver executable
driver_path = r'C:\Users\k\OneDrive\Desktop\Code\AutoMessage\chromedriver-win64\chromedriver.exe'  # Make sure this path is correct

# Set up the ChromeDriver service
service = Service(driver_path)

# Initialize the Chrome WebDriver with the service
browser = webdriver.Chrome(service=service)

# Open the Zalo website
browser.get('https://chat.zalo.me/')
time.sleep(30)

# Wait for the page to load completely
WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))

# Function to add friend by phone number
def add_friend(phone_number):
    time.sleep(2)
    # Click the "Add new contact" button
    browser.find_element(By.XPATH, "//i[@class='fa fa-outline-add-new-contact-2 pre']").click()
    time.sleep(2)
    
    # Enter the phone number
    phone_number_input = browser.find_element(By.XPATH, "//input[@class='phone-i-input flx-1']")
    phone_number_input.clear()
    phone_number_input.send_keys(phone_number)
    time.sleep(2)
    
    try:
        # Click the search button
        search_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-id='btn_Main_AddFrd_Search']"))
        )
        search_button.click()
        
        # Wait for the "Add Friend" button in the popup to be clickable
        add_friend_button = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='z--btn--v2 btn-neutral medium  --full-width' and @title='']//div[@data-translate-inner='STR_PROFILE_ADD_FRIEND']"))
        )
        add_friend_button.click()
        
        # Wait for the final "Add Friend" button to be clickable and click it
        final_add_friend_button = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-id='btn_AddFrd_Add' and @title='']//div[@data-translate-inner='STR_PROFILE_ADD_FRIEND']"))
        )
        final_add_friend_button.click()
        return True
    except Exception as e:
        print(f"Error: {e}")
        close_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@icon='close f16']"))
        )
        close_button.click()
        return False

# Loop through each phone number and add them as friends on Zalo
for phone_number in phone_numbers_list:
        add_friend(phone_number)
        print(f"Failed to add friend with phone number {phone_number}. Trying with the next phone number...")

# Close the browser
browser.quit()
