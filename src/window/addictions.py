import os
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QTableView, QPushButton
from collections import defaultdict
import pandas as pd
import plotly.graph_objects as go

USER_DOCUMENTS_PATH = os.path.join(os.path.expanduser('~'), 'Downloads')
SAFE_FILE_PATH = os.path.join(USER_DOCUMENTS_PATH, 'main.xlsx')

TableGlobalValue = None

class TableModel(QtGui.QStandardItemModel):
    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)
        self.setHorizontalHeaderLabels(["Date", "Category", "Amount"])

        self.itemChanged.connect(self.autoSaveToFile)

    def autoSaveToFile(self):
        self.saveToFile(SAFE_FILE_PATH)

    def updateData(self, data):
        self.clear()
        self.setHorizontalHeaderLabels(["Date", "Category", "Amount"])
        for row_data in data:
            items = [QtGui.QStandardItem(str(field)) for field in row_data]
            self.appendRow(items)
        self.autoSaveToFile()


    def saveToFile(self, filename):
        df = pd.DataFrame(columns=["Date", "Category", "Amount"])
        for row in range(self.rowCount()):
            data = [self.item(row, col).text() for col in range(self.columnCount())]
            df.loc[row] = data
        df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce').fillna(0).astype(int) 
        df.to_excel(filename, index=False, engine='openpyxl')

    def addRow(self, row_data):
        items = [QtGui.QStandardItem(field) for field in row_data]
        self.appendRow(items)
        self.itemChanged.connect(self.autoSaveToFile)

        self.autoSaveToFile()

    def removeRow(self, index):
        super().removeRow(index)
        self.itemChanged.connect(self.autoSaveToFile)

        self.autoSaveToFile()

    def get_data(self):
        data = []
        for row in range(self.rowCount()):
            row_data = []
            for column in range(self.columnCount()):
                item = self.item(row, column)
                row_data.append(item.text() if item is not None else "")
            data.append(row_data)
        return data

class Addictions(QtWidgets.QWidget):
    def __init__(self, window, show_notification_callback):
        super().__init__(window)
        self.window = window
        self.show_notification_callback = show_notification_callback
        self.initAddictions()

    def initAddictions(self):
        global TableGlobalValue

        print("Addictions has been loaded!")

        self.init_layout = QVBoxLayout(self)

        self.Table = QTableView()
        self.model = TableModel()

        self.Table.setModel(self.model)
        self.Table.horizontalHeader().setStretchLastSection(True)

        self.Table.setStyleSheet("""
            QTableView::corner {
                background-color: transparent;
            }
        """)

        TableGlobalValue = self.model

        self.add_row_button = QPushButton('Add')
        self.remove_row_button = QPushButton('Remove')
        self.save_button = QPushButton('Save')
        self.load_button = QPushButton('Load')
        self.load_graphic = QPushButton('Generate Graphic')

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_row_button)
        button_layout.addWidget(self.remove_row_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.load_graphic)
        self.init_layout.addWidget(self.Table)
        
        self.init_layout.addLayout(button_layout)

        self.add_row_button.clicked.connect(self.addRow)
        self.remove_row_button.clicked.connect(self.removeRow)
        self.save_button.clicked.connect(self.saveToFile)
        self.load_button.clicked.connect(self.loadFromFile)
        self.load_graphic.clicked.connect(self.load_graphic_window)

        self.load_main_file()
        self.styleTable()

    def styleTable(self):
        self.Table.setColumnWidth(0, 120)
        self.Table.setColumnWidth(1, 180)
        self.Table.setColumnWidth(2, 120)

    def load_graphic_window(self):
        try:
            self.data = self.model.get_data()
            
            data = defaultdict(lambda: defaultdict(int))
            for row in self.data:
                date_str, addiction_type, quantity = row
                data[date_str][addiction_type] = quantity

            try:
                all_dates = [pd.to_datetime(date_str, format='%d/%m/%Y') for date_str in data.keys()]
            except ValueError:
                QtWidgets.QMessageBox.warning(
                    self, 'Error', 
                    "To generate a graph, the Date data must follow the format Day/Month/Year"
                )
                return

            first_date = min(all_dates)
            last_date = pd.Timestamp.today().date()
            dates = pd.date_range(start=first_date, end=last_date, freq='D')

            addiction_types = set()
            for date_str in data:
                addiction_types.update(data[date_str].keys())

            data_dict = {'Date': dates}
            for addiction_type in addiction_types:
                data_dict[addiction_type] = [
                    data[date.strftime('%d/%m/%Y')].get(addiction_type, 0) 
                    for date in dates
                ]
            
            df = pd.DataFrame(data_dict)
            df['Date'] = pd.to_datetime(df['Date'])

            fig = go.Figure()
            for column in df.columns[1:]:
                fig.add_trace(go.Scatter(
                    x=df['Date'], y=df[column], 
                    mode='lines+markers', name=column)
                )

            fig.update_layout(
                title='Addiction Trends Over Time',
                xaxis_title='Date',
                yaxis_title='Amount',
                legend_title='Addictions',
                template='seaborn'
            )

            fig.show()

        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Error', str(e))

    def addRow(self):
        row_data, ok = QtWidgets.QInputDialog.getText(self, 'Add', 'New line entry (Date (Day/Month/Year), Category, Quantity):')
        if ok and row_data:
            row_data = row_data.split(',')
            if len(row_data) == 3:
                try:
                    row_data[2] = str(int(row_data[2]))
                except ValueError:
                    QtWidgets.QMessageBox.warning(self, 'Error', 'Amount must be a whole number.')
                    return
                self.model.addRow(row_data)
            else:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Enter the data in the format: Date, Category, Amount.')


    def removeRow(self):
        index, ok = QtWidgets.QInputDialog.getInt(self, 'Remove', 'Line number to be removed', 1, 1, self.model.rowCount())
        if ok:
            self.model.removeRow(index - 1)

    def saveToFile(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Archive', '', 'Excel Files (*.xlsx)')
        if filename:
            self.model.saveToFile(filename)

    def loadFromFile(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Archive', '', 'Excel Files (*.xlsx)')
        if filename:
            try:
                df = pd.read_excel(filename, engine='openpyxl')

                if set(["Date", "Category", "Amount"]).issubset(df.columns):
                    self.data = df[["Date", "Category", "Amount"]].values.tolist()
                    self.data = [[d[0], d[1], int(d[2])] for d in self.data]

                    self.model.updateData(self.data)
                else:
                    QtWidgets.QMessageBox.warning(self, 'Error', "The Excel file must contain the columns 'Date', 'Category', and 'Amount'.")
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, 'Error', f'Error Loading the File: {str(e)}')

    def load_main_file(self):
        try:
            if not os.path.exists(SAFE_FILE_PATH):
                df = pd.DataFrame(columns=["Date", "Category", "Amount"])
                df.to_excel(SAFE_FILE_PATH, index=False, engine='openpyxl')
                print(f'O arquivo {SAFE_FILE_PATH} foi criado porque não existia.')

            df = pd.read_excel(SAFE_FILE_PATH, engine='openpyxl')
            
            if set(["Date", "Category", "Amount"]).issubset(df.columns):
                self.data = df[["Date", "Category", "Amount"]].values.tolist()
                self.data = [[d[0], d[1], int(d[2])] for d in self.data]
                self.model.updateData(self.data)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Error', str(e))
