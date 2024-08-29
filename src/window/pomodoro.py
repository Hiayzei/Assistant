from PyQt6.QtCore import Qt
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import QSize, QUrl, Qt

from core.musicmanager import MusicManager, GetMusicPath, SetMusicPath

import os

def GetFirstFolder():
    music_path = GetMusicPath()
    
    if music_path and os.path.isdir(music_path):
        entries = os.listdir(music_path)
        
        directories = [entry for entry in entries if os.path.isdir(os.path.join(music_path, entry))]
        if directories:
            return os.path.join(music_path, directories[0])
        else:
            return None
    else:
        return None

class Pomodoro(QtWidgets.QWidget):
    def __init__(self,window,show_notification_callback):
        super().__init__(window)
        self.window = window

        self.OnPomodoro = False
        self.pomodoro_duration = 25 * 60
        self.break_duration = 5 * 60
        self.timer_pomodoro = QtCore.QTimer()
        self.timer_pomodoro.timeout.connect(self.update_pomodoro_timer)
        self.Pomodoro_Status = "None"
        self.show_notification_callback = show_notification_callback

        self.initPomodoro()

    def initPomodoro(self):
        print("Pomodoro has been loaded!")

        self.init_layout = QtWidgets.QVBoxLayout(self)

        self.pomodoro_label = QtWidgets.QLabel("Pomodoro Timer", alignment=Qt.AlignmentFlag.AlignCenter)
        self.pomodoro_label.setStyleSheet("border: none;")
        self.init_layout.addWidget(self.pomodoro_label)

        self.pomodoro_status = QtWidgets.QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)
        self.pomodoro_status.setStyleSheet("border: none;")
        self.init_layout.addWidget(self.pomodoro_status)

        self.pomodoro_timer = QtWidgets.QLabel("25:00", alignment=Qt.AlignmentFlag.AlignCenter)
        self.pomodoro_timer.setStyleSheet("border: none;")
        self.init_layout.addWidget(self.pomodoro_timer)

        self.start_button = QtWidgets.QPushButton("Start")
        self.start_button.clicked.connect(self.start_pomodoro)

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(100)
        self.player.setSource(QUrl.fromLocalFile("assets/Sounds/Alarm.mp3"))

        self.Music = QMediaPlayer()
        self.Music.setAudioOutput(self.audio_output)

        self.MusicManager = MusicManager(self.update_music_name)

        self.playlist_folder = GetFirstFolder()
        self.played_files = set()
        self.current_file = ""

        self.MusicButton = QtWidgets.QPushButton()
        self.MusicButton.setIcon(QtGui.QIcon('assets/Images/playbutton.png'))
        self.MusicButton.setIconSize(QSize(50, 50))
        self.MusicButton.clicked.connect(lambda: self.MusicManager.playlist_manager(self.MusicButton))

        self.playlist_selector = QtWidgets.QComboBox()
        self.playlist_selector.addItems(self.MusicManager.load_playlists())
        self.playlist_selector.currentIndexChanged.connect(
            lambda index: self.MusicManager.change_playlist(self.MusicButton, self.playlist_selector.itemText(index))
        )
        self.volume_slider = QtWidgets.QSlider( Qt.Orientation.Horizontal )
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(int(self.audio_output.volume() * 100))
        self.volume_slider.valueChanged.connect( lambda: self.MusicManager.set_volume(self ) )

        self.SetMusicPath = QtWidgets.QPushButton("Load Playlists")
        self.SetMusicPath.clicked.connect(self.SelectPath)
       
        self.init_layout.addWidget(self.start_button)
        self.init_layout.addWidget(self.playlist_selector)
        self.init_layout.addWidget(self.volume_slider)
        self.init_layout.addWidget(self.MusicButton)
        self.init_layout.addWidget(self.SetMusicPath)
        
    def SelectPath(self):
        foldername = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        if foldername:
            print(f'Selected folder: {foldername}')

            SetMusicPath(foldername)
            self.playlist_selector.clear()
            self.MusicManager.SetPath()
            self.playlist_selector.addItems(self.MusicManager.load_playlists())

    def update_music_name(self):
        if self.MusicManager.current_file:
            music_name = os.path.splitext(self.MusicManager.current_file)[0]
            

    def close_pomodoro(self):
        self.OnPomodoro = False
        if self.timer_pomodoro:
            self.timer_pomodoro.stop()
        self.pomodoro_duration = 25 * 60
        self.break_duration = 5 * 60
        self.pomodoro_timer.setText("25:00")
        self.start_button.setText("Start")
        self.pomodoro_status.setText("")
        self.Pomodoro_Status = "None"

    def start_pomodoro(self):
        if self.OnPomodoro:
            self.close_pomodoro()
        else:
            self.OnPomodoro = True
            self.timer_pomodoro.start(1000)
            self.start_button.setText("Finish")
            self.pomodoro_status.setText("")
            self.Pomodoro_Status = "Working"

    def update_pomodoro_timer(self):
        if self.pomodoro_duration > 0:
            self.pomodoro_duration -= 1
            minutes, seconds = divmod(self.pomodoro_duration, 60)
            self.pomodoro_timer.setText(f"{minutes:02}:{seconds:02}")
            self.pomodoro_status.setText("Working")
        elif self.break_duration > 0:
            if self.Pomodoro_Status == "Working":
                self.show_notification_callback("Pomodoro finished! Time for a break")
                self.Pomodoro_Status = "Break"
            self.break_duration -= 1
            minutes, seconds = divmod(self.break_duration, 60)
            self.pomodoro_timer.setText(f"{minutes:02}:{seconds:02}")
            self.pomodoro_status.setText("Break")
        else:
            self.timer_pomodoro.stop()
            self.start_button.setText("Finish")
            self.pomodoro_timer.setText("Pomodoro has been completed!")
            self.pomodoro_duration = 25 * 60
            self.show_notification_callback("Pomodoro finished! Time for a new one")
            self.close_pomodoro()