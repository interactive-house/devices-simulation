import pyrebase
from databaseInteractor import DatabaseInteractor
from musicPlayer import MusicPlayer


def main():
  # try:
    config = {
        "apiKey": "AIzaSyCOZcBxs3RkxuxDrf5vT2HwexFh3ZCw94c",
        "authDomain": "smarthome-3bb7b.firebaseapp.com",
        "projectId": "smarthome-3bb7b",
        "storageBucket": "smarthome-3bb7b.appspot.com",
        "serviceAccount": "./config/ServiceAccount.json"
    }

    firebase = pyrebase.initialize_app(config)

    database = firebase.database()

    player = MusicPlayer()

    interactor = DatabaseInteractor(database, player)

    interactor.observe("simulatedDevices")  # Runs in another thread

  # except Exception as error:
  #    print(error)


if __name__ == "__main__":
    main()
