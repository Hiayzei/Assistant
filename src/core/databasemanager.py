from pymongo import MongoClient
from pymongo.server_api import ServerApi
import logging

uri = None ## or insert your uri mongodb here

class Database:
    def __init__(self):
        try:
            self.client = MongoClient(uri, server_api=ServerApi('1'))
            self.database = self.client["AssistantData"]
            self.users_collection = self.database["Users"]
            self.annotations_collection = self.database["Annotations"]

            print("MongoDB connection successful!")
        except Exception as e:
            logging.error(f"An error occurred while connecting to MongoDB: {e}")
            self.client = None

    def create_user(self, token, user_data):
        if self.client:
            try:
                self.users_collection.insert_one({
                "_id": token,
                "data": {
                    "infos": user_data,
                    "settings": {
                        "ClientId": "",
                        "RichPresenceAutoStart": False,
                        "RPCMode": "",
                        "PlaylistsPath": "assets/Playlists",
                        "LibraryPath": "assets/Library",
                        "Theme": "Solarized"
                    }
                }
            })
            except Exception as e:
                username = user_data.get('infos', {}).get('username', 'Unknown')
                logging.error(f"An error occurred while creating user '{username}': {e}")
            
    def account_exists(self,token):
        if self.client:
            try:
                return self.users_collection.count_documents({"_id": token}) > 0
            except Exception as e:
                logging.error(f"An error occurred while checking if account exists: {e}")
                return False
            
    def account_exists_with_info(self, info):
        if self.client:
            try:
                return self.users_collection.find_one({"data.infos.sub": info["sub"]})
            except Exception as e:
                logging.error(f"An error occurred while checking if account exists: {e}")
                return None
        else:
            logging.error("Database client is not initialized.")
            return None

    def GetAnnotations(self, Token):
        if self.client:
            try:
                annotations = self.annotations_collection.find({"token": Token})
                
                return list(annotations)
            except Exception as e:
                logging.error(f"An error occurred: {e}")

    def GetAccountInformation(self, Token, Information):
        if self.client:
            try:
                query = {"_id": Token}
                account_info = self.users_collection.find_one(query)
                
                if account_info:
                    settings = account_info.get("data", {}).get("settings", {})
                    return settings.get(Information)
                else:
                    return None
            except Exception as e:
                return None


    def SetAccountInformation(self, Token, Information, NewValue):
        if self.client:
            try:
                query = {"_id": Token}
                
                update = {"$set": {f"data.settings.{Information}": NewValue}}
                
                result = self.users_collection.update_one(query, update)
                
                if result.matched_count > 0:
                    return True
                else:
                    return False
            except Exception as e:
                print(str(e))
                return False


