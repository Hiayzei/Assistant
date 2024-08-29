def elegant_theme():
    return """
    QWidget {
        background-color: #1E1E1E;
        color: #E0E0E0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 14px;
        border: none;
    }

    QLabel {
        color: #FFD700;
        padding: 8px;
        font-size: 16px;
        font-weight: bold;
        border: none;
    }

    QPushButton {
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #4CAF50, stop:1 #81C784);
        color: white;
        border: 2px solid #4CAF50;
        border-radius: 12px;
        padding: 12px 30px;
        font-size: 15px;
        font-weight: 600;
    }

    QPushButton:hover {
        background-color: #45A049;
    }

    QPushButton:pressed {
        background-color: #388E3C;
    }

    QPushButton:disabled {
        background-color: #9E9E9E;
        color: #CCCCCC;
        border: 2px solid #757575;
    }

    QWidget[role='important'] {
        background-color: #3C3F41;
        color: #FFD700;
        border-radius: 10px;
        padding: 12px;
    }

    QWidget[role='highlight'] {
        background-color: #3C3F41;
        color: #FFD700;
        border-radius: 10px;
        padding: 12px;
        font-weight: bold;
    }

    QComboBox {
        background-color: #3C3F41;
        color: #FFD700;
        border: 1px solid #5A5A5A;
        border-radius: 5px;
        padding: 5px;
    }

    QComboBox::drop-down {
        border-left: 1px solid #5A5A5A;
        background-color: #2B2B2B;
    }

    QLineEdit {
        background-color: #3C3F41;
        color: #FFD700;
        border: 1px solid #5A5A5A;
        border-radius: 5px;
        padding: 5px;
    }

    QListView {
        background-color: #2B2B2B;
        color: #FFD700;
        border: 1px solid #5A5A5A;
    }

    QListView::item:selected {
        background-color: #388E3C;
        color: white;
        font-weight: bold;
    }

    QProgressBar {
        background-color: #2C2C2C;
        border: 2px solid #5A5A5A;
        border-radius: 10px;
        text-align: center;
        color: #FFD700;
        padding: 5px;
        font-size: 15px;
    }

    QProgressBar::chunk {
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #6BCB77, stop:1 #4CAF50);
        border-radius: 10px;
    }

    QSlider::groove:horizontal {
        height: 8px;
        background: #5A5A5A;
        border-radius: 4px;
    }

    QSlider::handle:horizontal {
        background: #388E3C;
        width: 18px;
        margin: -5px 0;
        border-radius: 9px;
    }

    QTabBar::tab {
        background-color: #2C2C2C;
        color: #FFD700;
        padding: 10px;
        border: 2px solid #5A5A5A;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        margin-right: 2px;
    }

    QTabBar::tab:selected {
        background-color: #388E3C;
        color: white;
        font-weight: bold;
    }

    QTreeView {
        background-color: #2B2B2B;
        color: #FFD700;
        border: 1px solid #5A5A5A;
    }

    QTreeView::item:selected {
        background-color: #388E3C;
        color: white;
    }

    QToolTip {
        background-color: #5A5A5A;
        color: white;
        border: 1px solid #FFD700;
        padding: 5px;
        border-radius: 5px;
    }

    QMenuBar {
        background-color: #2B2B2B;
        color: #D3D3D3;
        padding: 8px;
    }

    QMenuBar::item:selected {
        background-color: #388E3C;
        color: white;
        font-weight: bold;
        border-radius: 5px;
    }

    QStatusBar {
        background-color: #2B2B2B;
        color: #D3D3D3;
        padding: 5px;
        font-size: 14px;
    }

    QHeaderView::section {
        background-color: #3C3F41;
        color: #FFD700;
        padding: 5px;
        border: 1px solid #5A5A5A;
        border-radius: 5px;
    }

    QToolButton {
        background-color: #3C3F41;
        color: #FFD700;
        border: 1px solid #5A5A5A;
        border-radius: 5px;
        padding: 5px;
    }

    QToolButton:checked {
        background-color: #388E3C;
        color: white;
        font-weight: bold;
    }

    QScrollBar:vertical {
        background: #2C2C2C;
        width: 15px;
    }

    QScrollBar::handle:vertical {
        background: #5A5A5A;
        min-height: 20px;
        border-radius: 7px;
    }
    """

