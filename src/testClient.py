import os
import pyrebase
import uuid

config = {
    "apiKey": "apiKey",
    "authDomain": "smarthome-3bb7b.firebaseapp.com",
    "databaseURL":  "https://smarthome-3bb7b-default-rtdb.firebaseio.com/",
    "projectId": "smarthome-3bb7b",
    "storageBucket": "smarthome-3bb7b.appspot.com",
    "serviceAccount": "./config/ServiceAccount.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

music = db.child("simulatedDevices").child("songList").get().val()
trackIds = []
for track in music:
    trackIds.append(track["trackId"])

choice = ''
os.system('clear')

validFields = ['play', 'pause', 'stop', 'next', 'prev']
while(choice != 'q'):

    choice = input('Syntax: <action> or <action>-<trackId>\n')

    if(choice == 'q'):
      print("Client Exiting")
      continue

    params = choice.split('-')
    totalParams = len(params)
    
    if totalParams not in (1, 2):
       print("Invlaid input")
       continue
    
    action = params[0]
    trackId = None

    if totalParams == 2:
        index = int(params[1])
        if index < len(trackIds):
            trackId = trackIds[index]
        else:
            print("Not a valid song index")
            continue

    if(action in validFields):
        data = {
           "id": str(uuid.uuid4()),
           "type": action,
           "trackId": trackId
        }
        db.child('simulatedDevices').child('action').set(data)
    elif(choice == 'q'):
        continue
    else: print('Invalid field entered')