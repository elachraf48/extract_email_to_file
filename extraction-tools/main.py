import imaplib
import email
import os, sys
import re
from email.header import decode_header
from email.parser import BytesParser
from PyQt6 import QtCore, QtGui, QtWidgets
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from email.policy import default
from  PyQt6.QtGui import QIcon

class AddEmailPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Email and Password")

        layout = QVBoxLayout(self)


        email_label = QLabel("Email:")
        layout.addWidget(email_label)
        email_entry = QLineEdit()
        layout.addWidget(email_entry)

        password_label = QLabel("Password:")
        layout.addWidget(password_label)
        password_entry = QLineEdit()
        password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(password_entry)

        save_button = QPushButton("Save")
        layout.addWidget(save_button)
        provider_entry = 'add'
        save_button.clicked.connect(lambda: self.save_email_password(email_entry.text(), password_entry.text()))

    def save_email_password(self, email, password):
        if  email and password:
            email_data = {"email": email, "password": password}
            # Save the new email and password to Google Sheets
            scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

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

            row = [ email, password]
            sheet.append_row(row)

            # Notify the user that the email and password have been saved
            success_text = f"Email and password for  have been saved."
            QMessageBox.information(self, "Success", success_text)

            # Save the new email and password to data.txt
            with open("data.json", "r") as file:
                email_password_data = json.load(file)
            email_password_data.append(email_data)
            with open("data.json", "w") as file:
                json.dump(email_password_data, file, indent=4)

            # Close the add window
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")


class DeleteWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Email")
        self.setup_ui()

    def setup_ui(self):
        selected_email_label = QtWidgets.QLabel("Selected Email:")
        self.selected_email_combo = QtWidgets.QComboBox()
        delete_button = QtWidgets.QPushButton("Delete account")
        delete_button.clicked.connect(self.confirm_delete)
        deleteENV_button = QtWidgets.QPushButton("Delete ALL Emial Envoi And Drafts")
        deleteENV_button.clicked.connect(self.deletenv)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(selected_email_label, 0, 0)
        layout.addWidget(self.selected_email_combo, 0, 1)
        layout.addWidget(delete_button, 1, 0, 1, 2)
        layout.addWidget(deleteENV_button, 2, 0, 1, 2)

        self.setLayout(layout)

        # Populate the selected_email_combo with email addresses
        self.populate_email_combobox()

    def populate_email_combobox(self):
        # Read email addresses from the JSON file
        with open("data.json", "r") as file:
            email_password_data = json.load(file)
            emails = [data["email"] for data in email_password_data]

        # Update the selected_email_combo
        self.selected_email_combo.addItems(emails)

    def confirm_delete(self):
        selected_email = self.selected_email_combo.currentText()
        if selected_email:
            confirmation = QtWidgets.QMessageBox.question(
                self, "Confirm Deletion", f"Are you sure you want to delete the email '{selected_email}'?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )
            if confirmation == QtWidgets.QMessageBox.StandardButton.Yes:
                # Delete the email from the data.json file
                with open("data.json", "r") as file:
                    email_password_data = json.load(file)
                email_password_data = [data for data in email_password_data if data["email"] != selected_email]
                with open("data.json", "w") as file:
                    json.dump(email_password_data, file, indent=4)
                QtWidgets.QMessageBox.information(self, "Email Deleted", f"The email '{selected_email}' has been deleted.")
                self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "No Email Selected", "Please select an email to delete.")
   
    


    

    def deletenv(self):
        selected_email = self.selected_email_combo.currentText()
        email_provider = selected_email.split('@')[1].lower()

        # Connect to the IMAP server based on the email provider
        if email_provider in ["outlook.com", "hotmail.com"]:
            imap_server = "imap-mail.outlook.com"
            mailbox = "Sent"
        elif email_provider == "yahoo.com":
            imap_server = "imap.mail.yahoo.com"
            mailbox = "Sent"
        elif email_provider == "gmail.com":
            imap_server = "imap.gmail.com"
            mailbox = "Sent Mail"  # Use "Sent Mail" instead of "[Gmail]/Sent Mail"
        elif email_provider == "aol.com":
            imap_server = "imap.aol.com"
            mailbox = "Sent"
        else:
            QtWidgets.QMessageBox.information(self, "Invalid", f"Invalid email provider.")
            return

        # Connect to the IMAP server using SSL
        imap = imaplib.IMAP4_SSL(imap_server)

        with open("data.json", "r") as file:
            data = json.load(file)

        PASSWORD = None

        for item in data:
            if item["email"] == selected_email:
                PASSWORD = item["password"]
                break

        if PASSWORD is None:
            QtWidgets.QMessageBox.information(self, "Password", f"Password not found for the selected email.")
            return

        # Login to your email account
        imap.login(selected_email, PASSWORD)

        # Print the selected mailbox for debugging purposes
        print(f"Selected Mailbox: {mailbox}")

        # Select the appropriate mailbox
        typ, response = imap.select(mailbox)
        print(f"SELECT Response: {typ} {response}")

        # Search for all sent emails
        status, response = imap.search(None, 'ALL')
        email_ids = response[0].split()

        # Delete each sent email
        for email_id in email_ids:
            imap.store(email_id, '+FLAGS', '\\Deleted')

        # Permanently delete the marked sent emails
        imap.expunge()

        # Close the connection
        imap.close()
        imap.logout()

        print("All sent emails have been deleted.")
        QtWidgets.QMessageBox.information(self, "Email Deleted", f"All sent emails '{selected_email}' have been deleted.")


