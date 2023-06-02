import imaplib
import email
import os
import re
from email.header import decode_header
from email.parser import BytesParser
import tkinter as tk
from tkinter import  ttk
import tkinter.simpledialog as sd  # Add this line for the simpledialog module
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from tkinter import messagebox
import json

# Check if the data.json file exists
if not os.path.exists("data.json"):
    # Create an empty email_password_data list
    email_password_data = []

    # Write the empty list to the data.json file
    with open("data.json", "w") as file:
        json.dump(email_password_data, file)
def extract_emails(email_provider,selected_email):
    # Connect to the IMAP server based on the email provider
    if email_provider == "Outlook" or email_provider == "Hotmail":
        imap_server = imaplib.IMAP4_SSL("imap-mail.outlook.com")
        provider =email_provider.lower()+'.com'
        folder_name = email_provider
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
    email_address = ""
    password= ""
    # Read the email and password data from the file "data.txt"
    with open("data.json", "r") as file:
        email_password_data = json.load(file)

    for email_data in email_password_data:
        email = email_data["email"]
        password = email_data["password"]
        if email == selected_email:
            email_password_dict[provider] = {"email": email, "password": password}


    # Check if the email provider is supported and retrieve the corresponding email and password
    if provider in email_password_dict:
        email_address = email_password_dict[provider]["email"]
        password = email_password_dict[provider]["password"]
    else:
        add_email_password()
    # Connect to the IMAP server
    try:
        # print(email_address, password)
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

    # Function to validate the email address
    def validate_email():
        email = email_entry.get()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
            return False
        return True

    # Grid layout for widgets in the add window
    email_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    email_entry.grid(row=0, column=1, padx=10, pady=5)
    password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    password_entry.grid(row=1, column=1, padx=10, pady=5)
    submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    # Validate email and save email and password
    def submit():
        if validate_email() and password_entry.get():
            save_email_password(add_window, provider_var.get(), email_entry.get(), password_entry.get())
        else:
            messagebox.showwarning("Invalid Input", "Please enter a valid email and password.")

    # Call the submit function when the submit button is clicked
    submit_button.config(command=submit)

    # Center the add window on the screen
    add_window.geometry("+%d+%d" % (add_window.winfo_screenwidth() / 2 - add_window.winfo_width() / 2, add_window.winfo_screenheight() / 2 - add_window.winfo_height() / 2))

   
email_password_dict = {}


