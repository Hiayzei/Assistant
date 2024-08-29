from time import strftime, localtime

import psutil, os, requests

class Utils:
    @staticmethod
    def get_random_phrases():
        response = requests.get('https://api.quotable.io/quotes/random')
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                quote_data = data[0]
                content = quote_data.get('content', '')
                author = quote_data.get('author', '')
                return content, author
            else:
                return "", ""
        else:   
            return "", ""

    @staticmethod
    def get_current_time():
        return strftime("%d-%m-%y | %H:%M:%S", localtime())
    
    @staticmethod
    def is_process_running(process_name):
        for proc in psutil.process_iter(['pid', 'name']):
            if process_name.lower() in proc.info['name'].lower():
                return proc
        return None
    
    @staticmethod
    def check_count_files_in_directory(directory,max):
        file_count = 0
        for root, dirs, files in os.walk(directory):
            file_count += len(files)
            if file_count > max:
                return True
        return False
                