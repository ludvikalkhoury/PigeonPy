"""
PigeonPy.carrier

This module provides functionality to send email notifications using Gmail with a secure, user-friendly setup flow.

Features:
- GUI-based configuration of email credentials and recipient address
- Persistent storage of credentials in a hidden environment file (~/.email_notify_env)
- Automatic loading of credentials for future use
- Supports multiple recipients separated by commas or semicolons
- Sends emails securely via Gmail's SMTP over SSL

Functions:
- send_pigeon(subject, body, to_email=None): Sends an email using stored credentials. If credentials are missing,
  the GUI setup is launched automatically.

Environment Variables:
- EMAIL_NOTIFY_USER: The Gmail address used to send emails
- EMAIL_NOTIFY_PASS: The Gmail App Password (not the regular login password)
- EMAIL_NOTIFY_RECEIVER: Default recipient(s) for email notifications (can be comma/semicolon-separated)

Usage Example:
---------------
from PigeonPy.carrier import send_pigeon

send_pigeon(
    subject="Job Complete",
    body="Your script finished successfully.",
    to_email="me@example.com; team@example.com"
)
"""

import os
import smtplib
from email.mime.text import MIMEText
from pathlib import Path
from .gui_setup import launch_setup


def _load_env():
	"""Load environment variables from ~/.email_notify_env if the file exists."""
	env_file = Path.home() / '.email_notify_env'
	if env_file.exists():
		with env_file.open() as f:
			for line in f:
				if '=' in line:
					key, val = line.strip().split('=', 1)
					os.environ[key] = val


def _check_or_setup():
	"""Ensure required environment variables are set, launching setup GUI if needed."""
	_load_env()
	if not all([
		os.getenv("EMAIL_NOTIFY_USER"),
		os.getenv("EMAIL_NOTIFY_PASS")
	]):
		launch_setup()
		_load_env()


def send_pigeon(subject, body, to_email=None):
	"""
	Send an email using the credentials and default receiver from the environment file.

	Parameters:
	- subject (str): Subject of the email
	- body (str): Body text of the email
	- to_email (str, optional): Comma- or semicolon-separated list of recipients.
	  If not provided, defaults to EMAIL_NOTIFY_RECEIVER or the sender.
	"""
	_check_or_setup()

	user = os.getenv("EMAIL_NOTIFY_USER")
	pw = os.getenv("EMAIL_NOTIFY_PASS")
	to_email = to_email or os.getenv("EMAIL_NOTIFY_RECEIVER") or user

	# Allow comma or semicolon separation, strip whitespace
	recipients = [e.strip() for e in to_email.replace(' ', '').replace(';', ',').split(',') if e.strip()]

	msg = MIMEText(body)
	msg['Subject'] = subject
	msg['From'] = user
	msg['To'] = ", ".join(recipients)

	with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
		server.login(user, pw)
		server.sendmail(user, recipients, msg.as_string())
