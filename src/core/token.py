from cryptography.fernet import Fernet
import json
import os

class Token:
    def __init__(self, key_file='secret.key', data_file='data.json'):
        self.key_file = os.path.join(os.path.expanduser("~"), key_file)
        self.data_file = os.path.join(os.path.expanduser("~"), data_file)
        self.key = self.load_or_generate_key()

    def load_or_generate_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as key_file:
                key_file.write(key)
            return key

    def encrypt_token(self, token):
        fernet = Fernet(self.key)
        encrypted_token = fernet.encrypt(token.encode())
        
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
        else:
            data = {}

        data['Token'] = encrypted_token.decode()

        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)
        
        print("Token encrypted and saved successfully.")

    def decrypt_token(self):
        if not os.path.exists(self.data_file):
            return ""
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                encrypted_token = data.get('Token')
                if encrypted_token is None:
                    raise ValueError("Token not found in data file.")
                
                fernet = Fernet(self.key)
                return fernet.decrypt(encrypted_token.encode()).decode()
        except (json.JSONDecodeError, KeyError, ValueError, Exception) as e:
            print(f"Error: {e}")
        return ""

    def store_token(self, token):
        self.encrypt_token(token)

    def get_token(self):
        return self.decrypt_token()

    def delete_files(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)

            data['Token'] = ""

            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=4)