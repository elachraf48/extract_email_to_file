import imaplib
import email
import os
import re
from email.header import decode_header
from email.parser import BytesParser
import tkinter as tk
from tkinter import filedialog, ttk
import tkinter.simpledialog as sd  # Add this line for the simpledialog module
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def extract_emails(email_provider):
    # Connect to the IMAP server based on the email provider
    if email_provider == "Hotmail":
        imap_server = imaplib.IMAP4_SSL("imap-mail.outlook.com")
        provider = "hotmail.com"
        folder_name = "hotmail"
    elif email_provider == "Outlook":
        imap_server = imaplib.IMAP4_SSL("imap-mail.outlook.com")
        provider = "outlook.com"
        folder_name = "Outlook"
    elif email_provider == "Yahoo":
        imap_server = imaplib.IMAP4_SSL("imap.mail.yahoo.com")
        provider = "yahoo.com"
        folder_name = "yahoo"
    elif email_provider == "Gmail":
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
                if email.endswith(provider):
                    email_password_dict[provider] = {"email": email, "password": password}

    # Check if the email provider is supported and retrieve the corresponding email and password
    if provider in email_password_dict:
        email_address = email_password_dict[provider]["email"]
        password = email_password_dict[provider]["password"]
    else:
        # error_text.insert(tk.END, "Email provider not found in data.txt.\n")
        # email_address = sd.askstring("Add Email and Password", "Enter your email address:")
        # password = sd.askstring("Add Email and Password", "Enter your password:")
        # email_password_dict[provider] = {"email": email_address, "password": password}

        # # Save the new email and password to data.txt
        # with open("data.txt", "a") as file:
        #     file.write(f"{email_address},{password}\n")
        add_email_password()
    # Connect to the IMAP server
    try:
        print(email_address, password)
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
                # from_name = decode_header(email_message["From"])[0][0]
                from_name_bytes = decode_header(email_message["From"])[0][0]
                from_name = from_name_bytes.decode("utf-8") if isinstance(from_name_bytes, bytes) else from_name_bytes

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
        progress_text = f"Progress: {current_email}/{total_emails} emails processed"
        print(progress_text)
        error_text.delete("1.0", tk.END)
        error_text.insert(tk.END, progress_text)
        error_text.update_idletasks()
        current_email += 1

        # Check if extraction is paused
        if pause_extraction:
            error_text.delete("1.0", tk.END)
            error_text.insert(tk.END, "Extraction paused.\n")
            while pause_extraction:
                window.update()
                if not email_extraction_running:
                    return

    # Close the connection to the IMAP server
    imap_server.expunge()
    imap_server.close()
    imap_server.logout()

def add_email_password():
    # Create a new window for adding email and password
    add_window = tk.Toplevel(window)
    add_window.title("Add Email and Password")

    # Create labels and entry fields for email and password
    email_label = ttk.Label(add_window, text="Email Address:")
    email_entry = ttk.Entry(add_window)
    password_label = ttk.Label(add_window, text="Password:")
    password_entry = ttk.Entry(add_window, show="*")
    submit_button = ttk.Button(add_window, text="Submit",
                               command=lambda: save_email_password(add_window, provider_var.get(), email_entry.get(), password_entry.get()))
    
    # Grid layout for widgets in the add window
    email_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    email_entry.grid(row=0, column=1, padx=10, pady=5)
    password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    password_entry.grid(row=1, column=1, padx=10, pady=5)
    submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    # Center the add window on the screen
    add_window.geometry("+%d+%d" % (add_window.winfo_screenwidth() / 2 - add_window.winfo_width() / 2, add_window.winfo_screenheight() / 2 - add_window.winfo_height() / 2))


   
email_password_dict = {}


def save_email_password(window, provider, email, password):
    email_password_dict[provider] = {"email": email, "password": password}
     # Save the new email and password to Google Sheets
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    scopes = [
     'https://www.googleapis.com/auth/spreadsheets'
     'https://www.googleapis.com/auth/drive'
     ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scopes=scopes)
    client = gspread.authorize(credentials)
    sheet = client.open('extract_data').sheet1  # Replace 'EmailPasswords' with your Google Sheet name
   

    row = [provider, email, password]
    sheet.append_row(row)

    # Notify the user that the email and password have been saved
    success_text = f"Email and password for {provider} have been saved."
    error_text.insert(tk.END, success_text)
    # Save the new email and password to data.txt
    with open("data.txt", "a") as file:
        file.write(f"{email},{password}\n")

    # Close the add window
    window.destroy()
def start_extraction():
    global email_extraction_running
    email_extraction_running = True
    email_provider = provider_var.get()
    extract_emails(email_provider)
    email_extraction_running = False


def pause_extraction():
    global pause_extraction
    if email_extraction_running:
        pause_extraction = True


def resume_extraction():
    global pause_extraction
    if email_extraction_running and pause_extraction:
        pause_extraction = False
        error_text.delete("1.0", tk.END)
        error_text.insert(tk.END, "Extraction resumed.\n")

# Create the Tkinter window
window = tk.Tk()
window.title("Email Extraction")
window.geometry("430x220")

# Configure style for the widgets
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TCombobox", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))

# Create widgets
provider_var = tk.StringVar()
provider_label = ttk.Label(window, text="Select Email Provider:")
provider_dropdown = ttk.Combobox(window, textvariable=provider_var, values=["Gmail", "Yahoo", "Hotmail","Outlook"])
provider_dropdown.set("Yahoo")
start_button = ttk.Button(window, text="Start Extraction", command=start_extraction)
pause_button = ttk.Button(window, text="Pause Extraction", command=pause_extraction)
resume_button = ttk.Button(window, text="Resume Extraction", command=resume_extraction)
error_text = tk.Text(window, height=2, width=50)

# Grid layout for widgets
provider_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
provider_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="we")
start_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="we")
pause_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")
resume_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")
error_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="we")

# Center the window on the screen
window.eval('tk::PlaceWindow . center')

# Global variables
email_extraction_running = False
pause_extraction = False

# Start the Tkinter event loop
window.mainloop()
