from selenium import webdriver
from selenium.webdriver.common.by import By  # Import By module
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment this for headless mode if needed

# Set up the Chrome driver service with the correct path
service = Service(executable_path=r"C:\\Users\\User\\Desktop\\chromedriver-win64\\chromedriver.exe")

# Initialize WebDriver with the correct service and options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open Instagram login page
driver.get("https://www.instagram.com/accounts/login/")

# Login process
time.sleep(5)

# Use the By module to locate elements
username = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
password = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
username.clear()
password.clear()

# Enter credentials
username.send_keys("fatihhhhhh26")
password.send_keys("))))))))")

# Find and click the login button
login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
login_button.click()

# After login
time.sleep(10)

try:
    not_now_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and contains(text(), 'Not now')]"))
    )
    not_now_button.click()
    print("Successfully clicked 'Not Now' for save login info.")
except Exception as e:
    print(f"Error clicking 'Not Now' button: {str(e)}")

# Wait for the next "Turn on Notifications" dialog and click 'Not Now'
try:
    # More specific waiting for the "Not Now" button for notifications
    not_now_button_2 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and contains(text(), 'Not Now')]"))
    )
    not_now_button_2.click()
    print("Successfully clicked 'Not Now' for notifications.")
except Exception as e:
    print(f"Error clicking 'Not Now' button (notifications): {str(e)}")


time.sleep(2)  # Wait a few seconds for the home page to load

# Go to your profile page using your username
profile_url = f"https://www.instagram.com/fatihhhhhh26/"
driver.get(profile_url)

time.sleep(3)  # Adjust this time as needed

# Click on 'Followings' to open the following list
followings_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/following')]"))
)
followings_button.click()

# Wait for the following list to load
time.sleep(5)

# Get the following dialog element
followings_container = driver.find_element(By.XPATH, "//div[@role='dialog']")

# Initialize an empty list to store all following links
following_urls = set()  # Use a set to avoid duplicates
previous_links_count = 0

# Keep scrolling until no new links are added
while True:
    # Scroll down the dialog to load more followings
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followings_container)
    time.sleep(3)  # Wait for new followings to load

    # Get all the 'a' tags inside the dialog
    following_links = driver.find_elements(By.XPATH, "//div[@role='dialog']//a")

    # Add the unique URLs to the set
    for link in following_links:
        url = link.get_attribute("href")
        if url and "/p/" not in url:  # Ignore non-profile links
            following_urls.add(url)

    # Check if the number of links has increased
    if len(following_urls) == previous_links_count:
        break  # Stop if no new links have been added
    previous_links_count = len(following_urls)

# Convert the set of following URLs to a list
following_urls = list(following_urls)

# Initialize a list to store followings' bios
followings_bios = []

# Loop through each following and get their bio
for url in following_urls:
    driver.get(url)
    time.sleep(3)  # Wait for the profile to load

    # We now wait for the bio element to be available in the DOM
    try:
        # Fetch the bio, checking for the "more" button
        bio_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span._ap3a._aaco._aacu._aacx._aad7._aade"))
        )
        
        bio = bio_element.text if bio_element.text else "No bio available"
        
        # Check for the 'more' button and click it to reveal the full bio
        more_button = driver.find_elements(By.XPATH, "//span[contains(text(), 'more')]")
        if more_button:
            more_button[0].click()
            time.sleep(2)  # Wait for the bio to expand
            bio = bio_element.text if bio_element.text else "No bio available"
        
    except Exception as e:
        bio = "No bio available"
        print(f"Error retrieving bio for {url}: {e}")

    followings_bios.append([url, bio])

# Save the followings' bios in a CSV file
with open("followings_bios.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Profile URL", "Bio"])
    writer.writerows(followings_bios)

print("Followings' bios have been saved to followings_bios.csv.")

# Close the driver after completing the task
driver.quit()