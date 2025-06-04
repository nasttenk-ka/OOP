from .User import User
from .Document import Document
import json , os
import dropbox

TOKEN = "sl.u.AFzYBcVFMgAtuHT7uZxyn8d2YbcmxKIjw1ijCGcV0Urp3Lu4K2ZuQvJeOkVBOU5Txn7Uv4t49CyshCT4XyeItOrIq7GODE5asu9hZUwFDLlt4fH2Yw6sgzIuuRh1ELca9L2KFjPY5B3jD3QK2Ufdw1vzs6l9bLZcDOFuYRNIPtsA3Vqj17KlvBhnBHGJIcbEcvyd07H9_4nmK8W-uBDThyVRjfUfjK0ExgXe6AN-ED0qhkli9lLEOirXw6mszPPyAfHhdisEnhCKvEF-pJiBf3BIX27_PYLS2GYUoz6yuOIB4vwUqDLoIgfZ6G854hcqtM0C4D_yhQDfri7u3SRDJTVtclxnGPOkHa56hukbZM48mqpcOCzOZZ4YdI0kggD1h7aa__ZKrUcR8ZGTkethXssYrScm4isEPw0R7AumMZlYL53fJBQBMd_FRN6WM-jKqIc1NAZl2fHCIYMQ-tyu4yHpLeJmXqnNSoW9FiXwhjgiTQ_rxkDOat50Pm2tzPu0d7hjUC9AMJFjcA0qpcKREzzO2pngNFQkzEEsytDDFJg3yOUySmkZSI1-2tZWvtLwqH2jEwkx5dcK2o-7NFAKe4EcBI7HW2xvVUBRTf1uD4F0n-kJdxE3XmN3WBWoQ4Tz_Xv8is8leCjYFwwzWlu3nGWnIMWUOi66_-3sbi9zuvsQSOJakv0aDhu2EZs4cRPZsyJE9hjq_OOFEJpKQw2HlT68XD3zmFy5UO2HGyFyBNG9Ofp-gwMN0cn-uYXmAbDwstpk0UYeS64P2F8mouUr3_aLrce3xOxZxE_DgpZ1tA2TUys5On54IBfT59lLPNLyZ5t7jBs5TJy16C6C89-UMwBhhU8nLyIERC9Z6IsdBpcvI7xJj5iemTNAtfd_LxquPwfdXMBx-iMGFx7ZqRqpxOdl6G-MlGjGVfLxptWS_tmm20r-d9ISKFVnEf7fQ20UXyNaCZhKlqkHZc9_ZsyXBlKwsjlQlIsfEkjPmv1JN1sSAOnVjXTE3__JtGQEUN0dlVr1RdrifS7-cH8YP9vf3CbMi3NiStE20YHsy1Kp0-88okdyPY0AVL2ZSd3r3qeZQlnFt4w1cpyQtUpGXpPcpJolveWU34Erv6w1K_uuOACGPfHnoRBuOaOt1BKSR0Ik8sKI_NYAvGokmmch_G3Vr5ooUdffs6hzjFNjIyRkXFob8PZgQV3fpyj8zcJ40qKW_qMkMIl2qAOuNo70017U5VGz6P1uJydKSa10B2wUGEwiE7Xq1b_6b0krt8AQNBTtlDCaMRFTcmkkrss_hqIRZtsLlUXRG4-CyPe4ZR6j2FGSPF6gQUNYod3kPeE5UrbprRnWgKHzCQKOh-VeZABqeKaWfyOT7wjwuaUCv-TNgNTAXTfOunAY95J7QGHpgLXP96WCgQFrDzRHsT8LLuRxbazKTpZY8T3ieBjZ_A2F4Y73kb0rdAEIz4BPciBUw2hdaWh_lDJvuHv18SDsrVjcUK4xaH4CXeck1z9EyMvXjQQf7A"

def file_exists(dbx, file_path):
    try:
        dbx.files_get_metadata(file_path)
        return True
    except dropbox.exceptions.ApiError as err:
        if err.error.is_path() and err.error.get_path().is_not_found():
            return False
        raise

