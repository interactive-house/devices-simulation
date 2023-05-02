import pyrebase
from src.databaseInteractor import DatabaseInteractor
from src.musicPlayer import MusicPlayer
import traceback
import signal
import sys

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

    player = MusicPlayer()

    interactor = DatabaseInteractor(database, player)

    dataStream = interactor.observe("simulatedDevices") # Runs in another thread

    def signal_handler(signal, frame):
      print("signal handled")
      interactor.updateDeviceStatus("offline")
      dataStream.close()
      sys.exit(1)
      
    signal.signal(signal.SIGINT, signal_handler)

    # This is required so that the keyboard interrupt signal is caught by joining the
    # thread with a timeout
    dataStream.thread.join(5)

  except Exception as e:
     print(e)
     
if __name__ == "__main__":
    main()
