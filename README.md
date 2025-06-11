# PigeonPy 📬

A lightweight Python package to send email notifications from your scripts, with a simple cross-platform GUI for securely storing your email credentials.

---

## ✨ Features

- ✅ Send email notifications automatically from Python
- 🔐 Locally store your Gmail and App Password in a hidden configuration file for future use (no GUI required, after setup) 
- 📧 Support for multiple recipients (comma or semicolon separated)
- 💻 Works on Windows, macOS, and Linux
- 🧠 Automatically prompts for setup if credentials are missing

---

## 🛠 Installation

Clone the repository and install in editable mode:

```
git clone https://github.com/ludvikalkhoury/PigeonPy.git
cd PigeonPy
pip install -e .
```

## 📬 Run the Code
The first time you run the code, a settings window will pop up, allowing you to configure the sender and receiver email addresses for notifications.
You can always return to this setup later if you want to change the sender or recipient. To launch the setup window again, run:

```
from PigeonPy.gui_setup import launch_setup
launch_setup()
```
To send an email notification, use the following:
```
from PigeonPy.carrier import send_pigeon
	
send_pigeon(
  subject="MY SUBJECT",
  body="Enter Text Here.",
  to_email="sendto@gmail.com"
  )
```
	
