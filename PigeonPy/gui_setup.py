"""
PigeonPy.gui_setup

This module provides a Tkinter-based GUI to collect and save email configuration settings for the PigeonPy package.

Features:
- Prompts the user to enter their Gmail address and Gmail App Password
- Allows the user to choose whether to send emails to themselves or to custom recipients
- Option to show/hide the password field
- Recipient field supports multiple addresses separated by commas or semicolons
- Opens the Gmail App Password help page for user assistance
- Saves all values to ~/.email_notify_env for persistent and secure reuse

Stored Variables:
- EMAIL_NOTIFY_USER: The Gmail address used to send emails
- EMAIL_NOTIFY_PASS: The Gmail App Password (not the regular login password)
- EMAIL_NOTIFY_RECEIVER: Default recipient(s) of email notifications

Usage:
-------
from PigeonPy.gui_setup import launch_setup

launch_setup()
"""

import os
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import webbrowser

def launch_setup():
	"""
	Launches the GUI window for setting up email notification credentials.
	Prompts the user for:
	- Gmail address
	- Gmail App Password
	- Recipient email (optional, can be the same or different)
	- Whether to show password
	- Whether to send to self or others

	Stores the input securely in ~/.email_notify_env for later use by the package.
	"""
	root = tk.Tk()
	root.title("Email Setup")

	# Load saved values if they exist
	env_file = Path.home() / '.email_notify_env'
	defaults = {}
	if env_file.exists():
		with env_file.open() as f:
			for line in f:
				if '=' in line:
					k, v = line.strip().split('=', 1)
					defaults[k] = v

	email_var = tk.StringVar(value=defaults.get("EMAIL_NOTIFY_USER", ""))
	pass_var = tk.StringVar(value=defaults.get("EMAIL_NOTIFY_PASS", ""))
	receiver_email_var = tk.StringVar(value=defaults.get("EMAIL_NOTIFY_RECEIVER", ""))
	show_pw = tk.BooleanVar(value=False)

	# Determine if "Send to same email" should be checked
	same_email_default = (
		not receiver_email_var.get()
		or receiver_email_var.get().strip() == email_var.get().strip()
	)
	to_same_var = tk.BooleanVar(value=same_email_default)

	# GUI Layout
	tk.Label(root, text="Your Gmail:").grid(row=0, column=0)
	tk.Label(root, text="App Password:").grid(row=1, column=0)
	email_entry = tk.Entry(root, textvariable=email_var, width=30)
	pass_entry = tk.Entry(root, textvariable=pass_var, width=30, show='*')
	email_entry.grid(row=0, column=1)
	pass_entry.grid(row=1, column=1)

	def toggle_pw():
		"""Toggles visibility of the password entry field."""
		pass_entry.config(show='' if show_pw.get() else '*')

	tk.Checkbutton(root, text="View Password", variable=show_pw, command=toggle_pw).grid(row=2, column=1, sticky='w')

	def toggle_recipient_field():
		"""
		Shows or hides the recipient email field depending on whether
		'Send to same email' checkbox is selected.
		"""
		if to_same_var.get():
			receiver_entry.grid_remove()
			receiver_label.grid_remove()
			hint_label.grid_remove()
		else:
			receiver_label.grid(row=4, column=0)
			receiver_entry.grid(row=4, column=1)
			hint_label.grid(row=5, column=1, sticky='w')

	receiver_label = tk.Label(root, text="Recipient Email:")
	receiver_entry = tk.Entry(root, textvariable=receiver_email_var, width=30)
	hint_label = tk.Label(root, text="(Separate multiple with commas or semicolons)")

	tk.Checkbutton(root, text="Send to same email", variable=to_same_var, command=toggle_recipient_field).grid(row=3, column=1, sticky='w')

	def open_gmail_help():
		"""
		Opens the Gmail App Password page in the default web browser
		to help the user generate an app-specific password.
		"""
		webbrowser.open("https://myaccount.google.com/apppasswords")

	tk.Button(root, text="How to get App Password", command=open_gmail_help).grid(row=6, column=0, columnspan=2)

	def save():
		"""
		Validates and saves the provided email credentials to ~/.email_notify_env.
		If 'Send to same email' is selected, uses the sender as recipient.
		Otherwise, uses the entered recipient address(es).
		"""
		email = email_var.get().strip()
		password = pass_var.get().strip()
		receiver = email if to_same_var.get() else receiver_email_var.get().strip()

		if not email or not password or not receiver:
			messagebox.showerror("Error", "All fields are required.")
			return

		with env_file.open('w') as f:
			f.write(f"EMAIL_NOTIFY_USER={email}\n")
			f.write(f"EMAIL_NOTIFY_PASS={password}\n")
			f.write(f"EMAIL_NOTIFY_RECEIVER={receiver}\n")

		messagebox.showinfo("Success", "Credentials saved. Restart your script.")
		root.destroy()

	tk.Button(root, text="Save", command=save).grid(row=7, column=1, sticky='e')

	toggle_recipient_field()  # Initial visibility
	root.mainloop()
