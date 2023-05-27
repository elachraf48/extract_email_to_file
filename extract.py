import imaplib
from email import message_from_bytes
from email.header import decode_header
import os
import re

# User input for email provider (Hotmail or Yahoo)
email_provider = input("Enter the number of email provider Hotmail (1) or Yahoo (2) : ")

if email_provider.lower() == "1":
    # Connect to the IMAP server (Hotmail)
    imap_server = imaplib.IMAP4_SSL("imap-mail.outlook.com")
    username = ""
    password = ""

elif email_provider.lower() == "2":
    # Connect to the IMAP server (Yahoo)
    imap_server = imaplib.IMAP4_SSL("imap.mail.yahoo.com")
    username = "achrafelabouye@yahoo.com"
    password = "wtwdebznrypcudga"
else:
    print("Invalid email provider. Please try again.")
    exit()

# User input for email credentials
if username =="":
    username = input("Enter your email address: ")
if password=="":
    password = input("Enter your password: ")

# Login to the email account
imap_server.login(username, password)

# Select the mailbox/folder you want to extract emails from
mailbox = "INBOX"
imap_server.select(mailbox)

# Search for all email IDs within the selected mailbox
status, response = imap_server.search(None, "ALL")
email_ids = response[0].split()

# Iterate over each email ID and fetch the email data
for email_id in email_ids:
    status, email_data = imap_server.fetch(email_id, "(RFC822)")
    raw_email = email_data[0][1]
    email_message = message_from_bytes(raw_email)

    # Extract the "From" name from the email headers
    from_name = decode_header(email_message["From"])[0][0]
    if isinstance(from_name, bytes):
        from_name = from_name.decode('utf-8')

    # Sanitize the filename by removing or replacing invalid characters
    sanitized_from_name = re.sub(r'[<>:"/\\|?*]', '', from_name)[:40].replace(' ', '_')

    # Create a new filename using the sanitized "From" name
    if email_provider=="1":
        file_name = f"resulta/hotmail/{sanitized_from_name}.txt"
    elif email_provider=="2":
        file_name = f"resulta/yahoo/{sanitized_from_name}.txt"
    # Perform any necessary processing or saving to a text file
    with open(file_name, "w") as file:
        file.write(raw_email.decode("utf-8").replace("\r\n", "\n"))

    # Mark the email for deletion
    # imap_server.store(email_id, "+FLAGS", "\\Deleted")

# Permanently delete the marked emails
imap_server.expunge()

# Close the connection to the IMAP server
imap_server.close()
imap_server.logout()
