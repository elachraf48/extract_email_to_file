import imaplib
import email
import os
import re
from email.header import decode_header
from email.parser import BytesParser

# User input for email provider (Hotmail, Yahoo, or Gmail)
email_provider = input("Enter the number of email provider: Hotmail (1), Yahoo (2), or Gmail (3): ")

if email_provider.lower() == "1":
    # Connect to the IMAP server (Hotmail)
    imap_server = imaplib.IMAP4_SSL("imap-mail.outlook.com")
    provider = "hotmail.com"
    folder_name = "hotmail"

elif email_provider.lower() == "2":
    # Connect to the IMAP server (Yahoo)
    imap_server = imaplib.IMAP4_SSL("imap.mail.yahoo.com")
    provider = "yahoo.com"
    folder_name = "yahoo"

elif email_provider.lower() == "3":
    # Connect to the IMAP server (Gmail)
    imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
    provider = "gmail.com"
    folder_name = "gmail"

else:
    print("Invalid email provider. Please try again.")
    exit()

# Create the folder if it doesn't exist
if not os.path.exists(f"resulta/{folder_name}"):
    os.makedirs(f"resulta/{folder_name}")

# Read the email and password data from the file "data.txt"
email_password_dict = {}
with open("data.txt", "r") as file:
    email_password_data = file.readlines()

if not email_password_data:
    print("No email and password data found in data.txt.")
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
    print("Email provider not found in data.txt.")
    email_address = input("Enter your email address: ")
    password = input("Enter your password: ")
    email_password_dict[provider] = {"email": email_address, "password": password}

# Connect to the IMAP server
imap_server.login(email_address, password)

# Select the mailbox/folder you want to extract emails from
mailbox = "INBOX"
imap_server.select(mailbox, readonly=False)

# Search for all email IDs within the selected mailbox
status, response = imap_server.search(None, "ALL")
email_ids = response[0].split()

# Iterate over each email ID and fetch the email data
for email_id in email_ids:
    email_id = email_id.decode('utf-8')
    print("Processing email ID:", email_id)  # Print the email ID
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

            # Print the file name for debugging
            print(f"File name: {file_name}")

            # Perform any necessary processing or saving to a text file
            with open(file_name, "wb") as file:
                file.write(raw_email)

            # Delete the email from the mailbox
            imap_server.store(email_id, "+FLAGS", "\\Deleted")
        else:
            print(f"Failed to fetch email ID: {email_id}")
    except Exception as e:
        print(f"Error processing email ID: {email_id}")
        print(str(e))

# Close the connection to the IMAP server
imap_server.expunge()
imap_server.close()
imap_server.logout()
