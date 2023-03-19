import os
import pyrebase
import threading
from firebase_admin import credentials

rootDir = os.path.dirname(os.path.abspath(__file__))
serviceAccountCredentials = os.path.join(rootDir, 'config', 'ServiceAccountKey.json')
cred = credentials.Certificate(serviceAccountCredentials)

config = {
    "apiKey": "apiKey",
    "authDomain": "test-realtime-8f213.firebaseapp.com",
    "databaseURL": "https://test-realtime-8f213-default-rtdb.europe-west1.firebasedatabase.app",
    "storageBucket": "test-realtime-8f213.appspot.com",
    "serviceAccount": "./config/ServiceAccountKey.json"
}

class MusicPlayerClient:
  def __init__(self):
    firebase = pyrebase.initialize_app(config)
    self.db = firebase.database()
    db_listener = threading.Thread(target=self.databaseObserver)
    db_listener.daemon = True
    db_listener.start()

  def databaseObserver(self):
    print("Listening for updates")
    self.db.child("musicPlayer").stream(self.messageHandler)

  def messageHandler(message):
    print(message["event"])
    print(message["path"])
    print(message["data"])

def main():
   player = MusicPlayerClient()