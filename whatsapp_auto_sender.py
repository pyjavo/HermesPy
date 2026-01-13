"""
WhatsApp Message Sender - No manual intervention needed after first setup
Uses saved browser session to stay logged in
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
import os
import json

class WhatsAppSender:
    def __init__(self, profile_dir="whatsapp_profile"):
        """
        Initialize WhatsApp sender with persistent session
        
        Args:
            profile_dir: Directory to store Firefox profile (maintains login)
        """
        self.profile_dir = os.path.abspath(profile_dir)
        self.driver = None
        
    def setup_driver(self):
        """Set up Firefox with persistent profile"""
        options = Options()
        
        # Create profile directory if it doesn't exist
        if not os.path.exists(self.profile_dir):
            os.makedirs(self.profile_dir)
            print(f"✓ Created profile directory: {self.profile_dir}")
        
        # Use custom profile to maintain login
        options.add_argument("-profile")
        options.add_argument(self.profile_dir)
        
        # Optional: Run in headless mode (no visible browser)
        # Uncomment the next line to run without opening browser window
        # options.add_argument("--headless")
        
        self.driver = webdriver.Firefox(options=options)
        print("✓ Firefox driver initialized with persistent profile")
        
    def first_time_setup(self):
        """
        Run this once to scan QR code and save session
        """
        if not self.driver:
            self.setup_driver()
            
        print("\n" + "="*50)
        print("FIRST TIME SETUP")
        print("="*50)
        print("Opening WhatsApp Web...")
        self.driver.get("https://web.whatsapp.com/")
        
        print("\n📱 Please scan the QR code in the browser window")
        print("⏳ Waiting for you to log in...")
        print("   (This is a ONE-TIME setup)")
        
        # Wait for login - look for the side panel
        try:
            WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located((By.ID, "side"))
            )
            print("\n✅ Login successful! Session saved.")
            print("🎉 You won't need to scan QR code again!")
            time.sleep(3)
            return True
        except:
            print("\n❌ Login timeout. Please try again.")
            return False
    
    def is_logged_in(self):
        """Check if already logged in to WhatsApp Web"""
        try:
            self.driver.get("https://web.whatsapp.com/")
            # Wait for either QR code or side panel
            time.sleep(5)
            
            # Check if side panel exists (means logged in)
            try:
                self.driver.find_element(By.ID, "side")
                return True
            except:
                return False
        except:
            return False
    
    def send_message(self, contact_name, message):
        """
        Send message to a contact
        
        Args:
            contact_name: Contact name as it appears in WhatsApp
            message: Message to send
        """
        if not self.driver:
            self.setup_driver()
        
        try:
            # Load WhatsApp if not already loaded
            if "web.whatsapp.com" not in self.driver.current_url:
                self.driver.get("https://web.whatsapp.com/")
                
            # Check if logged in
            if not self.is_logged_in():
                print("❌ Not logged in. Running first-time setup...")
                if not self.first_time_setup():
                    return False
            
            print(f"\n📤 Sending message to: {contact_name}")
            
            # Wait for WhatsApp to load
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "side"))
            )
            time.sleep(2)
            
            # Find and click search box
            search_box = None
            search_attempts = [
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'),
                (By.XPATH, '//div[@title="Search input textbox"]'),
                (By.XPATH, '//div[@id="side"]//div[@contenteditable="true"]'),
            ]
            
            for by, selector in search_attempts:
                try:
                    search_box = self.driver.find_element(by, selector)
                    break
                except:
                    continue
            
            if not search_box:
                raise Exception("Could not find search box")
            
            # Search for contact - type slowly to avoid issues
            search_box.click()
            time.sleep(1)
            
            # Clear any existing text
            search_box.send_keys(Keys.CONTROL + "a")
            search_box.send_keys(Keys.BACKSPACE)
            time.sleep(0.5)
            
            # Type contact name character by character
            for char in contact_name:
                search_box.send_keys(char)
                time.sleep(0.1)  # Small delay between characters
            
            print(f"✓ Searched for: {contact_name}")
            time.sleep(3)
            
            # Select contact (press Enter or click)
            try:
                contact = self.driver.find_element(By.XPATH, f'//span[@title="{contact_name}"]')
                contact.click()
            except:
                search_box.send_keys(Keys.ENTER)
            
            time.sleep(2)
            
            # Find message box
            message_box = None
            message_attempts = [
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'),
                (By.XPATH, '//div[@title="Type a message"]'),
                (By.XPATH, '//footer//div[@contenteditable="true"]'),
            ]
            
            for by, selector in message_attempts:
                try:
                    message_box = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((by, selector))
                    )
                    break
                except:
                    continue
            
            if not message_box:
                raise Exception("Could not find message box")
            
            # Send message - type character by character
            message_box.click()
            time.sleep(0.5)
            
            # Split message by lines to handle Enter key properly
            lines = message.split('\n')
            for i, line in enumerate(lines):
                for char in line:
                    message_box.send_keys(char)
                    time.sleep(0.05)  # Small delay between characters
                
                # Add line break if not the last line
                if i < len(lines) - 1:
                    message_box.send_keys(Keys.SHIFT + Keys.ENTER)
                    time.sleep(0.1)
            
            time.sleep(1)
            message_box.send_keys(Keys.ENTER)
            
            print("✅ Message sent successfully!")
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def send_message_by_phone(self, phone_number, message):
        """
        Send message using phone number (faster, bypasses search)
        
        Args:
            phone_number: Phone with country code (e.g., '573001234567')
            message: Message to send
        """
        if not self.driver:
            self.setup_driver()
        
        try:
            print(f"\n📤 Preparing to send message to: +{phone_number}")
            
            # First, ensure we're logged into WhatsApp Web
            print("⏳ Loading WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com/")
            time.sleep(5)
            
            # Check if logged in
            if not self.is_logged_in():
                print("❌ Not logged in. Running first-time setup...")
                if not self.first_time_setup():
                    return False
            
            print("✓ Logged in to WhatsApp Web")
            
            # Wait for WhatsApp to be fully loaded
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.ID, "side"))
                )
                print("✓ WhatsApp fully loaded")
            except:
                print("⚠️ WhatsApp may not be fully loaded, continuing...")

            time.sleep(3)

            # Now navigate to the phone number URL
            url = f"https://web.whatsapp.com/send?phone={phone_number}"
            print(f"⏳ Opening chat with +{phone_number}...")
            self.driver.get(url)

            # Wait and monitor for URL changes (the refresh)
            print("⏳ Waiting for page to stabilize (checking for refresh)...")
            initial_url = self.driver.current_url
            time.sleep(5)

            # Check if URL changed (indicates a refresh/redirect)
            current_url = self.driver.current_url
            if current_url != initial_url:
                print(f"✓ Page refreshed, new URL detected")
                time.sleep(5)  # Wait for new page to load

            # Wait for chat to be ready - look for the main chat area
            print("⏳ Waiting for chat window to load...")
            chat_loaded = False

            for i in range(10):  # Try for up to 30 seconds
                try:
                    # Check if main chat div exists
                    self.driver.find_element(By.XPATH, '//div[@id="main"]')
                    print("✓ Chat window loaded")
                    chat_loaded = True
                    break
                except:
                    if i < 9:
                        time.sleep(3)
                        print(f"  Still waiting... ({i+1}/10)")

            if not chat_loaded:
                print("⚠️ Chat window didn't load properly, trying anyway...")

            time.sleep(3)

            # Now find the message box - be very specific to avoid search box
            print("✓ Looking for message input box...")
            message_box = None
            max_attempts = 5

            for attempt in range(max_attempts):
                print(f"  Attempt {attempt + 1}/{max_attempts}...")

                if attempt > 0:
                    time.sleep(3)

                # Method 1: Message box in footer with data-tab="10" (most specific)
                try:
                    message_box = self.driver.find_element(
                        By.XPATH, 
                        '//footer//div[@contenteditable="true"][@data-tab="10"]'
                    )
                    print("✓ Found message box (method 1 - footer with data-tab)")
                    break
                except:
                    pass

                # Method 2: Message box by placeholder/title in footer
                try:
                    message_box = self.driver.find_element(
                        By.XPATH, 
                        '//footer//div[@contenteditable="true" and @role="textbox"]'
                    )
                    print("✓ Found message box (method 2 - footer textbox)")
                    break
                except:
                    pass

                # Method 3: Find footer first, then contenteditable inside it
                try:
                    # Make sure it's NOT in the side panel (search area)
                    message_box = self.driver.find_element(
                        By.XPATH, 
                        '//div[@id="main"]//footer//div[@contenteditable="true"]'
                    )
                    print("✓ Found message box (method 3 - main/footer)")
                    break
                except:
                    pass

                # Method 4: By data-testid
                try:
                    message_box = self.driver.find_element(
                        By.XPATH, 
                        '//div[@data-testid="conversation-compose-box-input"]'
                    )
                    print("✓ Found message box (method 4 - data-testid)")
                    break
                except:
                    pass

                # Method 5: Specific p tag approach (newer WhatsApp)
                try:
                    message_box = self.driver.find_element(
                        By.XPATH, 
                        '//div[@id="main"]//div[@contenteditable="true"][@data-tab="10"]'
                    )
                    print("✓ Found message box (method 5 - main area)")
                    break
                except:
                    pass

            if not message_box:
                print("❌ Could not find message box")
                print("💡 Checking for error messages...")

                # Check for invalid number message
                try:
                    error = self.driver.find_element(By.XPATH, '//*[contains(text(), "phone number")]')
                    print(f"❌ WhatsApp error: {error.text}")
                except:
                    pass

                print("\n🔍 Browser will stay open for 20 seconds - check the screen")
                time.sleep(20)
                return False

            # Send message character by character
            print("✓ Message box found! Typing message...")
            message_box.click()
            time.sleep(1)

            # Type message character by character
            lines = message.split('\n')
            for i, line in enumerate(lines):
                for char in line:
                    message_box.send_keys(char)
                    time.sleep(0.05)

                if i < len(lines) - 1:
                    message_box.send_keys(Keys.SHIFT + Keys.ENTER)
                    time.sleep(0.1)

            print("✓ Message typed! Sending...")
            time.sleep(1)
            message_box.send_keys(Keys.ENTER)

            print("✅ Message sent successfully!")
            time.sleep(3)
            return True

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("🔍 Browser will stay open for 20 seconds - check what's on screen")
            time.sleep(20)
            return False

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("Browser closed.")


# Example usage
if __name__ == "__main__":
    # Initialize sender (will create/use saved profile)
    sender = WhatsAppSender()
    
    print("="*50)
    print("WhatsApp Automated Message Sender")
    print("="*50)
    
    # Method 1: Send by contact name
    #sender.send_message(
    #    contact_name="Maleja Nieto",
    #    message="Hi Maleja, this is an automated message test :)"
    #)
    
    # Method 2: Send by phone number (faster, more reliable)
    sender.send_message_by_phone(
        phone_number="573001234567",  # Replace with actual number
        message="Hi Steffy, this is an automated message test :)"
    )
    
    # Close browser
    sender.close()