def save_email_password(window, provider, email, password):
    email_data = {"email": email, "password": password}
    email_password_dict[provider] = email_data    # Save the new email and password to Google Sheets
    scopes = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_dict({
        "type": "service_account",
        "project_id": "extractsource",
        "private_key_id": "9be4c6909f01ae301d90316d2e823177e2b0dc67",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDAn9YvpDLlORhR\ns3iF+VZMJHVU9pL1alGBcwAXzWXI4FcwBFIL7a0sbIvOwavnbUpXf86z9oEW7CxV\nF6KOO0LUV6ybt0ln8s0LMkkOc9U9V8iV4/vBlfsQDNmhBFrnjlCYbhnnrMOKWMP1\nP7ew8pUE4b2cpuN7AwWzy8jfxVrrdPp5TcfDbZQY8e8bJLpbFT7p+AHwjqxDhqXf\nXn/qKjeVVLI0RMMkCXdilyA/SVdOZOCYxlWhgTc48ckH8d2uGJuKAesH+gv62D4/\nTHjWG5lB5v3821QPnPHgakxvgwj+ck+G6x9JiZDctqcnDMDAfF+TNGbqBaUEtPFo\nH2U0E+aJAgMBAAECggEAHvTxIrn0VgN9hY/e1EU0mcsYMj3oc1mRXMkDIFApxgVL\n7dMb7n/Vn3iYZXOZsXlOg85uBV0d9PWi0FAal1otzNuESYhE21hZnK2JsTFreU7U\n1UYNDVkRvswZ47dD9sfX6w9yyVlqGZ9XauBBIMZzrZOr+fOWRow/S9x53YClsoZU\nDlFBjLuObWiyq2VM6IAZlrujoHJAxOYqqAlXo7xuNLBYlx1Z/WCBrermkLIAvqFi\n2rbSaWNXQmQm7sLATL0iTHXG8ZlLp9Rk7sGd4JNbLvh945K4n533V0+hgsifABBz\nnjzb9yOzkw7asjceTfja450/ELPFB1ttIjPlh2LUswKBgQD0rqQGbr7OBGvzw+8v\n8yBPtGCpf5NCltzPmIYlPIPD6NaPZzDzfsXjPOPqo7odwdTv5pnSw4JEjJPxKkpI\n+FVeOmd/KamCEu2wSGcRPDbxQ9+wsw6OKfUOjscmDUHQWKjsGeylu0rIwXBxicYE\nyXuHw7looUu4iPAJK5Z1ivuk+wKBgQDJiMNBUBYbCqoS6jkYE6oSFHgXe3LYipOC\nyBpdQLjwEUynpRuoyY1xQhyJ5cZ8PaBSmNS0J3EPSaOOaoOSDHyw9I1Y43+A2Vf/\nMGDAwxLUrr0vXcnmckY9odjMB4Sv4xAEMPvYSYdm5tMBnE7/aTlhqT6HSNbzioxS\n3M5cHjDjSwKBgHUnRUv7LIqR3WpK7zRDMb5X/ExL1CN2/mS7f8dGcUSVMF5bJzn/\nAhrqZapMGGn1C9KN1CrxB2dw88jt2cGUfbNvPWzKcunfzESydf7vmNLuD6WYJij1\nd+sve7UBdfie6sqZIxC7W3RCAmeqctCJ9AauNREe4ZWKo3uQjirbj9+PAoGAa+8F\n+4XDwQnOGkE9AKsPa41w38qqsFRPOjym+gh+w3vQXPytOpFvYhfxJt1blxB+O55E\nVJPHFlPu94gOHPr5EOB4jwGQONauLSqgtrwC6ssG4UZOqk/LVJjIfkUMiBKIcmY1\nixmeHbtDiNpI6LtXEvnMVjHphRdPndVJ48X7ks8CgYEAgpDvtU3TowLP09YpqbTB\nN6/WamGco2l4ROGoZxmVRuUq3fxKTdD3Xhh4rfM5aBakNhXaAo4GN3QKs7SXad5d\nB81StsVKMwF9A29bmP4ls5goOzuqGfs6Kn1aFpBMdyCzL/y4IBvTpxrY94huqxwO\nBQsd7NP7OP6XyzTEyBPdg88=\n-----END PRIVATE KEY-----\n",
        "client_email": "accesgoogleapi@extractsource.iam.gserviceaccount.com",
        "client_id": "113939611534077726336",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/accesgoogleapi%40extractsource.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }, scopes)
    client = gspread.authorize(credentials)
    sheet = client.open('extract_data').sheet1

    row = [provider, email, password]
    sheet.append_row(row)

    # Notify the user that the email and password have been saved
    success_text = f"Email and password for {provider} have been saved."
    error_text.insert(tk.END, success_text)
    # Save the new email and password to data.txt
    with open("data.json", "r") as file:
        email_password_data = json.load(file)
    email_password_data.append(email_data)
    with open("data.json", "w") as file:
        json.dump(email_password_data, file, indent=4)

    # Close the add window
    window.destroy()

