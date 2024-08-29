from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from core.data import data
from pypresence import Presence
from core.utils import Utils
import time
import sys, os

languagues = ["py","cpp"]

def GetValue(Name):
    from window.init import database, TokenManager

    return database.GetAccountInformation(TokenManager.get_token(),Name)

def get_last_modified_script():
    user_home = os.path.expanduser("~")
    directory = os.path.join(user_home, "AppData", "Roaming", "Code", "User", "History")

    if not os.path.exists(directory):
        return None
    
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            files.append((filepath, os.path.getmtime(filepath)))

    if not files:
        return None

    latest_file = max(files, key=lambda x: x[1])

    for language in languagues:
        if language in latest_file[0]:
            return language

def update_rpc():
    print("Trying to connect with Discord RPC")
    client_id = GetValue("ClientId")
    if not client_id:
        print("ClientId not found.")
        return

    rpc = Presence(client_id)
    time.sleep(2)

    try:
        rpc.connect()
    except Exception as e:
        print(f"Error connecting to Discord RPC: {e}")
        return

    print("Connected with Discord RPC")
    start_time = time.time()

    while True:
        try:
            if GetValue("RichPresenceAutoStart") and not data.get('WindowClosed', False):
                elapsed_time = int(time.time() - start_time)
                elapsed_minutes = elapsed_time // 60
                elapsed_seconds = elapsed_time % 60
                formatted_elapsed_time = f"{elapsed_minutes}m {elapsed_seconds}s"

                rblxopen = Utils.is_process_running("RobloxStudioBeta.exe")
                vscodeopen = Utils.is_process_running("Code.exe")

                large_image = None
                large_text = None
                small_image = None
                small_text = None

                mode = GetValue('RPCMode')
                if mode == "Coding":
                    if rblxopen:
                        large_text = "Coding on Roblox Studios"
                        large_image = "rblx"
                        small_image = "luau"
                        small_text = "luau"
                    elif vscodeopen:
                        Languague = get_last_modified_script()

                        large_text = "Coding on VS Code"
                        large_image = "vscode"
                        small_image = Languague
                        small_text = Languague
                    else:
                        mode = "Idling"
                else:
                    large_image = mode.lower()

                rpc.update(
                    state="Time Elapsed: {}".format(formatted_elapsed_time),
                    details=mode,
                    large_image=large_image,
                    large_text=large_text,
                    small_image=small_image,
                    small_text=small_text,
                    buttons=[
                        {"label": "Portfolio", "url": "https://hiayzei.github.io/"}
                    ],
                )

            else:
                if data.get('WindowClosed', False):
                    sys.exit()
                break
        except Exception as e:
            print(f"Error during RPC update: {e}")
            break

        time.sleep(1)

    rpc.close()

def Init():
    while True:
        if GetValue("RichPresenceAutoStart") and GetValue("ClientId"):
            update_rpc()
        time.sleep(1)

def DiscordRPCSetup():
    Init()


class ToggleSwitch(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setFixedSize(50, 50)
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self.update_style)

    def update_style(self, checked):
        from window.home import SetJsonInformations
        if checked:
            self.setText("On")
        else:
            self.setText("Off")

        SetJsonInformations("RichPresenceAutoStart",checked)

class RPCMenu:
    def __init__(self, window):
        super().__init__()
        self.window = window

        self.InitRPCMenu()
    def InitRPCMenu(self):
        from window.home import GetJsonInformations

        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.toggle_switch = ToggleSwitch("On" if GetJsonInformations("RichPresenceAutoStart") else "Off", self)
        self.toggle_switch.setChecked(GetJsonInformations("RichPresenceAutoStart"))
        self.horizontal_layout.addWidget(self.toggle_switch)

        self.mode_list = QtWidgets.QComboBox()
        self.mode_list.addItems(["Coding","Studying","Reading"])
        self.mode_list.currentIndexChanged.connect(
            lambda index: self.change_mode(self.mode_list.itemText(index))
        )
        self.mode_list.setCurrentIndex(0)
        self.horizontal_layout.addWidget(self.mode_list)

        self.clientid_box = QtWidgets.QLineEdit()
        ClientID = GetJsonInformations("ClientId")
        self.clientid_box.setPlaceholderText("Insert ClientID" if ClientID == "" else f"Current ClientID: {ClientID}")
        self.clientid_box.textEdited.connect(
            lambda clientid: self.change_clientid(clientid)
        )
        self.horizontal_layout.addWidget(self.clientid_box)

        self.window.init_layout.addLayout(self.horizontal_layout)
    def change_mode(self,newitem):
        from window.home import SetJsonInformations
        SetJsonInformations("RPCMode",newitem)

    def change_clientid(self,clientid):
        from window.home import SetJsonInformations
        SetJsonInformations("ClientId",clientid)
