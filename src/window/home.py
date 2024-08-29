from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from core.utils import Utils
from core.richpresence import RPCMenu

class TextLoaderThread(QThread):
    text_loaded = pyqtSignal(str, str)

    def run(self):
        content, author = Utils.get_random_phrases()
        self.text_loaded.emit(content, author)

def GetJsonInformations(Information):
    from window.init import database, TokenManager

    return database.GetAccountInformation(TokenManager.get_token(),Information)

def SetJsonInformations(Information,NewValue):
    from window.init import database, TokenManager

    return database.SetAccountInformation(TokenManager.get_token(),Information,NewValue)

        
class Home(QtWidgets.QWidget):
    def __init__(self, window, show_notification_callback):
        super().__init__(window)
        self.window = window
        self.show_notification_callback = show_notification_callback

        self.initHome()

    def initHome(self):
        print("Home has been loaded!")

        self.init_layout = QtWidgets.QVBoxLayout(self)

        self.HourText = QtWidgets.QLabel(Utils.get_current_time(), alignment=Qt.AlignmentFlag.AlignCenter)
        self.HourText.setStyleSheet("border: none; font-size: 32px;")
        self.init_layout.addWidget(self.HourText)

        self.MusicText = QtWidgets.QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)
        self.MusicText.setStyleSheet("border: none;")
        self.init_layout.addWidget(self.MusicText)

        self.RandomText = QtWidgets.QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)
        self.RandomText.setStyleSheet("border: none; font-size: 18px;")
        self.RandomText.setWordWrap(True)
        self.init_layout.addWidget(self.RandomText)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        RPCMenu(self)

        self.start_text_loading()
    def start_text_loading(self):
        self.text_loader_thread = TextLoaderThread()
        self.RandomText.setText("Loading...")
        self.text_loader_thread.text_loaded.connect(self.update_text)
        self.text_loader_thread.start()

    def update_text(self, content, author):
        self.RandomText.setText(f"{content} \n\n-{author}")

    def update_time(self):
        self.HourText.setText(Utils.get_current_time())
