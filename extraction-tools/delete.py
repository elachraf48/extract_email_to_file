import imaplib

# IMAP settings
IMAP_SERVER = 'imap.gmail.com'
EMAIL = 'chaymaejarodi@gmail.com'
PASSWORD = 'fwwakvtmoewrfdtw'

# Connect to the IMAP server
imap = imaplib.IMAP4_SSL(IMAP_SERVER)

# Login to your Gmail account
imap.login(EMAIL, PASSWORD)

# Select the Sent Mail folder
imap.select('"[Gmail]/Sent Mail"')

# Search for all sent emails
status, response = imap.search(None, 'ALL')
email_ids = response[0].split()

# Delete each sent email
for email_id in email_ids:
    imap.store(email_id, '+FLAGS', '\\Deleted')

# Permanently delete the marked sent emails
imap.expunge()

# Select the Drafts folder
imap.select('"[Gmail]/Drafts"')

# Search for all draft emails
status, response = imap.search(None, 'ALL')
email_ids = response[0].split()

# Delete each draft email
for email_id in email_ids:
    imap.store(email_id, '+FLAGS', '\\Deleted')

# Permanently delete the marked draft emails
imap.expunge()

# Close the connection
imap.close()
imap.logout()

print("All sent emails and draft emails have been deleted.")