def minimal_black_theme():
    return """
    QWidget {
        background-color: #121212;
        color: #E0E0E0;
        font-family: 'Segoe UI', Tahoma, Geneva, sans-serif;
        font-size: 14px;
        border: none;
    }

    QLabel {
        color: #B0B0B0;
        font-size: 14px;
        padding: 6px;
        border: none;
    }

    QPushButton {
        background-color: #1F1F1F;
        color: #E0E0E0;
        border: 1px solid #333333;
        border-radius: 5px;
        padding: 8px 16px;
        font-size: 14px;
    }

    QPushButton:hover {
        background-color: #333333;
    }

    QPushButton:pressed {
        background-color: #444444;
    }

    QPushButton:disabled {
        background-color: #2C2C2C;
        color: #777777;
        border: 1px solid #555555;
    }

    QLineEdit {
        background-color: #1F1F1F;
        color: #E0E0E0;
        border: 1px solid #333333;
        border-radius: 5px;
        padding: 6px;
    }

    QComboBox {
        background-color: #1F1F1F;
        color: #E0E0E0;
        border: 1px solid #333333;
        border-radius: 5px;
        padding: 6px;
    }

    QComboBox::drop-down {
        border-left: 1px solid #333333;
        background-color: #2C2C2C;
    }

    QComboBox QAbstractItemView {
        background-color: #1F1F1F;
        color: #E0E0E0;
        selection-background-color: #333333;
        selection-color: #FFFFFF;
    }

    QListView, QTreeView {
        background-color: #1F1F1F;
        color: #E0E0E0;
        border: 1px solid #333333;
    }

    QListView::item:selected, QTreeView::item:selected {
        background-color: #333333;
        color: #FFFFFF;
    }

    QProgressBar {
        background-color: #1F1F1F;
        border: 1px solid #333333;
        border-radius: 3px;
        text-align: center;
        color: #B0B0B0;
    }

    QProgressBar::chunk {
        background-color: #3E3E3E;
    }

    QSlider::groove:horizontal {
        height: 6px;
        background: #333333;
        border-radius: 3px;
    }

    QSlider::handle:horizontal {
        background: #4F4F4F;
        width: 12px;
        border-radius: 6px;
    }

    QSlider::groove:vertical {
        width: 6px;
        background: #333333;
        border-radius: 3px;
    }

    QSlider::handle:vertical {
        background: #4F4F4F;
        height: 12px;
        border-radius: 6px;
    }

    QScrollBar:vertical, QScrollBar:horizontal {
        background: #121212;
        width: 12px;
        height: 12px;
    }

    QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
        background: #333333;
        min-height: 20px;
        min-width: 20px;
        border-radius: 6px;
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        background: #2C2C2C;
    }

    QScrollBar::up-arrow, QScrollBar::down-arrow, QScrollBar::left-arrow, QScrollBar::right-arrow {
        border: none;
        background: #2C2C2C;
        color: #777777;
    }

    QMenuBar {
        background-color: #121212;
        color: #B0B0B0;
        padding: 4px;
    }

    QMenuBar::item {
        background-color: #121212;
        color: #B0B0B0;
        padding: 8px;
    }

    QMenuBar::item:selected {
        background-color: #333333;
        color: #FFFFFF;
    }

    QMenu {
        background-color: #1F1F1F;
        color: #E0E0E0;
        border: 1px solid #333333;
    }

    QMenu::item:selected {
        background-color: #333333;
        color: #FFFFFF;
    }

    QStatusBar {
        background-color: #1F1F1F;
        color: #B0B0B0;
        padding: 4px;
    }

    QTabWidget::pane {
        background-color: #121212;
        border: none;
    }

    QTabBar::tab {
        background-color: #1F1F1F;
        color: #B0B0B0;
        padding: 8px 16px;
        border: 1px solid #333333;
        border-bottom: none;
    }

    QTabBar::tab:selected {
        background-color: #333333;
        color: #FFFFFF;
    }

    QToolButton {
        background-color: #1F1F1F;
        color: #E0E0E0;
        border: 1px solid #333333;
        padding: 8px;
        border-radius: 3px;
    }

    QToolButton:checked {
        background-color: #333333;
        color: #FFFFFF;
    }

    QToolTip {
        background-color: #333333;
        color: #FFFFFF;
        padding: 6px;
        border: none;
        border-radius: 3px;
    }

    QFrame {
        background-color: #121212;
        border: 1px solid #333333;
    }

    QGroupBox {
        border: 1px solid #333333;
        border-radius: 5px;
        margin-top: 10px;
        background-color: #1F1F1F;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        padding: 4px 10px;
        color: #E0E0E0;
    }

    QHeaderView::section {
        background-color: #1F1F1F;
        color: #E0E0E0;
        padding: 6px;
        border: 1px solid #333333;
    }

    QTableView {
        background-color: #121212;
        color: #E0E0E0;
        border: 1px solid #333333;
        gridline-color: #333333;
    }

    QTableView::item:selected {
        background-color: #333333;
        color: #FFFFFF;
    }
    """

