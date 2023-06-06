import os
import re
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox, QProgressBar

class ReturnPathExtractorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.folder_path = ""
        self.output_file = "Return_Path.txt"
        self.return_path_pattern = r'Return-Path:\s*(.+)'

        self.setWindowTitle("Return-Path Extractor")

        self.folder_label = QLabel("Select Folder:")
        self.folder_button = QPushButton("Browse")
        self.folder_button.clicked.connect(self.select_folder)

        self.extract_button = QPushButton("Extract Return-Paths")
        self.extract_button.clicked.connect(self.extract_return_paths)

        self.progress_label = QLabel("Progress:")
        self.progress_bar = QProgressBar()

        layout = QVBoxLayout()
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_button)
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

    def extract_return_paths(self):
        if self.folder_path:
            return_paths = []
            total_files = 0
            processed_files = 0

            for filename in os.listdir(self.folder_path):
                if filename.endswith('.txt'):
                    total_files += 1

            for filename in os.listdir(self.folder_path):
                if filename.endswith('.txt'):
                    file_path = os.path.join(self.folder_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        matches = re.findall(self.return_path_pattern, content, re.IGNORECASE)
                        return_paths.extend(matches)
                    
                    processed_files += 1
                    self.update_progress(processed_files, total_files)

            return_paths = list(set(return_paths))
            return_paths = [return_path.replace("<", "").replace(">", "") for return_path in return_paths]

            if not os.path.exists(self.output_file):
                open(self.output_file, 'w').close()

            with open(self.output_file, 'w', encoding='utf-8') as output:
                for return_path in return_paths:
                    output.write(return_path + '\n')

            print(f'Return paths extracted and saved to {self.output_file}.')

            # Display a notification when the task finishes
            self.show_notification("Return-Path Extraction", "Task finished successfully!")

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
