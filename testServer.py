import pyrebase
import firebase_admin
from firebase_admin import credentials
from pathlib import Path
import os

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

def streamHandler(message):
    print(message["event"])
    print(message["path"])
    print(message["data"])

firebase = pyrebase.initialize_app(config)
db = firebase.database()

db_listener = db.child("musicPlayer").stream(streamHandler)



