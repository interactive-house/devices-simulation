import pyrebase
import os
from databaseInteractor import DatabaseInteractor
from musicPlayer import MusicPlayer

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
    
    # Create a dict with the song name without the file extension
    # as key, and full file path as value.
    tracklist: dict = {}
    for file in os.listdir('music'):
      if file.endswith(".mp3"):
          niceName = file.split(".")[0]
          tracklist[niceName] = file

    player = MusicPlayer(tracklist)

    interactor = DatabaseInteractor(database, player, tracklist)

    interactor.observe("simulatedDevices") # Runs in another thread

  except Exception as error:
     print(error)
     
if __name__ == "__main__":
    main()
