import pyrebase
import os
from databaseInteractor import DatabaseInteractor
from musicPlayer import MusicPlayer
from uuid import uuid4

def createTrackList():
  tracklist: list = []
  for file in os.listdir('music'):
    if file.endswith(".mp3"):
      trackData = file.split(".")[0].split('-')
      trackId = str(uuid4())
      artist = trackData[0]
      song = trackData[1]
      data = {
        "trackId": trackId,
        "artist": artist,
        "song": song
      }
      tracklist.append(data)
  return tracklist  

def main():
  try:
    config = {
        "apiKey": "apiKey",
        "authDomain": "test-realtime-8f213.firebaseapp.com",
        "databaseURL": "https://test-realtime-8f213-default-rtdb.europe-west1.firebasedatabase.app",
        "storageBucket": "test-realtime-8f213.appspot.com",
        "serviceAccount": "./config/ServiceAccount.json"
    }

    firebase = pyrebase.initialize_app(config)

    database = firebase.database()

    tracklist = createTrackList()

    player = MusicPlayer(tracklist)

    interactor = DatabaseInteractor(database, player, tracklist)

    interactor.observe("simulatedDevices") # Runs in another thread

  except Exception as error:
     print(error)
     
if __name__ == "__main__":
    main()