def minimal_white_theme():
    return """
    QWidget {
        background-color: #FFFFFF;
        color: #333333;
        font-family: 'Segoe UI', Tahoma, Geneva, sans-serif;
        font-size: 14px;
        border: none;
    }

    QLabel {
        color: #333333;
        font-size: 14px;
        padding: 6px;
        border: none;
    }

    QPushButton {
        background-color: #F0F0F0;
        color: #333333;
        border: 1px solid #CCCCCC;
        border-radius: 5px;
        padding: 8px 16px;
        font-size: 14px;
    }

    QPushButton:hover {
        background-color: #E0E0E0;
    }

    QPushButton:pressed {
        background-color: #D0D0D0;
    }

    QPushButton:disabled {
        background-color: #F5F5F5;
        color: #AAAAAA;
        border: 1px solid #DDDDDD;
    }

    QLineEdit {
        background-color: #F9F9F9;
        color: #333333;
        border: 1px solid #CCCCCC;
        border-radius: 5px;
        padding: 6px;
    }

    QComboBox {
        background-color: #F9F9F9;
        color: #333333;
        border: 1px solid #CCCCCC;
        border-radius: 5px;
        padding: 6px;
    }

    QComboBox::drop-down {
        border-left: 1px solid #CCCCCC;
        background-color: #FFFFFF;
    }

    QComboBox QAbstractItemView {
        background-color: #FFFFFF;
        color: #333333;
        selection-background-color: #E0E0E0;
        selection-color: #000000;
    }

    QListView, QTreeView {
        background-color: #FFFFFF;
        color: #333333;
        border: 1px solid #CCCCCC;
    }

    QListView::item:selected, QTreeView::item:selected {
        background-color: #E0E0E0;
        color: #000000;
    }

    QProgressBar {
        background-color: #F0F0F0;
        border: 1px solid #CCCCCC;
        border-radius: 3px;
        text-align: center;
        color: #666666;
    }

    QProgressBar::chunk {
        background-color: #3E99F0;
    }

    QSlider::groove:horizontal {
        height: 6px;
        background: #CCCCCC;
        border-radius: 3px;
    }

    QSlider::handle:horizontal {
        background: #AAAAAA;
        width: 12px;
        border-radius: 6px;
    }

    QSlider::groove:vertical {
        width: 6px;
        background: #CCCCCC;
        border-radius: 3px;
    }

    QSlider::handle:vertical {
        background: #AAAAAA;
        height: 12px;
        border-radius: 6px;
    }

    QScrollBar:vertical, QScrollBar:horizontal {
        background: #FFFFFF;
        width: 12px;
        height: 12px;
    }

    QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
        background: #CCCCCC;
        min-height: 20px;
        min-width: 20px;
        border-radius: 6px;
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        background: #F5F5F5;
    }

    QScrollBar::up-arrow, QScrollBar::down-arrow, QScrollBar::left-arrow, QScrollBar::right-arrow {
        border: none;
        background: #E0E0E0;
        color: #777777;
    }

    QMenuBar {
        background-color: #FFFFFF;
        color: #333333;
        padding: 4px;
    }

    QMenuBar::item {
        background-color: #FFFFFF;
        color: #333333;
        padding: 8px;
    }

    QMenuBar::item:selected {
        background-color: #E0E0E0;
        color: #000000;
    }

    QMenu {
        background-color: #FFFFFF;
        color: #333333;
        border: 1px solid #CCCCCC;
    }

    QMenu::item:selected {
        background-color: #E0E0E0;
        color: #000000;
    }

    QStatusBar {
        background-color: #F0F0F0;
        color: #666666;
        padding: 4px;
    }

    QTabWidget::pane {
        background-color: #FFFFFF;
        border: none;
    }

    QTabBar::tab {
        background-color: #F0F0F0;
        color: #333333;
        padding: 8px 16px;
        border: 1px solid #CCCCCC;
        border-bottom: none;
    }

    QTabBar::tab:selected {
        background-color: #FFFFFF;
        color: #000000;
    }

    QToolButton {
        background-color: #F9F9F9;
        color: #333333;
        border: 1px solid #CCCCCC;
        padding: 8px;
        border-radius: 3px;
    }

    QToolButton:checked {
        background-color: #E0E0E0;
        color: #000000;
    }

    QToolTip {
        background-color: #E0E0E0;
        color: #000000;
        padding: 6px;
        border: none;
        border-radius: 3px;
    }

    QFrame {
        background-color: #FFFFFF;
        border: 1px solid #CCCCCC;
    }

    QGroupBox {
        border: 1px solid #CCCCCC;
        border-radius: 5px;
        margin-top: 10px;
        background-color: #F9F9F9;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        padding: 4px 10px;
        color: #333333;
    }

    QHeaderView::section {
        background-color: #F0F0F0;
        color: #333333;
        padding: 6px;
        border: 1px solid #CCCCCC;
    }

    QTableView {
        background-color: #FFFFFF;
        color: #333333;
        border: 1px solid #CCCCCC;
        gridline-color: #CCCCCC;
    }

    QTableView::item:selected {
        background-color: #E0E0E0;
        color: #000000;
    }
    """

