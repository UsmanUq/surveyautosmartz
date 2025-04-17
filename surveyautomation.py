from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
import random  # Import random for selecting answers

# Load credentials from config.json 🔑
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

username_text = config['login_id']
password_text = config['password']

# Setup Chrome
chrome_options = Options()
service = Service('C://Iobm-all-Usman//smartzsurvey//chromedriver.exe')  # or full path
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open login page
driver.get("https://smartz.iobm.edu.pk/StudentPortal/Survey/1")

# Wait until username field is visible (max 10 seconds)
try:
    wait = WebDriverWait(driver, 10)
    # Wait for and fill the username and password fields
    username = wait.until(EC.presence_of_element_located((By.ID, "txtRegistrationNo_cs")))
    password = wait.until(EC.presence_of_element_located((By.ID, "txtPassword_m6cs")))

    # 💡 Use credentials from JSON
    username.send_keys(username_text)
    password.send_keys(password_text)
    
    # Click login button
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "btnlgn")))
    login_button.click()

except Exception as e:
    print("❌ Login failed:", e)

print("✅ Logged in successfully!")
time.sleep(6)

while True:
    # Find all form buttons
    buttons = driver.find_elements(By.CLASS_NAME, "BtnGrid")

    if not buttons:
        print("✅ No more forms left.")
        break

    print(f"📋 {len(buttons)} form(s) found.")

    for i in range(len(buttons)):
        #try:
            # Re-fetch buttons on every loop (DOM refreshes)
            buttons = driver.find_elements(By.CLASS_NAME, "BtnGrid")

            if i >= len(buttons):
                break

            print(f"➡️ Opening form {i+1}")
            buttons[i].click()

            # Wait for form to load
            time.sleep(3)

            # Wait until the form link is visible (button for filling survey)
            wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_TgridSurvey_ctl00_ctl08_RadButton1")))

            # Simulate clicking to go to the survey form
            form_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_TgridSurvey_ctl00_ctl08_RadButton1")
            form_button.click()

            # Wait for the form to load completely (ensure questions are loaded)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Answers")))

           # Get all radio buttons on the page
            radio_buttons = driver.find_elements(By.CLASS_NAME, "Answers")

# Create a dictionary to store buttons grouped by their 'name' attribute
            radio_groups = {}

            for btn in radio_buttons:
                name = btn.get_attribute("name")
            if name not in radio_groups:
                radio_groups[name] = []
            radio_groups[name].append(btn)

# For each group, randomly select and click one option
    for group_name, buttons in radio_groups.items():
            try:
                random.choice(buttons).click()
            except Exception as e:
                print(f"⚠️ Could not select radio for {group_name}: {e}")


            # Wait for a few seconds before submitting
            time.sleep(2)

            # Submit the form (ID of the submit button)
            submit_button = driver.find_element(By.ID, "btnSubmit")  # Use actual submit button ID
            submit_button.click()

            print("✅ Survey submitted successfully!")

            # Wait for the popup to appear (this could be a confirmation dialog or alert)
            time.sleep(2)

            # Handle the popup (Click on "OK" button)
            try:
                ok_button = driver.find_element(By.XPATH, "//button[contains(text(),'OK')]")
                ok_button.click()
                print("✅ Popup 'OK' button clicked.")
            except Exception as e:
                print("⚠️ No popup detected:", e)

            # Wait for the 'Proceed to portal' button (after the form submission)
            proceed_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Proceed to Portal')]")))
            proceed_button.click()
            print("✅ Proceeded to portal.")

            # Go back to survey list after clicking 'Proceed to Portal'
            time.sleep(2)
            driver.get("https://smartz.iobm.edu.pk/StudentPortal/Survey/1")
            time.sleep(2)

        #except Exception as e:
            #print(f"⚠️ Error on form {i+1}: {e}")
            continue

#except Exception as e:
 #   print("❌ Login failed:", e)

input("🟢 Done. Press Enter to close the browser...")
driver.quit()
