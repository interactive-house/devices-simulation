import pyrebase
from src.databaseInteractor import DatabaseInteractor
from src.musicPlayer import MusicPlayer
import traceback
import signal
import time

def main():

  try:
    config = {
        "apiKey": "apiKey",
        "authDomain": "smarthome-3bb7b.firebaseapp.com",
        "databaseURL":  "https://smarthome-3bb7b-default-rtdb.firebaseio.com/",
        "projectId": "smarthome-3bb7b",
        "storageBucket": "smarthome-3bb7b.appspot.com",
        "serviceAccount": "./config/ServiceAccount.json"
    }

    firebase = pyrebase.initialize_app(config)

    database = firebase.database()
       
    musicPlayer = MusicPlayer()

    interactor = DatabaseInteractor(database, musicPlayer)

    dataStream = interactor.observe("simulatedDevices") # Runs in another thread

    def signal_handler(signal, frame):
      print("Closing music player")
      interactor.updateDeviceStatus("offline")
      dataStream.close()
      interactor.close()
      musicPlayer.close()
      
    signal.signal(signal.SIGINT, signal_handler)

    while(dataStream.thread.is_alive()):
       time.sleep(0.1)

  except KeyboardInterrupt as e:
     print("key")
     
if __name__ == "__main__":
    main()
