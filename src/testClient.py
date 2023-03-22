import os
import pyrebase
import uuid

config = {
    "apiKey": "apiKey",
    "authDomain": "test-realtime-8f213.firebaseapp.com",
    "databaseURL": "https://test-realtime-8f213-default-rtdb.europe-west1.firebasedatabase.app",
    "storageBucket": "test-realtime-8f213.appspot.com",
    "serviceAccount": "./config/ServiceAccount.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

choice = ''
os.system('clear')

validFields = ['play', 'pause', 'stop', 'next', 'previous']
while(choice != 'q'):
    
    choice = input('Syntax: <action> <track>\n')

    if(choice == 'q'):
      print("Client Exiting")
      continue

    params = choice.split(' ')
    
    if len(params) == 0:
       print("Invlaid input")
       continue
    
    action = params[0]
    track = params[1] if len(params) > 1 else None

    if(len(params) == 2):
      track = params[1]

    if(action in validFields):
        data = {
           "id": str(uuid.uuid4()),
           "type": action,
           "track": track
        }
        db.child('simulatedDevices').child('action').set(data)
    elif(choice == 'q'):
        continue
    else: print('Invalid field entered')