# WhatsApp Automated Message Sender

Send automated WhatsApp messages using Python and Selenium. After a one-time QR code scan, the script can send messages without any manual intervention.

## Features

- ✅ One-time QR code scanning - session is saved for future use
- ✅ Send messages by contact name or phone number
- ✅ Character-by-character typing to avoid WhatsApp Web issues
- ✅ Handles page refreshes and dynamic loading
- ✅ Persistent login session

## Prerequisites

- Python 3.7 or higher
- Firefox browser installed
- GeckoDriver (Firefox WebDriver)

## Installation

### 1. Install GeckoDriver (Firefox browser)

**Windows:**
1. Download GeckoDriver from [GitHub Releases](https://github.com/mozilla/geckodriver/releases)
2. Extract the `geckodriver.exe` file
3. Add the folder to your system PATH, or place it in the same folder as your script

**macOS:**
```bash
brew install geckodriver
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install firefox-geckodriver
```

**Linux (Fedora):**
```bash
sudo dnf -y install firefox-geckodriver
```

**Linux (Other distributions):**
Download from [GitHub](https://github.com/mozilla/geckodriver/releases) and place in `/usr/local/bin/`

### 2. Create Virtual Environment

Open your terminal/command prompt and navigate to your project directory:

```bash
# Create virtual environment
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

### 4. Install Selenium

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

## Configuration

Open the script file and modify the configuration at the bottom:

```python
if __name__ == "__main__":
    sender = WhatsAppSender()
    
    # Method 1: Send by contact name
    sender.send_message(
        contact_name="Maleja Nieto",  # Change to your contact name
        message="Hi Maleja, this is an automated message test 👏"
    )
    
    # Method 2: Send by phone number (recommended)
    # sender.send_message_by_phone(
    #     phone_number="573001234567",  # Country code + number (no + or spaces)
    #     message="Hi Maleja, this is an automated message test 👏"
    # )
    
    sender.close()
```

## Usage

### First Time Setup

1. Make sure your virtual environment is activated
2. Run the script:

```bash
python whatsapp_auto_sender.py
```

3. Firefox will open automatically
4. Scan the QR code with your phone's WhatsApp
5. The script will save your session and send the message
6. Done! Your session is now saved

### Subsequent Runs

Simply run the script - no QR scanning needed:

```bash
python whatsapp_auto_sender.py
```

The script will automatically:
- Load your saved WhatsApp session
- Open the chat
- Send your message
- Close the browser

## Sending Messages

### Method 1: By Contact Name

The contact must be saved in your phone's contacts:

```python
sender.send_message(
    contact_name="John Doe",
    message="Hello John!"
)
```

### Method 2: By Phone Number (Recommended)

Works even if the contact is not saved. Include country code without + or spaces:

```python
sender.send_message_by_phone(
    phone_number="573001234567",  # Format: [country code][number]
    message="Hello!"
)
```

**Phone Number Format Examples:**
- Colombia: `573001234567` (57 + phone number)
- USA: `15551234567` (1 + phone number)
- UK: `447911123456` (44 + phone number)
- Spain: `34612345678` (34 + phone number)

## Advanced Options

### Run in Headless Mode (No Browser Window)

Uncomment line 43 in the script:

```python
options.add_argument("--headless")
```

### Change Profile Directory

By default, the session is saved in `whatsapp_profile` folder. To change it:

```python
sender = WhatsAppSender(profile_dir="my_custom_folder")
```

### Adjust Typing Speed

Modify the sleep times in the script:
- Line 124: Search box typing speed (default: 0.1 seconds per character)
- Line 172: Message typing speed (default: 0.05 seconds per character)

## Troubleshooting

### "geckodriver not found" error
- Make sure GeckoDriver is installed and in your PATH
- Try placing `geckodriver.exe` in the same folder as your script

### Session expired / Need to scan QR code again
- Delete the `whatsapp_profile` folder
- Run the script again to create a new session

### Message not sending
- Make sure the phone number includes the country code
- Verify the contact name is spelled exactly as it appears in WhatsApp
- Check that WhatsApp Web is not open in another browser

### Browser stays open after error
- This is intentional for debugging
- Check what's displayed on screen
- Close manually or press Ctrl+C in terminal

## Deactivating Virtual Environment

When you're done:

```bash
deactivate
```

## Project Structure

```
your-project/
├── whatsapp_auto_sender.py    # Main script
├── whatsapp_profile/          # Saved WhatsApp session (created automatically)
├── venv/                      # Virtual environment (created by you)
├── requirements.txt           # Python packages to install
└── README.md                  # This file
```

## Notes

- The script types messages character by character to avoid WhatsApp Web detection
- Your WhatsApp session is saved locally in the `whatsapp_profile` folder
- Keep this folder secure as it contains your WhatsApp Web login session
- The script works with personal WhatsApp accounts (no business API needed)
- I use Clause Code to help me create this fast (I was in a hurry!)

## License

This is a personal automation tool. Use responsibly and in accordance with WhatsApp's Terms of Service.

---

**Happy automating! 🚀**
