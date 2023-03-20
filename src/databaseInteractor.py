# Takes a firebase database instance and music player to handle interactions
# when updates occur

class DatabaseInteractor:
    def __init__(self, database, player):
        self.database = database
        self.player = player

    # Starts observing a collection in the database for changes
    def observe(self, collection):
      print(f"Observing {collection} collection for changes")
      self.database.child(collection).stream(self.onChange)

    # onChange will handle responses from the stream when data is updated
    # in the database. This will then call the MusicPlayer instance methods
    # depending on what data has changed.
    def onChange(self, message):
        
        # Check if the event type is patch, which is an update
        if(message["event"] == "patch"):
            
            # Get the updated field and value
            field = list(message["data"].keys())[0]
            value = message["data"][field]

            # Handle the different field updates
            match field:
                case "state":
                    self.handleStateChange(value)
                    
                case "currentTrack":
                    self.handleTrackChange(value)

    # Method to call the various state change methods in the music player
    def handleStateChange(self, value):
        if(value == "playing"):
            self.player.play()
        if(value == "stopped"):
            self.player.stop()
        if(value == "paused"):
            self.player.pause()

    # Method to call the track change method in the music player
    def handleTrackChange(self, track):
        self.player.changeTrack(track)



