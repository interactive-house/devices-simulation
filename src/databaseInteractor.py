from enum import Enum
import os
from uuid import uuid4

class DatabaseInteractor:
    def __init__(self, database, player):
        self.database = database
        self.player = player
        self.syncSongLibrary()
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

    def syncSongLibrary(self):
        localMusic = self.discoverLocalMusic()
        databaseMusic = self.getDatabaseMusic()
        songList = []
        for localItem in localMusic:
            isMatch = False
            for dbItem in databaseMusic:
                if dbItem["artist"] == localItem["artist"] and dbItem["song"] == localItem["song"]:
                    isMatch = True
                    break
            if isMatch:
                songList.append(dbItem)
            else:
                trackData = {
                    **localItem,
                    "trackId": str(uuid4())
                }
                songList.append(trackData)

        self.database.child("simulatedDevices").child("songList").set(songList)
        self.player.setTrackList(songList)

    def updateDeviceStatus(self):
        self.database.child("simulatedDevices").child("deviceStatus").set("online")

    def discoverLocalMusic(self):
        localMusic: list = []
        for file in os.listdir('music'):
            if file.endswith(".mp3"):
                trackData = file.split(".")[0].split('-')
                artist = trackData[0]
                song = trackData[1]
                data = {
                    "artist": artist,
                    "song": song
                }
                localMusic.append(data)
        print("Local music")
        print(localMusic)
        return localMusic
    
    def getDatabaseMusic(self):
        databaseMusic = self.database.child("simulatedDevices").child("songList").get().val()
        print("Database music")
        print(databaseMusic)
        if type(databaseMusic) is list:
            return databaseMusic
        else:
            return list()


class Action(Enum):
    PLAY = "play"
    PAUSE = "pause"
    STOP = "stop"
    NEXT = "next"
    PREV = "prev"