def solarized_theme():
    return """
    QWidget {
        background-color: #002b36;
        color: #839496;
        font-family: 'Segoe UI', Tahoma, Geneva, sans-serif;
        font-size: 14px;
        border: none;
    }

    QLabel {
        color: #93a1a1;
        font-size: 14px;
        padding: 6px;
        border: none;
    }

    QPushButton {
        background-color: #268bd2;
        color: #ffffff;
        border: 1px solid #2aa198;
        border-radius: 5px;
        padding: 8px 16px;
        font-size: 14px;
    }

    QPushButton:hover {
        background-color: #259bb2;
    }

    QPushButton:pressed {
        background-color: #268bd2;
    }

    QPushButton:disabled {
        background-color: #073642;
        color: #586e75;
        border: 1px solid #2aa198;
    }

    QLineEdit {
        background-color: #073642;
        color: #839496;
        border: 1px solid #2aa198;
        border-radius: 5px;
        padding: 6px;
    }

    QComboBox {
        background-color: #073642;
        color: #93a1a1;
        border: 1px solid #2aa198;
        border-radius: 5px;
        padding: 6px;
    }

    QComboBox::drop-down {
        border-left: 1px solid #2aa198;
        background-color: #002b36;
    }

    QComboBox QAbstractItemView {
        background-color: #073642;
        color: #93a1a1;
        selection-background-color: #586e75;
        selection-color: #ffffff;
    }

    QListView, QTreeView {
        background-color: #002b36;
        color: #93a1a1;
        border: 1px solid #2aa198;
    }

    QListView::item:selected, QTreeView::item:selected {
        background-color: #586e75;
        color: #ffffff;
    }

    QProgressBar {
        background-color: #073642;
        border: 1px solid #2aa198;
        border-radius: 3px;
        text-align: center;
        color: #93a1a1;
    }

    QProgressBar::chunk {
        background-color: #859900;
    }

    QSlider::groove:horizontal {
        height: 6px;
        background: #2aa198;
        border-radius: 3px;
    }

    QSlider::handle:horizontal {
        background: #b58900;
        width: 12px;
        border-radius: 6px;
    }

    QScrollBar:vertical, QScrollBar:horizontal {
        background: #002b36;
        width: 12px;
        height: 12px;
    }

    QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
        background: #586e75;
        min-height: 20px;
        min-width: 20px;
        border-radius: 6px;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical, QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        background: #073642;
        border: 1px solid #2aa198;
    }

    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical, QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
        image: url(:/icons/arrow.png); /* Customize as needed */
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical, QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
        background: none;
    }

    QMenuBar {
        background-color: #073642;
        color: #93a1a1;
        padding: 4px;
    }

    QMenuBar::item {
        background-color: #073642;
        color: #93a1a1;
        padding: 8px;
    }

    QMenuBar::item:selected {
        background-color: #586e75;
        color: #ffffff;
    }

    QMenu {
        background-color: #002b36;
        color: #93a1a1;
        border: 1px solid #2aa198;
    }

    QMenu::item:selected {
        background-color: #586e75;
        color: #ffffff;
    }

    QTabWidget::pane {
        background-color: #002b36;
        border: 1px solid #2aa198;
    }

    QTabBar::tab {
        background-color: #073642;
        color: #93a1a1;
        padding: 8px 16px;
        border: 1px solid #2aa198;
        border-bottom: none;
    }

    QTabBar::tab:selected {
        background-color: #2aa198;
        color: #002b36;
    }

    QTableView {
        background-color: #002b36;
        color: #93a1a1;
        border: 1px solid #2aa198;
        gridline-color: #2aa198;
    }

    QTableView::item:selected {
        background-color: #586e75;
        color: #ffffff;
    }

    QToolButton {
        background-color: #073642;
        color: #93a1a1;
        border: 1px solid #2aa198;
        padding: 8px;
        border-radius: 3px;
    }

    QToolTip {
        background-color: #586e75;
        color: #ffffff;
        padding: 6px;
        border: none;
        border-radius: 3px;
    }

    QGroupBox {
        background-color: #002b36;
        border: 1px solid #2aa198;
        border-radius: 5px;
        margin-top: 20px;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 6px 12px;
        color: #93a1a1;
    }

    QDockWidget::title {
        background-color: #073642;
        color: #93a1a1;
        padding: 6px;
    }

    QFrame {
        border: 1px solid #2aa198;
        background-color: #002b36;
    }

    QHeaderView::section {
        background-color: #073642;
        color: #93a1a1;
        padding: 6px;
        border: 1px solid #2aa198;
    }

    QCheckBox, QRadioButton {
        color: #93a1a1;
        spacing: 8px;
        padding: 4px;
    }

    QCheckBox::indicator, QRadioButton::indicator {
        width: 18px;
        height: 18px;
        background-color: #073642;
        border: 1px solid #2aa198;
    }

    QCheckBox::indicator:checked, QRadioButton::indicator:checked {
        background-color: #2aa198;
        border: 1px solid #93a1a1;
    }

    QStatusBar {
        background-color: #002b36;
        color: #93a1a1;
        border-top: 1px solid #2aa198;
    }

    QToolBox::tab {
        background-color: #073642;
        border: 1px solid #2aa198;
        padding: 8px;
    }

    QToolBox::tab:selected {
        background-color: #2aa198;
        color: #002b36;
    }
    """


