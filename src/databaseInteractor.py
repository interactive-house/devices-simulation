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
            dataKeys = data.keys()
            type = data["type"] if "type" in dataKeys else None
            trackId = data["trackId"] if "trackId" in dataKeys else None

            match type:
                case Action.PLAY.value:
                    self.player.play(trackId)
                case Action.PAUSE.value:
                    self.player.pause()
                case Action.STOP.value:
                    self.player.stop()
                case Action.NEXT.value:
                    self.player.next()
                case Action.PREV.value:
                    self.player.prev()

    def setTracklist(self):
        self.database.child("simulatedDevices").child("songList").set(self.tracklist)

    def updateDeviceStatus(self):
        self.database.child("simulatedDevices").child("deviceStatus").set("online")

class Action(Enum):
    PLAY = "play"
    PAUSE = "pause"
    STOP = "stop"
    NEXT = "next"
    PREV = "prev"





