import vlc

class MusicPlayer():

    musicDirectory = "music/"

    def __init__(self, tracklist: list):
        self.instance = vlc.Instance()
        self.player: vlc.MediaListPlayer = self.instance.media_list_player_new()
        self.tracklist: list = tracklist
        self.setPlayerTracklist(tracklist)

    def play(self, trackId):
        # If a track is passed in, the index of the track is retrieved from the tracklist 
        # dict and used to play the corresponding track at that index in the MediaList.
        if trackId:
            trackIndex = None
            for i, track in enumerate(self.tracklist):
                if track["trackId"] == trackId:
                    trackIndex = i
            self.player.play_item_at_index(trackIndex)
        # If track is None and there is no current track loaded, the first track
        # of the list will play.
        # If track is None and there is a current track loaded that has been either
        # paused or stopped. The current track will resume playing. 
        # If the track is already playing, nothing will happen.
        else:
            self.player.play()

    # Pause playback of current track, nothing happens if no loaded track is playing.
    def pause(self):
        self.player.pause()

    # Stop playback of current track, This will also move the progress of the currently
    # loaded song back to the start. Nothing happens if no song is loaded or playing.
    def stop(self):
        self.player.stop()

    # nextResult will be -1 if next() is called on the final track in the list.
    # When -1 is returned, play the first track in the list.
    def next(self):
        nextResult = self.player.next()
        if nextResult == -1:
            self.player.play_item_at_index(0)

    # Previous result will be -1 if prev() is called on the first track in the list.
    # When -1 is returned, play the last track in the list.
    def prev(self):
        previousResult = self.player.previous()
        if previousResult == -1:
            lastIndex = len(self.tracklist) - 1
            self.player.play_item_at_index(lastIndex)
        

    # Creates vlc Media objects and adds them to a vlc MediaList. 
    # The created vlc MediaList is then assigned to the vlc MediaListPlayer.
    def setPlayerTracklist(self, tracklist):
        mediaList = self.instance.media_list_new()
        for track in tracklist:
            artist = str(track["artist"]).strip()
            song = str(track["song"]).strip()
            path = f"{self.musicDirectory}{artist} - {song}.mp3"
            media = self.instance.media_new(path)
            mediaList.add_media(media)
        self.player.set_media_list(mediaList)
