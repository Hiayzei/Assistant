from PyQt6 import QtGui
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QMessageBox

import os, random

def GetMusicPath():
    from window.init import database, TokenManager

    return database.GetAccountInformation(TokenManager.get_token(),"PlaylistsPath") or "assets/Sounds/Playlists"

def SetMusicPath(NewMusicPath):
    from window.init import database, TokenManager

    database.SetAccountInformation(TokenManager.get_token(),"PlaylistsPath",NewMusicPath)

class MusicManager:
    def __init__(self, update_music_name_callback=None):
        self.PlayingMusic = False
        self.MusicPlaying = ""

        self.played_files = set()

        self.path = GetMusicPath()

        if not os.path.exists(self.path):
            SetMusicPath("assets/Playlists")
            QMessageBox.warning(None, "Warning", "No playlists were found")
            return

        items = os.listdir(self.path)
        folders = [item for item in items if os.path.isdir(os.path.join(self.path, item))]

        if folders:
            self.playlist_folder = f"{self.path}/{folders[0]}"
            self.music_files = self.load_music_files()

        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(100)

        self.Music = QMediaPlayer()
        self.Music.setAudioOutput(self.audio_output)
        
        self.played_files = set()
        self.current_file = ""

        if update_music_name_callback:
            self.update_music_name_callback = update_music_name_callback

        self.Music.mediaStatusChanged.connect(self.on_media_status_changed)
        
    def SetPath(self):
        self.path = GetMusicPath()
        items = os.listdir(self.path)
        folders = [item for item in items if os.path.isdir(os.path.join(self.path, item))]

        if folders:
            self.playlist_folder = f"{self.path}/{folders[0]}"
            self.music_files = self.load_music_files()

    def change_playlist(self, button, newindex):
        self.playlist_folder = f'{self.path}/{newindex}'
        self.music_files = self.load_music_files()
        self.played_files.clear()
        self.current_file = ""

        if self.PlayingMusic:
            self.Music.stop()
            self.MusicPlaying = ""
            button.setIcon(QtGui.QIcon('assets/Images/playbutton.png'))
            self.PlayingMusic = False

    def set_volume(self, s):
        volume = s.volume_slider.value() / 100
        self.audio_output.setVolume(volume)

    def load_playlists(self):
        playlists = []
        if self.path != "" and os.listdir(self.path):
            playlists = [name for name in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, name))]
        return playlists

    def load_music_files(self):
        print(f"Checking folder path: {self.playlist_folder}")
        if not os.path.exists(self.playlist_folder):
            print(f"Error: The path does not exist: {self.playlist_folder}")
            return []
        
        try:
            music_files = [f for f in os.listdir(self.playlist_folder) if f.endswith('.mp3')]
            random.shuffle(music_files)
            return music_files

        except Exception as e:
            print(f"Exception occurred: {e}")
            return []
        
    def play_next_song(self):
        try:
            if len(self.played_files) == len(self.music_files):
                self.played_files.clear()
                self.music_files = self.load_music_files()

            available_files = [f for f in self.music_files if f not in self.played_files]
            if available_files:
                self.current_file = random.choice(available_files)
                self.MusicPlaying = self.current_file
                self.played_files.add(self.current_file)
                song_path = os.path.join(self.playlist_folder, self.current_file)
                self.Music.setSource(QUrl.fromLocalFile(song_path))
                self.Music.play()
                if hasattr(self, 'update_music_name_callback'):
                    self.update_music_name_callback()
                return True
        except:
            QMessageBox.warning(None, "Warning", "No playlists were found")
            return False

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.play_next_song()

    def exit(self):
        self.Music.stop()

        self.Music.mediaStatusChanged.disconnect(self.on_media_status_changed)
        self.Music.setSource(QUrl())
        self.Music.setAudioOutput(None)
        self.Music = None

        self.audio_output = None

        self.current_file = ""
        self.MusicPlaying = ""
        self.played_files.clear()
        self.PlayingMusic = False
        print("MusicManager resources have been cleaned up.")
        
    def playlist_manager(self, button=None):
        self.PlayingMusic = not self.PlayingMusic

        if self.PlayingMusic:
            if self.play_next_song():
                button.setIcon(QtGui.QIcon('assets/Images/pausebutton.png'))
            else:
                self.PlayingMusic = False
        else:
            self.Music.stop()
            self.current_file = ""
            if button:
                button.setIcon(QtGui.QIcon('assets/Images/playbutton.png'))