class EmailExtractor(QtWidgets.QMainWindow):
    def __init__(self):
            super().__init__()
            self.setup_ui()
            self.email_password_dict = {}

    def setup_ui(self):

        # Check if the data.json file exists
        if not os.path.exists("data.json"):
            # Create an empty email_password_data list
            email_password_data = []

            # Write the empty list to the data.json file
            with open("data.json", "w") as file:
                json.dump(email_password_data, file)

        self.email_password_dict = {}
    def add_email_password(self):
                dialog = AddEmailPasswordDialog(self)
                dialog.exec()
    def show_delete_window(self):
            delete_window = DeleteWindow(self)
            delete_window.exec()
    def setup_ui(self):
        self.setWindowTitle("Email Extractor")

        self.email_provider_combo = QtWidgets.QComboBox()
        self.email_provider_combo.addItems(["Outlook", "Hotmail", "Yahoo", "Gmail", "AOL"])

        self.reload_button = QtWidgets.QPushButton("Reload")
        self.reload_button.clicked.connect(self.load_emails)

        self.selected_email_label = QtWidgets.QLabel("Selected Email:")
        # self.selected_email_label.setHidden(True)

        self.selected_email_combo = QtWidgets.QComboBox()
        # self.selected_email_combo.setHidden(True)

        self.extract_button = QtWidgets.QPushButton("Extract")
        self.extract_button.clicked.connect(self.extract_emails)

        self.add_button = QtWidgets.QPushButton("Add New Account")
        self.add_button.clicked.connect(self.add_email_password)

        self.delete_button = QtWidgets.QPushButton("Delete Account")
        self.delete_button.clicked.connect(self.show_delete_window)

        self.error_text = QtWidgets.QTextEdit()
        self.error_text.setReadOnly(True)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QGridLayout(central_widget)
        layout.addWidget(QtWidgets.QLabel("Email Provider:"), 0, 0)
        layout.addWidget(self.email_provider_combo, 0, 1)
        layout.addWidget(self.reload_button, 1, 0, 1, 2)
        layout.addWidget(self.selected_email_label, 2, 0)
        layout.addWidget(self.selected_email_combo, 2, 1)
        layout.addWidget(self.extract_button, 3, 0, 1, 2)
        layout.addWidget(self.error_text, 4, 0, 1, 2)
        layout.addWidget(self.add_button, 5, 0, 1, 1)
        layout.addWidget(self.delete_button, 5, 1, 1, 2)
    def load_emails(self):
            email_provider = self.email_provider_combo.currentText().lower()

            # Clear the selected email combobox
            self.selected_email_combo.clear()

            # Read email addresses from the JSON file
            with open("data.json", "r") as file:
                email_password_data = json.load(file)
                emails = [data["email"] for data in email_password_data if "@" in data["email"] and data["email"].split('@')[1].startswith(email_provider)]

            # Update the selected email combobox
            self.selected_email_combo.addItems(emails)

            # If no email addresses found, show dialog and ask to add new
            if not emails:
                response = QtWidgets.QMessageBox.question(self, "No Emails Found", "No emails available for the selected provider. Do you want to add a new email?",
                                                          QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                if response == QtWidgets.QMessageBox.StandardButton.Yes:
                    self.add_email_password()


    def extract_emails(self):
        email_provider = self.email_provider_combo.currentText()
        selected_email = self.selected_email_combo.currentText()

        provider = email_provider.lower() + ".com"
        folder_name = email_provider

        # Connect to the IMAP server based on the email provider
        if email_provider == "Outlook" or email_provider == "Hotmail":
            mail = imaplib.IMAP4_SSL("imap-mail.outlook.com")
        elif email_provider == "Yahoo":
            mail = imaplib.IMAP4_SSL("imap.mail.yahoo.com")
        elif email_provider == "Gmail":
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
        elif email_provider == "AOL":
            mail = imaplib.IMAP4_SSL("imap.aol.com")
        else:
            self.error_text.setText("Invalid email provider.")
            return

        # Create the folder if it doesn't exist
        if not os.path.exists(f"resulta/{email_provider}"):
            os.makedirs(f"resulta/{email_provider}")

        # Read the email and password data from the file "data.json"
        email_address = ""
        password = ""
        email_password_dict = {}

        # Read the email and password data from the file "data.json"
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
            AddEmailPasswordDialog()

        # Fetch emails for the selected email account
        try:
            mail.login(email_address, password)
            mail.select("INBOX", readonly=False)
            _, message_numbers = mail.search(None, "ALL")
            message_numbers = message_numbers[0].split()
            total_emails = len(message_numbers)
            current_email = 1

            self.error_text.clear()
            if total_emails == 0:
                        QMessageBox.information(self, "Empty Mailbox", "The mailbox is empty.")
            else:
                # Iterate over each email ID and fetch the email data
                for email_id in message_numbers:
                    email_id = email_id.decode('utf-8')
                    #current_email += 1
                    progress_text = f"Progress: {current_email}/{total_emails} emails processed"
                    self.error_text.clear()
                    self.error_text.append(progress_text)

                    #self.error_text.clear()
                    #self.error_text.append(f"Processing email ID: {email_id}\n")
                    print(progress_text)
                    try:
                        _, email_data = mail.fetch(email_id, "(RFC822)")
                        if email_data:
                            raw_email = email_data[0][1]

                            # Parse the email message from the raw email data
                            email_message = BytesParser(policy=default).parsebytes(raw_email)

                            # Extract the "From" name from the email headers and decode if necessary
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
                            file_name = f"resulta/{email_provider}/{sanitized_from_name}"

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
                            mail.store(email_id, "+FLAGS", "\\Deleted")
                        else:
                            self.error_text.clear()
                            self.error_text.append(f"Failed to fetch email ID: {email_id}\n")
                    except Exception as e:
                        self.error_text.clear()
                        self.error_text.append(f"Error processing email ID: {email_id}\n")
                        self.error_text.append(f"Error details: {str(e)}\n")
                    finally:
                        current_email += 1
                        progress_text = f"Progress: {current_email}/{total_emails} emails processed"
                        self.error_text.clear()
                        self.error_text.append(progress_text)
                QMessageBox.information(self, "Task Finished", "Email extraction completed successfully.")

        except Exception as e:
            self.error_text.clear()
            self.error_text.setText(f"Error: {str(e)}")
            return








if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = EmailExtractor()
    main_window.setWindowIcon(QIcon("./code.ico"))
    main_window.show()
    sys.exit(app.exec())
