import pyrebase
from src.databaseInteractor import DatabaseInteractor
from src.musicPlayer import MusicPlayer

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

    interactor.observe("simulatedDevices") # Runs in another thread

  except Exception as error:
     print(error)
     
if __name__ == "__main__":
    main()
