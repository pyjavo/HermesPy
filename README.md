# WhatsApp Automated Message Sender

Send automated WhatsApp messages using Python and Selenium. After a one-time QR code scan, the script can send messages without any manual intervention.
Supports scheduled messaging to multiple contacts throughout the day.

## Features

- ✅ One-time QR code scanning - session is saved for future use
- ✅ Send messages by contact name or phone number
- ✅ Character-by-character typing to avoid WhatsApp Web issues
- ✅ Handles page refreshes and dynamic loading
- ✅ Persistent login session
- ✅ **Scheduled messaging** - send messages at specific times
- ✅ **Bulk messaging** - send to multiple contacts from a JSON file
- ✅ **Timezone support** - uses Bogotá time (UTC-5)

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

### 4. Install Required Packages

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

## Configuration

### Create contacts.json File

Rename your file `contacts_sample.json` to `contacts.json` in your project directory with your contacts and schedule

**JSON Structure:**
- `name`: Contact's name (for reference only)
- `phone`: Phone number with country code (no + or spaces)
- `message`: Custom message for this contact (supports emojis and line breaks with `\n`)
- `schedule_time`: Time to send in 24-hour format "HH:MM" (Bogotá timezone UTC-5)


## Usage

### First Time Setup

1. Make sure your virtual environment is activated
2. Run the script:

```bash
python whatsapp_auto_sender.py
```

3. Firefox will open automatically
4. Scan the QR code with your phone's WhatsApp
5. The script will save your session
6. Done! Your session is now saved

### Scheduled Messages (Recommended)

Send messages to multiple contacts at scheduled times:

```bash
python whatsapp_auto_sender.py
```

The script will:
1. Load all contacts from `contacts.json`
2. Display a schedule overview
3. Wait until each scheduled time
4. Send messages automatically one by one

**Example Output:**
```
============================================================
SCHEDULED MESSAGES OVERVIEW
============================================================
Current time in Bogotá: 08:45:23
Total contacts: 3

Schedule:
  09:00 - Juan (+573001234567)
  10:30 - John (+573007654321)
  14:00 - Maria (+573009876543)
============================================================

📋 Processing contact 1/3
   Name: Juan
   Phone: +573001234567
⏰ Scheduled for 09:00 (Bogotá time)
⏳ Waiting 14 minutes and 37 seconds...
```

### Send Single Message Immediately

Edit the script and add the single message section:

```python
# Option 1: Send single message immediately
sender.send_message_by_phone(
    phone_number="573001234567",
    message="Hi Juan, this is an automated message test :)"
)
```

Then run:
```bash
python whatsapp_auto_sender.py
```

## Sending Messages

### Method 1: Scheduled Bulk Messages (From JSON)

The default behavior needs the `contacts.json`. Make sure the Python code is using the following line:

```python
sender.send_scheduled_messages("contacts.json")
```

and then run the script:

```bash
python whatsapp_auto_sender.py
```

**Features:**
- Automatically waits until scheduled time for each contact
- Processes contacts in chronological order
- Skips messages scheduled in the past
- Shows progress and status for each message

### Method 2: Single Message by Phone Number

Works even if the contact is not saved. Include country code without + or spaces:

```python
sender.send_message_by_phone(
    phone_number="573001234567",
    message="Hello!"
)
```

### Method 3: Single Message by Contact Name

The contact must be saved in your phone's contacts:

```python
sender.send_message(
    contact_name="John Doe",
    message="Hello John!"
)
```

## Time Format and Timezone

- **Timezone:** America/Bogota (UTC-5)
- **Format:** 24-hour format "HH:MM"
- **Examples:**
  - Morning: `"09:00"`, `"09:30"`
  - Afternoon: `"14:00"`, `"15:45"`
  - Evening: `"18:00"`, `"20:30"`
  - Night: `"23:00"`, `"23:59"`

**Important:** The script uses Bogotá time (Colombia). If you're in a different timezone, the messages will still be sent at the specified Bogotá time.

## Phone Number Format

Include country code without + or spaces:

**Examples:**
- 🇨🇴 Colombia: `573001234567` (57 + phone number)
- 🇺🇸 USA: `15551234567` (1 + phone number)
- 🇬🇧 UK: `447911123456` (44 + phone number)
- 🇪🇸 Spain: `34612345678` (34 + phone number)
- 🇲🇽 Mexico: `525512345678` (52 + phone number)
- 🇦🇷 Argentina: `5491112345678` (54 + phone number)

## Advanced Options

### Run in Headless Mode (No Browser Window)

Uncomment line 43 in the script:

```python
options.add_argument("--headless")
```

**Note:** First-time QR code scanning requires a visible browser window.

### Change Profile Directory

By default, the session is saved in `whatsapp_profile` folder. To change it:

```python
sender = WhatsAppSender(profile_dir="my_custom_folder")
```

### Adjust Typing Speed

