import pyrebase
from src.databaseInteractor import DatabaseInteractor
from src.musicPlayer import MusicPlayer
import traceback
import signal
import time
from src.handler import Handler
from watchdog.observers import Observer


def main():

    # Configure real time database.
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

        dataStream = interactor.observe(
            "simulatedDevices")  # Runs in another thread

        # Handle device status to offline by receiving a signal and frame, close datastream, interactor and music player.
        def signal_handler(signal, frame):
            print("Closing music player")
            interactor.updateDeviceStatus("offline")
            dataStream.close()
            interactor.close()
            musicPlayer.close()

        fileObserver = Observer()

        fileChangeHandler = Handler(interactor)

        fileObserver.schedule(fileChangeHandler, "./music", False)

        fileObserver.start()

        signal.signal(signal.SIGINT, signal_handler)

        while (dataStream.thread.is_alive()):
            time.sleep(1)

    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()
