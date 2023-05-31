import imaplib
import email
import os
import re
from email.header import decode_header
from email.parser import BytesParser
import tkinter as tk
from tkinter import filedialog

def extract_emails(email_provider):
    # Connect to the IMAP server based on the email provider
    if email_provider.lower() == "1":
        imap_server = imaplib.IMAP4_SSL("imap-mail.outlook.com")
        provider = "hotmail.com"
        folder_name = "hotmail"
    elif email_provider.lower() == "2":
        imap_server = imaplib.IMAP4_SSL("imap.mail.yahoo.com")
        provider = "yahoo.com"
        folder_name = "yahoo"
    elif email_provider.lower() == "3":
        imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
        provider = "gmail.com"
        folder_name = "gmail"
    else:
        error_text.insert(tk.END, "Invalid email provider. Please try again.\n")
        return

    # Create the folder if it doesn't exist
    if not os.path.exists(f"resulta/{folder_name}"):
        os.makedirs(f"resulta/{folder_name}")

    # Read the email and password data from the file "data.txt"
    email_password_dict = {}
    with open("data.txt", "r") as file:
        email_password_data = file.readlines()

    if not email_password_data:
        error_text.insert(tk.END, "No email and password data found in data.txt.\n")
        email_address = input("Enter your email address: ")
        password = input("Enter your password: ")
        email_password_dict[provider] = {"email": email_address, "password": password}
    else:
        for line in email_password_data:
            line = line.strip()
            if line:
                email, password = line.split(",")
                email_password_dict[provider] = {"email": email, "password": password}

    # Check if the email provider is supported and retrieve the corresponding email and password
    if provider in email_password_dict:
        email_address = email_password_dict[provider]["email"]
        password = email_password_dict[provider]["password"]
    else:
        error_text.insert(tk.END, "Email provider not found in data.txt.\n")
        email_address = input("Enter your email address: ")
        password = input("Enter your password: ")
        email_password_dict[provider] = {"email": email_address, "password": password}

    # Connect to the IMAP server
    try:
        imap_server.login(email_address, password)
    except imaplib.IMAP4.error as e:
        error_text.insert(tk.END, f"Failed to log in to the email server: {str(e)}\n")
        return

    # Select the mailbox/folder you want to extract emails from
    mailbox = "INBOX"
    imap_server.select(mailbox, readonly=False)

    # Search for all email IDs within the selected mailbox
    status, response = imap_server.search(None, "ALL")
    email_ids = response[0].split()

    total_emails = len(email_ids)
    current_email = 1

    # Iterate over each email ID and fetch the email data
    for email_id in email_ids:
        email_id = email_id.decode('utf-8')
        error_text.insert(tk.END, f"Processing email ID: {email_id}\n")
        try:
            status, email_data = imap_server.fetch(email_id, "(RFC822)")
            if email_data:
                raw_email = email_data[0][1]

                # Parse the email message from the raw email data
                email_parser = BytesParser()
                email_message = email_parser.parsebytes(raw_email)

                # Extract the "From" name from the email headers and decode if necessary
                from_name = decode_header(email_message["From"])[0][0]
                if isinstance(from_name, bytes):
                    from_name = from_name.decode("utf-8")

                # Extract the name portion from the "From" field
                match = re.search(r'(.+?)\s*<', from_name)
                if match:
                    from_name = match.group(1)

                # Sanitize the filename by removing or replacing invalid characters
                sanitized_from_name = re.sub(r'[<>:"/\\|?*]', '', from_name)[:40].replace(' ', '_')

                # Create a new filename using the sanitized "From" name based on the email provider
                file_name = f"resulta/{folder_name}/{sanitized_from_name}"

                # Remove newline characters from the file name
                file_name = file_name.replace("\r", "").replace("\n", "")

                # Check if the file already exists and add a count if necessary
                count = 1
                while os.path.exists(f"{file_name}_{count}.txt"):
                    count += 1

                # Append the count before the .txt extension
                file_name = f"{file_name}_{count}.txt"

                # Perform any necessary processing or saving to a text file
                with open(file_name, "wb") as file:
                    file.write(raw_email)

                # Delete the email from the mailbox
                imap_server.store(email_id, "+FLAGS", "\\Deleted")
            else:
                error_text.insert(tk.END, f"Failed to fetch email ID: {email_id}\n")
        except Exception as e:
            error_text.insert(tk.END, f"Error processing email ID: {email_id}\n")
            error_text.insert(tk.END, f"Error details: {str(e)}\n")

        # Update the progress
        progress_text = f"Progress: {current_email}/{total_emails} emails processed\n"
        error_text.insert(tk.END, progress_text)
        error_text.update_idletasks()
        current_email += 1

    # Close the connection to the IMAP server
    imap_server.expunge()
    imap_server.close()
    imap_server.logout()

def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

def start_extraction_gmail():
    extract_emails("3")

def start_extraction_yahoo():
    extract_emails("2")

def start_extraction_hotmail():
    extract_emails("1")

# Create the Tkinter window
window = tk.Tk()
window.title("Email Extraction")
window.geometry("410x410")

# Create widgets
gmail_button = tk.Button(window, text="Gmail", command=start_extraction_gmail)
yahoo_button = tk.Button(window, text="Yahoo", command=start_extraction_yahoo)
hotmail_button = tk.Button(window, text="Hotmail", command=start_extraction_hotmail)
error_text = tk.Text(window, height=10, width=50)

# Grid layout for widgets
gmail_button.grid(row=0, column=0, pady=5)
yahoo_button.grid(row=1, column=0, pady=5)
hotmail_button.grid(row=2, column=0, pady=5)
error_text.grid(row=3, column=0, padx=0, pady=10)

window.mainloop()