def midnight_purple_theme():
    return """
    QWidget {
        background-color: #2C003E;
        color: #E0B3FF;
        font-family: 'Segoe UI', Tahoma, Geneva, sans-serif;
        font-size: 14px;
        border: none;
    }

    QLabel {
        color: #E0E0E0;
        font-size: 14px;
        padding: 6px;
        border: none;
    }

    QPushButton {
        background-color: #800080;
        color: #FFFFFF;
        border: 1px solid #9400D3;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 14px;
    }

    QPushButton:hover {
        background-color: #4B0082;
    }

    QPushButton:pressed {
        background-color: #2E0854;
    }

    QPushButton:disabled {
        background-color: #4A0072;
        color: #D1B2FF;
        border: 1px solid #6A0DAD;
    }

    QLineEdit {
        background-color: #4A0072;
        color: #E0B3FF;
        border: 1px solid #9400D3;
        border-radius: 5px;
        padding: 6px;
    }

    QComboBox {
        background-color: #4A0072;
        color: #D4A1FF;
        border: 1px solid #9400D3;
        border-radius: 5px;
        padding: 6px;
    }

    QListView, QTreeView {
        background-color: #2C003E;
        color: #D4A1FF;
        border: 1px solid #9400D3;
    }

    QListView::item:selected, QTreeView::item:selected {
        background-color: #800080;
        color: #E0B3FF;
    }

    QProgressBar {
        background-color: #4A0072;
        border: 1px solid #9400D3;
        border-radius: 5px;
        text-align: center;
        color: #D4A1FF;
    }

    QProgressBar::chunk {
        background-color: #8B00FF;
    }

    QSlider::groove:horizontal {
        height: 6px;
        background: #9400D3;
        border-radius: 3px;
    }

    QSlider::handle:horizontal {
        background: #800080;
        width: 12px;
        border-radius: 6px;
    }

    QTabBar::tab {
        background-color: #4A0072;
        color: #D4A1FF;
        padding: 8px;
        border: 1px solid #9400D3;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
    }

    QTabBar::tab:selected {
        background-color: #800080;
        color: #FFFFFF;
    }

    QTreeView {
        background-color: #2C003E;
        color: #FFD700;
        border: 1px solid #5A5A5A;
    }

    QTreeView::item:selected {
        background-color: #2C003E;
        color: white;
    }

    QToolTip {
        background-color: #2C003E;
        color: white;
        border: 1px solid #FFD700;
        padding: 5px;
        border-radius: 5px;
    }

    QMenuBar {
        background-color: #2C003E;
        color: #D3D3D3;
        padding: 8px;
    }

    QMenuBar::item:selected {
        background-color: #2C003E;
        color: white;
        font-weight: bold;
        border-radius: 5px;
    }

    QStatusBar {
        background-color: #2C003E;
        color: #D3D3D3;
        padding: 5px;
        font-size: 14px;
    }

    QHeaderView::section {
        background-color: #2C003E;
        color: #FFD700;
        padding: 5px;
        border: 1px solid #5A5A5A;
        border-radius: 5px;
    }

    QToolButton {
        background-color: #2C003E;
        color: #FFD700;
        border: 1px solid #5A5A5A;
        border-radius: 5px;
        padding: 5px;
    }

    QToolButton:checked {
        background-color: #2C003E;
        color: white;
        font-weight: bold;
    }

    QScrollBar:vertical {
        background: #E0E0E0;
        width: 15px;
    }

    QScrollBar::handle:vertical {
        background: #E0E0E0;
        min-height: 20px;
        border-radius: 7px;
    }
    """


themes = {
    "Minimal Black": minimal_black_theme,
    "Minimal White": minimal_white_theme,
    "Elegant": elegant_theme,
    "Solarized": solarized_theme,
    "Midnight Purple": midnight_purple_theme,
}

def get_theme(theme_name): return themes.get(theme_name, solarized_theme)()

def get_theme_saved():
    from window.init import database, TokenManager
    data = database.GetAccountInformation(TokenManager.get_token(),"Theme") or "Minimal Black"

    return get_theme(data)

def set_theme_saved(name):
    from window.init import database, TokenManager
    database.SetAccountInformation(TokenManager.get_token(),"Theme",name)