from enum import Enum

class DatabaseInteractor:
    def __init__(self, database, player, tracklist: list):
        self.database = database
        self.player = player
        self.tracklist = tracklist
        self.setTracklist()
        self.updateDeviceStatus()

    # Starts observing a collection in the database for changes
    def observe(self, collection: str):
      print(f"Observing {collection} collection for changes")
      self.database.child(collection).stream(self.onChange)

    # onChange will handle responses from the stream when data is updated
    # in the database. This will then call the MusicPlayer instance methods
    # depending on what data has changed.
    def onChange(self, message):
        print(message)
        # Check if the event type is patch, which is an update
        if(message["path"] == "/action"):
            
            # Get the updated field and value
            data = message["data"]
            dataKeys = list(data.keys())
            type = data["type"] if 'type' in dataKeys else None
            track = data['track'] if 'track' in dataKeys else None

            match type:
                case 'play':
                    self.player.play(track)
                case 'pause':
                    self.player.pause()
                case 'stop':
                    self.player.stop()
                case 'next':
                    self.player.next()
                case 'previous':
                    self.player.previous()

    def setTracklist(self):
        self.database.child("simulatedDevices").child("songList").set(list(self.tracklist.keys()))

    def updateDeviceStatus(self):
        self.database.child("simulatedDevices").child("deviceStatus").set("online")

class Action(Enum):
    PLAY = "play"
    PAUSE = "pause"
    STOP = "stop"
    NEXT = "next"
    PREVIOUS = "previous"





