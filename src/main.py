import sys
from window.init import CreateWindow
from PyQt6 import (
    QtWidgets,
    QtGui
)

def main():
    app = QtWidgets.QApplication([])
    app_icon = QtGui.QIcon("Assets/Images/Icon.png")

    app.setWindowIcon(app_icon)

    window = CreateWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()