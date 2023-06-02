# Email Extraction Tool

This is a Python script that extracts emails from IMAP servers such as Outlook, Yahoo, and Gmail. It saves the extracted emails as text files in specific folders based on the email provider.

## Prerequisites

Before running the script, make sure you have the following Python modules installed:

- `imapclient`: Install using `pip install imapclient`
- `email`: Install using `pip install email`
- `os`: Install using `pip install os`
- `regex`: Install using `pip install regex`
- `tkinter`: Install using `pip install tkinter`
- `gspread`: Install using `pip install gspread`
- `oauth2client`: Install using `pip install oauth2client`
- `json`: Install using `pip install json`

## Usage

1. Clone this repository or download the script file (`extract_emails.py`).

2. Open the terminal or command prompt and navigate to the directory where the script is located.

3. Run the script using the command `python extract_emails.py`.

4. A GUI window will appear where you can select the email provider and enter your email address and password.

5. Click the "Submit" button to save the email and password. If the email provider is not supported, an error message will be displayed.

6. After submitting the email and password, the script will connect to the IMAP server and start extracting emails. The progress will be displayed in the GUI window.

7. Extracted emails will be saved as text files in the corresponding provider's folder (`resulta/outlook`, `resulta/yahoo`, `resulta/gmail`).

## Notes

- The script uses the `data.json` file to store the email and password data. If the file doesn't exist, it will be created automatically.

- The `extract_emails` function retrieves emails from the selected email provider's IMAP server. It fetches all emails from the "INBOX" mailbox and saves each email as a separate text file.

- The `add_email_password` function opens a new window where you can enter your email address and password. The data is then saved to the `data.json` file.

- The script supports Outlook, Hotmail, Yahoo, and Gmail as email providers. You can add support for more providers by extending the code.

- If an error occurs during the email extraction process, an error message will be displayed in the GUI window.

- You can pause the email extraction process by clicking the "Pause" button in the GUI window. To resume, click the "Resume" button.

- The script will automatically delete the extracted emails from the mailbox after saving them as text files.

- The script uses the `decode_header` function from the `email.header` module to extract the sender's name from the email headers.

- The extracted emails are saved with filenames based on the sender's name and the email provider. The filenames are sanitized to remove invalid characters and limited to 40 characters.

- If multiple emails have the same sender's name, a count will be added to the filename to avoid overwriting existing files.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
