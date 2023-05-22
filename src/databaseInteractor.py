from enum import Enum
import os
import time
from uuid import uuid4
from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3
from .musicPlayer import MusicPlayer
import vlc

class DatabaseInteractor:
    def __init__(self, database, player):
        self.database = database
        self.player: MusicPlayer = player
        self.tracklist = []
        self.syncSongLibrary()
        self.updateDeviceStatus("online")

    # Starts observing a collection in the database for changes
    def observe(self, collection: str):
        print(f"Observing {collection} collection for changes")
        return self.database.child(collection).stream(self.onChange)
        


    # onChange will handle responses from the stream when data is updated
    # in the database. This will then call the MusicPlayer instance methods
    # depending on what data has changed.
    def onChange(self, message):
        
        # Check if the event type is patch, which is an update
        if(message["path"] == "/action"):
            print(message)
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

            time.sleep(0.1)
            self.updatePlayerState()

            
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
        self.tracklist = songList

    def updateDeviceStatus(self, status):
        self.database.child("simulatedDevices").child("deviceStatus").set(status)
        self.database.child("simulatedDevices").child("playerState").set({
                "state": "Stopped",
                "currentTrack": {"artist": "", "track": ""}
            })

    def updatePlayerState(self):
        states = vlc.State._enum_names_
        currentState = self.player.listPlayer.get_state()
        playerState = states[currentState.value]
        newTrack: vlc.Media = self.player.mediaPlayer.get_media()

        if newTrack:
            artist = newTrack.get_meta(vlc.Meta.Artist)
            song = newTrack.get_meta(vlc.Meta.Title)
            trackId = ""
            for track in self.tracklist:
                if track["artist"][0] == artist and track["song"][0] == song:
                    trackId = track["trackId"]

            currentTrack = {"artist": "", "track": "", "trackId": ""} if(playerState == "Stopped") else {"artist": artist, "track": song, "trackId": trackId}

        stateObject = {
            "state": playerState,
            "currentTrack": currentTrack
        }

        self.database.child("simulatedDevices").child("playerState").set(stateObject)
        
    def discoverLocalMusic(self):
        localMusic: list = []
        for file in os.listdir('music'):
            if file.endswith(".mp3"):
                trackpath = f"./music/{file}"
                trackData = MP3(trackpath, ID3 = EasyID3)
                data = {
                    "artist": trackData["artist"],
                    "song": trackData["title"]
                }
                localMusic.append(data)
        return localMusic
    
    def getDatabaseMusic(self):
        databaseMusic = self.database.child("simulatedDevices").child("songList").get().val()
        return databaseMusic if type(databaseMusic) is list else list()
    
    def close(self):
        self.player = None
        self.database = None

class Action(Enum):
    PLAY = "play"
    PAUSE = "pause"
    STOP = "stop"
    NEXT = "next"
    PREV = "prev"





