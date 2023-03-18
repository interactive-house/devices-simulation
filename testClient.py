import pyrebase
from firebase_admin import credentials
import os
import json


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

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def streamHandler(message):
    print(message["event"])
    print(message["path"])
    print(message["data"])

def main():
    choice = ''
    os.system('clear')

    validFields = ['state', 'currentTrack']
    while(choice != 'q'):
        
        choice = input('Update a field with syntax: <field> <data>\n')

        if(choice == 'q'):
          print("Client Exiting")
          continue

        params = choice.split(' ')
        
        if(len(params) != 2):
           print('Invalid input')
           continue

        
        field = params[0]
        data = params[1]

        if(field in validFields):
            db.child('musicPlayer').update({f"{field}": f"{data}"})
        elif(choice == 'q'):
            continue
        else: print('Invalid field entered')

if __name__ == "__main__":
    main()