def delete_email():
    def confirm_delete():
        selected_email = selected_email_combobox.get()
        if selected_email:
            confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the email '{selected_email}'?")
            if confirmation:
                # Delete the email from the data.json file
                with open("data.json", "r") as file:
                    email_password_data = json.load(file)
                email_password_data = [data for data in email_password_data if data["email"] != selected_email]
                with open("data.json", "w") as file:
                    json.dump(email_password_data, file, indent=4)
                messagebox.showinfo("Email Deleted", f"The email '{selected_email}' has been deleted.")
                add_window.destroy()
        else:
            messagebox.showwarning("No Email Selected", "Please select an email to delete.")

    # Create a new window for deleting email
    add_window = tk.Toplevel(window)
    add_window.title("Delete Email")

    # Read emails from data.json file
    with open("data.json", "r") as file:
        email_password_data = json.load(file)
    emails = [data["email"] for data in email_password_data]

    # Create combobox to display emails
    selected_email_var = tk.StringVar()
    selected_email_label = ttk.Label(add_window, text="Selected Email:")
    selected_email_combobox = ttk.Combobox(add_window, textvariable=selected_email_var, values=emails, state="readonly")

    # Create button to confirm deletion
    delete_button = ttk.Button(add_window, text="Delete", command=confirm_delete, style="Red.TButton")

    # Grid layout for widgets in the delete window
    selected_email_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    selected_email_combobox.grid(row=0, column=1, padx=10, pady=5)
    delete_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    # Center the delete window on the screen
    add_window.geometry("+%d+%d" % (add_window.winfo_screenwidth() / 2 - add_window.winfo_width() / 2, add_window.winfo_screenheight() / 2 - add_window.winfo_height() / 2))

def start_extraction():
    global email_extraction_running
    email_extraction_running = True
    email_provider = provider_var.get()
    selected_email = selected_email_var.get()

    if selected_email!='' and email_provider!='':
        if selected_email:
            extract_emails(email_provider,selected_email)

        email_extraction_running = False
    else:
        print('please select email')



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







def get_emails_by_provider():
    email_provider = provider_var.get().lower()

    # Clear the selected email combobox
    selected_email_combobox['values'] = []

    # Read email addresses from the JSON file
    with open("data.json", "r") as file:
        email_password_data = json.load(file)
        emails = [data["email"] for data in email_password_data if data["email"].split('@')[1].startswith(email_provider)]

    # Update the selected email combobox
    selected_email_combobox['values'] = emails

    # If no email addresses found, show dialog and ask to add new
    if not emails:
        response = messagebox.askquestion("No Emails Found", "No emails available for the selected provider. Do you want to add a new email?")
        if response == "yes":
            add_email_password()
# Create the Tkinter window
window = tk.Tk()
window.title("Email Extraction")
window.geometry("480x280")

# Configure style for the widgets
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TCombobox", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))
style.configure("Red.TButton", background="red")
style.configure("Bleu.TButton", background="#0000FF")
style.configure("Green.TButton", background="green")

# Create widgets
provider_var = tk.StringVar()
provider_label = ttk.Label(window, text="Select Email Provider:")
provider_dropdown = ttk.Combobox(window, textvariable=provider_var, values=["Gmail", "Yahoo", "Hotmail", "Outlook"],state="readonly")
provider_dropdown.set("Gmail")
selected_email_var = tk.StringVar()
selected_email_label = ttk.Label(window, text="Selected Email:")
selected_email_combobox = ttk.Combobox(window, textvariable=selected_email_var, state="readonly")
start_button = ttk.Button(window, text="Start Extraction", command=start_extraction, style="Green.TButton")
pause_button = ttk.Button(window, text="Pause Extraction", command=pause_extraction, style="Bleu.TButton")
resume_button = ttk.Button(window, text="Resume Extraction", command=resume_extraction, style="Red.TButton")
error_text = tk.Text(window, height=2, width=50)
reload = ttk.Button(window, text="Reload", command=get_emails_by_provider, style="Green.TButton")
addnewemail = ttk.Button(window, text="Add New Email", command=add_email_password, style="Bleu.TButton")
deletemail = ttk.Button(window, text="Delete Email", command=delete_email, style="Red.TButton")

reload.grid(row=1, column=2, padx=10, pady=5, sticky="we")
addnewemail.grid(row=1, column=1, padx=10, pady=0)
deletemail.grid(row=1, column=0, padx=10, pady=5, sticky="w")

selected_email_combobox.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="we")

provider_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
provider_dropdown.grid(row=0, column=2, padx=10, pady=5, sticky="we")
start_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="we")
pause_button.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="we")
resume_button.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="we")
error_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="we")


# Center the window on the screen
window.eval('tk::PlaceWindow . center')

# Start the Tkinter event loop
window.mainloop()