class TextEditor:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._users = []
        self._authorized_user = None
        self._documents = {}
        self._current_document = None
        self._text = None

    @property
    def documents(self):
        return self._documents

    @property
    def current_document(self):
        return self._current_document
    
    @current_document.setter
    def current_document(self,value):
        self._current_document = value

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self,value):
        self._text = value
    
    @property
    def users(self):
        return self._users
    
    @property
    def authorized_user(self):
        return self._authorized_user

    @authorized_user.setter
    def authorized_user(self,value):
        self._authorized_user = value

    def sign_in(self, login, password):
        if(any(user._login == login for user in self.users)):
            raise Exception("account with that login is already existing")
        else:
            self.users.append(User(login, password))
            self._authorized_user = self.users[-1]
        
        

    def log_in(self, login, password):
        if (self.authorized_user != None):
            raise Exception("user already logined")
        for user in self.users:
            if(user._login == login and user._password == password):
                self.authorized_user = user
                break
        if (self.authorized_user == None):
            raise Exception("no user with this login info")

    def log_out(self):
        self.authorized_user = None
        self.close_document()      

    def close_document(self):
        self._current_document = None
        self._text = None

    def check_extension(self,s):
        return s[-4:] == ".txt" or s[-4:] == ".xml" or s[-5:] == ".json" or s[-3:] == ".md"
    
    def redactor_or_visitor(self,s):
        if (self.authorized_user._login == self.documents[s]._author._login or 
        any(user._login == self.authorized_user._login for user in self.documents[s].redactors)):
            return True
        #elif(any(user._login == self.authorized_user._login for user in self.documents[s].visitors)):
        else:
            return False
        #else: raise Exception("Бля гдето юзера проебали")

    def open_document(self, s):
        if (self.authorized_user != None):
            if (os.path.exists(f"documents/{s}")):
                self.current_document = self.documents[s]
                if (self.check_extension(s)):
                    with open("documents/" + s, 'r', encoding='utf-8') as file:
                        self.text = file.read()
                else:
                    raise Exception("this extention not supported")
            else: 
                #добавить в документс документ
                if (self.check_extension(s)):
                    self.documents[s] = Document(s, self.authorized_user)
                    self.current_document = self.documents[s]
                    with open("documents/" + s, 'r', encoding='utf-8') as file:
                        self.text = file.read()
                else:
                    raise Exception("this extention not supported")
        else: raise Exception("no authorization")

    def save_document(self):
        if (self.current_document != None):
            with open(f"documents/{self.current_document._name}", 'w', encoding='utf-8') as f:
                f.write(self.text)
            if self._authorized_user != self._current_document._author:
                message = f"document '{self._current_document._name}' was changed by {self._authorized_user._login}"
                self._current_document._author.notify(message)
        else: raise Exception("document not opened")

    def save_document_cloud(self):
        if (self.current_document != None):
            dbx = dropbox.Dropbox(TOKEN)
            with open(f"documents/{self.current_document._name}", "rb") as f:
                dbx.files_upload(f.read(), f"/{self.current_document._name}", mode=dropbox.files.WriteMode.overwrite)
            
        else: raise Exception("document not opened")

    def open_document_cloud(self,s):
        if (self.current_document != None):
            dbx = dropbox.Dropbox(TOKEN)

            if file_exists(dbx, f"/{s}"):
                metadata, res = dbx.files_download(f"/{s}")
                self.text = res.content.decode("utf-8")
                self.current_document = self.documents[s]

            else:
                self.documents[s] = Document(s, self.authorized_user)
                self.current_document = self.documents[s]
                dbx.files_upload(b"", f"/{s}")
                metadata, res = dbx.files_download(f"/{s}")
                self.text = res.content.decode("utf-8")
                
            
        else: raise Exception("document not opened")

    def delete_document(self):
        file_path = f"documents/{self.current_document._name}"
        os.remove(file_path)
        del self.documents[self.current_document._name]
        self.text = ""
        self.current_document = None



    #сделать проверку на существования имени 
    #присваивать авторизованного юзера в автора при создании
    #возвращать true / false соответственно может редачить или нет



#editor = TextEditor()
#editor.sign_in("ya","ogo")
#editor.open_document("aboba.txt")
#print(editor.text)

#editor.open_document("aboba2.txt")
#print(editor.text)