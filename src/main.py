import pyrebase
from databaseInteractor import DatabaseInteractor
from musicPlayer import MusicPlayer

def main():
  # try:
    config = {
        "apiKey": "apiKey",
        "authDomain": "test-realtime-8f213.firebaseapp.com",
        "databaseURL": "https://test-realtime-8f213-default-rtdb.europe-west1.firebasedatabase.app",
        "storageBucket": "test-realtime-8f213.appspot.com",
        "serviceAccount": "./config/ServiceAccount.json"
    }

    firebase = pyrebase.initialize_app(config)

    database = firebase.database()

    player = MusicPlayer()

    interactor = DatabaseInteractor(database, player)

    interactor.observe("simulatedDevices") # Runs in another thread

  # except Exception as error:
  #    print(error)
     
if __name__ == "__main__":
    main()
