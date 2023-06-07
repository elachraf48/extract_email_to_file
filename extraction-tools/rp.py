import os
import re
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox, QProgressBar, QComboBox

class ReturnPathExtractorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.folder_path = ""
        self.output_file = ""
        self.email_provider = ""
        self.extract_button = None
        self.return_path_pattern = ""

        self.setWindowTitle("Return-Path Extractor")

        self.folder_label = QLabel("Select Folder:")
        self.folder_button = QPushButton("Browse")
        self.folder_button.clicked.connect(self.select_folder)

        self.email_provider_combo = QComboBox()
        self.email_provider_combo.addItems(["Return-Path", "Received-SPF", "From", "Message-ID", "Subject"])
        self.email_provider_combo.currentIndexChanged.connect(self.update_email_provider)

        self.extract_button = QPushButton("Extract")
        self.extract_button.clicked.connect(self.extract_data)
        self.extract_button.setEnabled(False)

        self.progress_label = QLabel("Progress:")
        self.progress_bar = QProgressBar()

        layout = QVBoxLayout()
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_button)
        layout.addWidget(self.email_provider_combo)
        layout.addWidget(self.extract_button)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def select_folder(self):
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.FileMode.Directory)
        folder_path = folder_dialog.getExistingDirectoryUrl(self, "Select Folder")
        if folder_path:
            self.folder_path = folder_path.toLocalFile()
            self.update_extract_button_state()

    def update_email_provider(self, index):
        self.email_provider = self.email_provider_combo.currentText()
        self.update_extract_button_state()

    def update_extract_button_state(self):
        if self.folder_path and self.email_provider:
            self.extract_button.setEnabled(True)
        else:
            self.extract_button.setEnabled(False)

    def extract_data(self):
        if self.folder_path:
            self.output_file = self.email_provider + ".txt"
            self.return_path_pattern = r'^' + self.email_provider + r':\s*(.+)'

            extracted_data = []
            total_files = 0
            processed_files = 0

            for filename in os.listdir(self.folder_path):
                if filename.endswith('.txt'):
                    total_files += 1

            for filename in os.listdir(self.folder_path):
                if filename.endswith('.txt'):
                    file_path = os.path.join(self.folder_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        for line in lines:
                            match = re.match(self.return_path_pattern, line, re.IGNORECASE)
                            if match:
                                extracted_data.append(match.group(1))

                    processed_files += 1
                    self.update_progress(processed_files, total_files)

            extracted_data = list(set(extracted_data))

            if not os.path.exists(self.output_file):
                open(self.output_file, 'w').close()

            with open(self.output_file, 'w', encoding='utf-8') as output:
                for data in extracted_data:
                    output.write(data + '\n')

            print(f'Data extracted and saved to {self.output_file}.')

            # Display a notification when the task finishes
            self.show_notification("Data Extraction", "Task finished successfully!")

    def update_progress(self, value, maximum):
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(value)

    def show_notification(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()

if __name__ == "__main__":
    app = QApplication([])
    window = ReturnPathExtractorWindow()
    window.show()
    app.exec()
