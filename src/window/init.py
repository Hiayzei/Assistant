from PyQt6 import (
    QtCore,
    QtWidgets,
    QtGui
)
from PyQt6.QtGui import (
    QIcon,
    QAction
)
from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QWidget,
    QMenu
)
from PyQt6.QtCore import (
    Qt,
    QEasingCurve,
    QUrl,
    QThread,
    pyqtSignal,
    QSize
)
from PyQt6.QtMultimedia import (
    QMediaPlayer,
    QAudioOutput
)

from core.data import data
from core.richpresence import DiscordRPCSetup
from core.musicmanager import MusicManager
from core.databasemanager import Database
from core.auth_with_google import Auth
from core.token import Token
from core.themes import get_theme, themes, get_theme_saved, set_theme_saved

import os

TokenManager = Token()
database = Database()

from window import home
from window import pomodoro
from window import addictions
from window import writing
from window import library

section_map = {
    "Home": home.Home,
    "Pomodoro": pomodoro.Pomodoro,
    "Writing": writing.Writing,
    "Addictions": addictions.Addictions,
    "Library": library.Library
}


class CustomMessageBox(QtWidgets.QMessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def closeEvent(self, event):
        self.parent().stop_sound()
        super().closeEvent(event)

class Mys(QThread):
    finished = pyqtSignal()

    def run(self):
        DiscordRPCSetup()
        self.finished.emit()

class GoogleAuthThread(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        Auth()
        self.finished.emit()

class CreateWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.Preload()
        self.AnimationOpenUi()
        self.update_interface()

    def Preload(self):
        self.widget_instances = {}
        self.google_thread = None
        self.Mys = None
        self.content_stack = None
        self.music_manager = None

        try:
            self.Mys = Mys()
            self.Mys.start()
        except:
            pass
    
        NotificationAudioUrl = QUrl.fromLocalFile("assets/Sounds/Alarm.mp3")

        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(100)

        self.NotificationAudio = QMediaPlayer()
        self.NotificationAudio.setAudioOutput(self.audio_output)
        self.NotificationAudio.setSource(NotificationAudioUrl)

    def initUI(self):
        self.closeFunction()
        self.setWindowTitle('Assistant')

        if database.account_exists(TokenManager.get_token()):
            self.Preload()
            self.create_menubar()
            self.SetupPages()
        else:
            self.clear_cache()
            self.CreateAuthUI()
            self.create_menubar(True)
    
    def create_menubar(self,Delete=None):
        if Delete:
            self.setMenuBar(None)
            return
        
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Account")
        

        save_action = QAction("Disconnect", self)
        save_action.triggered.connect(self.Disconnect)
        file_menu.addAction(save_action)

        themes_menu = QMenu("Themes", self)
        menubar.addMenu(themes_menu)


        for theme in themes:
            self.add_theme_action(themes_menu, theme)

    def add_theme_action(self, menu, theme_name):
        action = QAction(theme_name, self)
        action.setToolTip(f"Switch to {theme_name} theme")
        action.triggered.connect(lambda: self.apply_theme(theme_name))
        menu.addAction(action)
    
    def apply_theme(self, theme_name):
        self.set_stylesheet( get_theme(theme_name) )
        set_theme_saved(theme_name)
    
    def set_stylesheet(self, stylesheet):
        self.setStyleSheet(stylesheet)
    
    def CreateAuthUI(self):
        self.set_stylesheet(get_theme("Solarized"))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.main_layout = QtWidgets.QVBoxLayout(central_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.google_login_button = QPushButton('Login with Google')
        self.google_login_button.setIcon(QIcon('assets/Images/google.png')) 
        self.google_login_button.setIconSize(QSize(24, 24))

        self.google_login_button.clicked.connect(self.login_with_google)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)
        self.main_layout.addWidget(self.google_login_button)

    def Disconnect(self):
        TokenManager.delete_files()
        
        self.update_interface()

    def update_interface(self):
        self.initUI()

    def login_with_google(self):
        self.google_thread = GoogleAuthThread()
        self.google_thread.finished.connect(self.on_google_auth_finished)
        self.google_thread.start()

    def on_google_auth_finished(self):
        if database.account_exists(TokenManager.get_token()) and self.google_thread:
            self.update_interface()

        self.google_thread = None

    def SetupPages(self):
        self.setStyleSheet( get_theme_saved() )

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QtWidgets.QHBoxLayout(central_widget)
        self.sidebar = QtWidgets.QVBoxLayout()
        self.sidebar.setSpacing(15)
        self.sidebar.setContentsMargins(15, 15, 15, 15)
        self.sidebar.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addLayout(self.sidebar)

        self.content_stack = QtWidgets.QStackedWidget()
        self.main_layout.addWidget(self.content_stack)

        self.init_page = QWidget()
        self.content_stack.addWidget(self.init_page)

        self.SelectSection("Home")

        for SectionName in data["Sections"]:
            SectionButton = QPushButton(SectionName)
            self.sidebar.addWidget(SectionButton)

            SectionButton.clicked.connect(lambda checked, name=SectionName: self.SelectSection(name))

        self.music_manager = MusicManager()

    def update_music_name(self):
        if self.music_manager.current_file:
            music_name = os.path.splitext(self.music_manager.current_file)[0]
            self.MusicText.setText(f"Playing: {music_name}")
        else:
            self.MusicText.setText("")

    def show_notification(self, message):
        msg_box = CustomMessageBox()
        msg_box.setWindowTitle("Pomodoro Finished")
        msg_box.setText(message)
        
        print("Pomodoro Notification")
        self.NotificationAudio.play()
        msg_box.buttonClicked.connect(self.stop_sound)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)

        msg_box.raise_()
        msg_box.activateWindow()
        QtWidgets.QApplication.instance().focusWidget()
        msg_box.exec()

    def stop_sound(self):
        if self.NotificationAudio:
            self.NotificationAudio.stop()

            if self.music_manager:
                self.music_manager.current_file = ""

    def SelectSection(self, button):
        print(f"{button} has been clicked!")

        if button in section_map:
            widget_instance = self.widget_instances.get(button)

            try:
                if widget_instance is None or not widget_instance.isVisible():
                    raise RuntimeError 
            except RuntimeError:
                print(f"Creating new instance for {button}.")
                widget_class = section_map[button]
                widget_instance = widget_class(self, self.show_notification)
                self.widget_instances[button] = widget_instance

            if self.content_stack.indexOf(widget_instance) == -1:
                self.content_stack.addWidget(widget_instance)

            self.content_stack.setCurrentWidget(widget_instance)
        else:
            print(f"No module found for section '{button}'")

    def clear_cache(self):
        try:
            if self.widget_instances:
                self.widget_instances.clear()

            if self.content_stack:
                while self.content_stack.count() > 0:
                    widget = self.content_stack.widget(0)
                    self.content_stack.removeWidget(widget)
                    widget.deleteLater()

            print("Cache cleared and content stack reset.")
        except:
            print(f"Error clearing cache")


    def AnimationOpenUi(self):
        self.resize_effect = QtCore.QPropertyAnimation(self, b"geometry")
        self.resize_effect.setDuration(500)

        screen = QtGui.QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        start_rect = QtCore.QRect(
            screen_geometry.width() // 2 - 50,
            screen_geometry.height() // 2 - 50,
            100,
            100
        )
        
        end_rect = QtCore.QRect(
            screen_geometry.width() // 2 - 400,
            screen_geometry.height() // 2 - 250,
            800,
            600
        )

        self.resize_effect.setStartValue(start_rect)
        self.resize_effect.setEndValue(end_rect)
        self.resize_effect.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self.opacity_effect = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.opacity_effect.setDuration(1000)
        self.opacity_effect.setStartValue(0)
        self.opacity_effect.setEndValue(1)
        self.opacity_effect.setEasingCurve(QEasingCurve.Type.BezierSpline)

        self.resize_effect.start()
        self.opacity_effect.start()

    def closeFunction(self):
        if self.music_manager:
            self.music_manager.exit()
            self.music_manager = None
        if self.Mys:
            self.Mys.exit()
            self.Mys = None
        if self.google_thread:
            self.google_thread.exit()
            self.google_thread = None

        try:
            if addictions.TableGlobalValue:
                try:
                    addictions.TableGlobalValue.saveToFile('main.xlsx')
                except Exception as e:
                    QtWidgets.QMessageBox.warning(self, 'Erro', f'Save Error:: {str(e)}')
                    return
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Erro', f'Unexpected Error:: {str(e)}')

    def closeEvent(self, event):
        data['WindowClosed'] = True

        print("Window has been closed")
        self.closeFunction()
        event.accept()