Modify the sleep times in the script to type faster or slower:
- Line 124: Search box typing speed (default: 0.1 seconds per character)
- Line 172: Message typing speed (default: 0.05 seconds per character)

Lower values = faster typing, but may be detected by WhatsApp.

### Custom JSON File Location

Specify a different JSON file path:

```python
sender.send_scheduled_messages("path/to/my_contacts.json")
```

### Multi-line Messages

Use `\n` in your JSON messages for line breaks:

```json
{
    "message": "Hello!\n\nThis is a multi-line message.\n\nBest regards,\nYour Name"
}
```

## Troubleshooting

### "geckodriver not found" error
- Make sure GeckoDriver is installed and in your PATH
- Try placing `geckodriver.exe` in the same folder as your script

### "No module named 'pytz'" error
- Make sure you installed pytz: `pip install pytz`
- Verify your virtual environment is activated

### Session expired / Need to scan QR code again
- Delete the `whatsapp_profile` folder
- Run the script again to create a new session

### Message not sending
- Make sure the phone number includes the country code
- Verify the contact name is spelled exactly as it appears in WhatsApp
- Check that WhatsApp Web is not open in another browser
- Ensure the scheduled time hasn't already passed

### "contacts.json not found"
- The script will automatically create an example file
- Edit the example with your contacts and times
- Make sure the JSON file is in the same directory as the script

### Messages sent at wrong time
- Verify you're using 24-hour format: `"14:00"` not `"2:00 PM"`
- The timezone is set to Bogotá (UTC-5)
- Check your system time is correct

### Browser stays open after error
- This is intentional for debugging
- Check what's displayed on screen
- Close manually or press Ctrl+C in terminal

## Script Modes

### Mode 1: Scheduled Messages (Default)

In the script, this is enabled by default:

```python
sender.send_scheduled_messages("contacts.json")
```

### Mode 2: Single Immediate Message

Comment out Mode 1 and uncomment this:

```python
sender.send_message_by_phone(
    phone_number="573001234567",
    message="Hi Steffy, this is an automated message test :)"
)
```

## Tips and Best Practices

1. **Test First:** Send a test message to yourself before scheduling bulk messages
2. **Realistic Timing:** Space out messages by at least 15-30 minutes to appear more natural
3. **Personalize Messages:** Use different messages for each contact
4. **Keep Session Active:** Run the script at least once a week to keep WhatsApp session alive
5. **Backup contacts.json:** Keep a backup of your contacts file
6. **Monitor First Run:** Watch the first scheduled run to ensure everything works correctly
7. **Use Descriptive Names:** In contacts.json, use clear names for easy reference

## Example Use Cases

### Morning Greetings
```json
{
    "contacts": [
        {
            "name": "Client 1",
            "phone": "573001234567",
            "message": "Good morning! Have a great day! ☀️",
            "schedule_time": "08:00"
        }
    ]
}
```

### Birthday Messages
```json
{
    "contacts": [
        {
            "name": "Friend",
            "phone": "573001234567",
            "message": "Happy Birthday! 🎉🎂 Wishing you an amazing day!",
            "schedule_time": "09:00"
        }
    ]
}
```

### Appointment Reminders
```json
{
    "contacts": [
        {
            "name": "Patient 1",
            "phone": "573001234567",
            "message": "Reminder: You have an appointment tomorrow at 3 PM. See you then! 👨‍⚕️",
            "schedule_time": "18:00"
        }
    ]
}
```

## Deactivating Virtual Environment

When you're done:

```bash
deactivate
```

## Project Structure

```
your-project/
├── whatsapp_auto_sender.py    # Main script
├── contacts.json              # Your contacts (git-ignored)
├── contacts_sample.json       # Rename this file as contacts.json
├── whatsapp_profile/          # Saved WhatsApp session (git-ignored)
├── venv/                      # Virtual environment (git-ignored)
├── .gitignore                 # Git ignore file
├── requirements.txt           # Python packages to install
└── README.md                  # This file
```

## Security Notes

- **Keep `contacts.json` private** - it contains phone numbers and messages
- **Keep `whatsapp_profile/` secure** - it contains your WhatsApp Web login session
- **Add both to `.gitignore`** - never commit these to version control
- **Don't share your session folder** - anyone with access can use your WhatsApp

## Limitations

- WhatsApp may limit bulk messaging to prevent spam
- Session expires if inactive for extended periods
- Requires Firefox browser to be installed
- Cannot send media files (images, videos, documents)
- Works only with text messages

## Notes

- The script types messages character by character to avoid WhatsApp Web detection
- Your WhatsApp session is saved locally in the `whatsapp_profile` folder
- The script works with personal WhatsApp accounts (no business API needed)
- Messages are sent in chronological order based on schedule_time
- Past scheduled times are automatically skipped

## License

This is a personal automation tool. Use responsibly and in accordance with WhatsApp's Terms of Service.

---

**Happy automating! 🚀**