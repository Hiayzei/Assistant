from PyQt6 import QtCore, QtWidgets, QtGui
from window.init import database, TokenManager
import uuid

class Writing(QtWidgets.QWidget):
    def __init__(self, window, show_notification_callback):
        super().__init__(window)

        self.window = window
        self.show_notification_callback = show_notification_callback

        self.currentpage = self
        self.data = []

        self.initWriting()
        self.load_page()

    def load_page(self, Page=None):
        global TokenManager

        
        for i in reversed(range(self.currentpage.layout_texts.count())): 
            widget = self.currentpage.layout_texts.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        if not Page:
            if self.data == []:
                collectiondata = database.GetAnnotations(TokenManager.get_token())
                print(f"Collection data: {collectiondata}")
                self.data = [doc['info'] for doc in collectiondata]

                try:
                    for item in self.data:
                        if item['parent_folder'] == "None":
                            if item['class'] == "Folder":
                                self.create_folder(item,"Loading")
                            elif item['class'] == "Text":
                                self.create_text(item,"Loading")
                except:
                    print("Data Corrupted")
        else:
            try:
                for item in self.data:
                    if item['parent_folder'] == Page:
                        if item['class'] == "Folder":
                            self.create_folder(item,"Loading")
                        elif item['class'] == "Text":
                            self.create_text(item,"Loading")
            except:
                print("Data Corrupted")

    def initWriting(self):
        print("Writing has been loaded!")

        self.init_layout = QtWidgets.QVBoxLayout(self)
        self.WritingTemplate = QtWidgets.QFrame()
        self.layout_texts = QtWidgets.QVBoxLayout(self.WritingTemplate)
        self.layout_texts.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidget(self.WritingTemplate)
        self.scroll_area.setWidgetResizable(True)

        self.createfolderbutton = QtWidgets.QPushButton("Create Folder")
        self.createfolderbutton.clicked.connect(self.create_folder)

        self.init_layout.addWidget(self.scroll_area)
        self.init_layout.addWidget(self.createfolderbutton)

    def create_text(self, info=None,State=None):
        if info and not any(item["_id"] == info['_id'] for item in self.data):
            self.data.append(info)
        
        if State != "Loading":
            database.annotations_collection.insert_one({
                "token": TokenManager.get_token(),
                "info": info
            })

        text_button = QtWidgets.QPushButton(info['name'])
        text_button.clicked.connect(lambda: self.open_text_page(info['_id']))


        h_layout = QtWidgets.QHBoxLayout()

        image_button = QtWidgets.QPushButton()
        image_button.setProperty('text_id', info['_id'])
        image_button.setIcon(QtGui.QIcon('assets/Images/deletebutton.png'))
        image_button.setIconSize(QtCore.QSize(24, 24))
        image_button.clicked.connect(lambda: self.DeleteById(info['_id']))

        h_layout.addWidget(text_button,2)
        h_layout.addWidget(image_button)

        

        container_widget = QtWidgets.QWidget()
        container_widget.setLayout(h_layout)

        self.currentpage.layout_texts.addWidget(container_widget)

    def DeleteById(self, text_id):
        def remove_item_recursively(current_id):
            items_to_remove = [item for item in self.data if item['parent_folder'] == current_id]
            for item in items_to_remove:
                remove_item_recursively(item['_id'])
            
            self.data = [item for item in self.data if item['_id'] != current_id]

            for i in reversed(range(self.currentpage.layout_texts.count())):
                widget = self.currentpage.layout_texts.itemAt(i).widget()
                if widget:
                    h_layout = widget.layout()
                    if h_layout:
                        image_button = h_layout.itemAt(1).widget()
                        if image_button.property('text_id') == current_id:
                            self.currentpage.layout_texts.removeWidget(widget)
                            widget.deleteLater()
                            self.currentpage.layout_texts.update()
                            break

            database.annotations_collection.delete_many({
                "token": TokenManager.get_token(),
                "$or": [
                    {"info._id": current_id},
                    {"info.parent_folder": current_id}
                ]
            })

        remove_item_recursively(text_id)


    def create_folder(self, info=None,State=None):
        if not info:
            info = {
                "name": "New Folder",
                "parent_folder": "None",
                "_id": str(uuid.uuid4()),
                "class": "Folder"
            }


        if State == "Loading":
            if not any(item["_id"] == info['_id'] for item in self.data):
                self.data.append(info)
        else:
            database.annotations_collection.insert_one({
                "token": TokenManager.get_token(),
                "info": info
            })        


        folder_button = QtWidgets.QPushButton(info['name'])

        h_layout = QtWidgets.QHBoxLayout()

        image_button = QtWidgets.QPushButton()
        image_button.setProperty('text_id', info['_id'])
        image_button.setIcon(QtGui.QIcon('assets/Images/deletebutton.png'))
        image_button.setIconSize(QtCore.QSize(24, 24))
        image_button.clicked.connect(lambda: self.DeleteById(info['_id']))

        h_layout.addWidget(folder_button,2)
        h_layout.addWidget(image_button)

        container_widget = QtWidgets.QWidget()
        container_widget.setLayout(h_layout)

        self.currentpage.layout_texts.addWidget(container_widget)

        def onclick():
            folder_page = QtWidgets.QWidget()

            self.currentpage = folder_page
            self.currentpage.layout = QtWidgets.QVBoxLayout(folder_page)
            self.currentpage.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

            name_edit = QtWidgets.QLineEdit()
            name_edit.setText(info['name'])

            def update_name():
                new_name = name_edit.text()
                if new_name:
                    info['name'] = new_name
                    folder_button.setText(info['name'])
                    self.update_data_item(info)

                    print(info['name'])

            name_edit.textEdited.connect(update_name)
            self.currentpage.layout.addWidget(name_edit)

            self.currentpage.writing_template = QtWidgets.QFrame()

            self.currentpage.layout_texts = QtWidgets.QVBoxLayout(self.currentpage.writing_template)
            self.currentpage.layout_texts.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

            scroll_area = QtWidgets.QScrollArea()
            scroll_area.setWidget(self.currentpage.writing_template)
            scroll_area.setWidgetResizable(True)

            create_folder_button = QtWidgets.QPushButton("Create Folder")
            create_folder_button.clicked.connect(
                lambda: self.create_folder({
                    "name": "New Folder",
                    "parent_folder": info['_id'],
                    "_id": str(uuid.uuid4()),
                    "class": "Folder"
                })
            )

            create_text_button = QtWidgets.QPushButton("Create Text")
            create_text_button.clicked.connect(
                lambda: self.create_text({
                    "name": "New Text",
                    "parent_folder": info['_id'],
                    "_id": str(uuid.uuid4()),
                    "class": "Text",
                    "content": ""
                })
            )

            back_button = QtWidgets.QPushButton("Back")
            back_button.clicked.connect(self.returnpage)

            self.currentpage.layout.addWidget(scroll_area)
            self.currentpage.layout.addWidget(create_folder_button)
            self.currentpage.layout.addWidget(create_text_button)
            self.currentpage.layout.addWidget(back_button)

            self.window.content_stack.addWidget(folder_page)
            self.window.content_stack.setCurrentWidget(folder_page)

            self.load_page(info['_id'])

        folder_button.clicked.connect(onclick)

    def update_data_item(self, updated_item):
        for i, item in enumerate(self.data):
            if item['_id'] == updated_item['_id']:
                self.data[i] = updated_item

                filter_query = {
                    "token": TokenManager.get_token(),
                    "info._id": updated_item['_id']
                }

                update_query = {
                    "$set": {
                        "info": updated_item
                    }
                }

                try:
                    result = database.annotations_collection.update_one(
                        filter_query,
                        update_query
                    )

                    if result.modified_count == 0:
                        print("No document was updated")
                    else:
                        print("Document updated successfully")
                except Exception as e:
                    print(f"An error occurred: {e}")
    
    def open_text_page(self, text_id):
        text_info = next((item for item in self.data if item["_id"] == text_id), None)

        if text_info is None:
            print("Text not found!")
            return
        
        text_page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(text_page)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        name_edit = QtWidgets.QLineEdit()
        name_edit.setText(text_info['name'] if text_info else "New Text")

        def update_name():
            new_name = name_edit.text()
            if new_name:
                text_info['name'] = new_name
                self.update_data_item(text_info)

        name_edit.textEdited.connect(update_name)

        layout.addWidget(name_edit)

        text_edit = QtWidgets.QTextEdit()

        text_edit.setStyleSheet("""
            QTextEdit {
                border: 2px solid #2aa198;
                border-radius: 8px;
            }
        """)
        text_edit.setText(text_info["content"])

        text_edit.textChanged.connect(lambda: self.save_text(text_id, text_edit.toPlainText()))

        back_button = QtWidgets.QPushButton("Back")
        back_button.clicked.connect(self.returnpage)

        layout.addWidget(text_edit)
        layout.addWidget(back_button)

        self.window.content_stack.addWidget(text_page)
        self.window.content_stack.setCurrentWidget(text_page)
        
    def save_text(self, text_id, content):

        for item in self.data:
            if item["_id"] == text_id:
                item["content"] = content

                filter_query = {
                    "token": TokenManager.get_token(),
                    "info._id": item['_id']
                }

                update_query = {
                    "$set": {
                        "info": item
                    }
                }

                try:
                    result = database.annotations_collection.update_one(
                        filter_query,
                        update_query
                    )

                    if result.modified_count == 0:
                        print("No document was updated")
                    else:
                        print("Document updated successfully")
                except Exception as e:
                    print(f"An error occurred: {e}")
                break

    def returnpage(self):
        self.window.content_stack.addWidget(self)
        self.window.content_stack.setCurrentWidget(self)

        self.currentpage = self