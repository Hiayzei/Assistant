from PyQt6 import  QtWidgets
from PyQt6.QtWidgets import QMessageBox
import subprocess, os

from core.utils import Utils

def GetLibraryPath():
    from window.init import database, TokenManager

    return database.GetAccountInformation(TokenManager.get_token(),"LibraryPath") or "assets/Books"

def SetLibraryPath(NewPath):
    from window.init import database, TokenManager

    return database.SetAccountInformation(TokenManager.get_token(),"LibraryPath",NewPath)
    
class Library(QtWidgets.QWidget):
    def __init__(self, window, show_notification_callback):
        super().__init__(window)
        self.window = window
        self.show_notification_callback = show_notification_callback

        self.initLibrary()

    def initLibrary(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderLabels(["Name", "Type"])
        self.tree.setColumnWidth(0, 300)
        self.tree.setColumnWidth(1, 100)

        self.SetLibraryPath = QtWidgets.QPushButton("Load Books")
        self.SetLibraryPath.clicked.connect(self.SelectPath)
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)

        main_layout.addWidget(self.tree)
        main_layout.addWidget(self.SetLibraryPath)

        self.load_library()
    def SelectPath(self):
        foldername = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        if foldername:
            SetLibraryPath(foldername)
            print(f'Selected folder: {foldername}')
        
        self.load_library()

    def load_library(self):
        root_path = GetLibraryPath()
        if not os.path.exists(root_path):
            QMessageBox.warning(self, "Warning", "The library path does not exist!")
            return

        num_files = Utils.check_count_files_in_directory(root_path,5000)

        if num_files:
            QMessageBox.warning(self, "Warning", "The library path contains more than 5,000 files! This probably will crash your program")
            SetLibraryPath('assets/Books')
            return 

        self.tree.clear()
        self.add_items(self.tree.invisibleRootItem(), root_path)

    def add_items(self, parent_item, path):
        for entry in os.listdir(path):
            entry_path = os.path.join(path, entry)
            item = QtWidgets.QTreeWidgetItem(parent_item, [entry, "Folder" if os.path.isdir(entry_path) else "File"])

            if os.path.isdir(entry_path):
                self.add_items(item, entry_path)

    def on_item_double_clicked(self, item):
        path = self.get_item_path(item)
        type = item.text(1)
        
        if type == "File":
            file_path = f"{GetLibraryPath()}/{path.replace('\\', '/')}"
            if os.path.exists(file_path):
                try:
                    if os.name == 'nt':
                        subprocess.Popen(['start', '', file_path], shell=True)
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Failed to open the file: {e}")
            else:
                QMessageBox.warning(self, "Error", "The selected file does not exist!")

    def get_item_path(self, item):
        path_parts = []
        while item:
            path_parts.append(item.text(0))
            item = item.parent()
        return os.path.join(*reversed(path_parts))