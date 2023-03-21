import pyrebase
from musicPlayer import MusicPlayer
from databaseInteractor import DatabaseInteractor

def main():
    
  config = {
      "apiKey": "apiKey",
      "authDomain": "test-realtime-8f213.firebaseapp.com",
      "databaseURL": "https://test-realtime-8f213-default-rtdb.europe-west1.firebasedatabase.app",
      "storageBucket": "test-realtime-8f213.appspot.com",
      "serviceAccount": "./config/ServiceAccount.json"
  }

  firebase = pyrebase.initialize_app(config)

  database = firebase.database()
    
  musicPlayer = MusicPlayer()

  interactor = DatabaseInteractor(database, musicPlayer)

  interactor.observe("musicPlayer") # Runs in another thread

if __name__ == "__main__":
    main()


