import vlc

class MusicPlayer():

    musicDirectory = "music/"

    def __init__(self, tracklist: list):
        self.instance = vlc.Instance()
        self.player: vlc.MediaListPlayer = self.instance.media_list_player_new()
        self.tracklist: dict = tracklist
        self.setPlayerTracklist(tracklist)

    def play(self, track):
        # If a track is passed in, the index of the track is retrieved from the
        # tracklist dict and used to play the corresponding track in the MediaList.
        if track:
            trackIndex = None
            for i, key in enumerate(self.tracklist.keys()):
                if key == track:
                    trackIndex = i
            self.player.play_item_at_index(trackIndex)
        # If track is None and there is no current track loaded, the first track
        # of the list will play.
        # If track is None and there is a current track loaded that has been either
        # paused or stopped. The current track will resume playing. 
        # If the track is already playing, nothing will happen.
        else:
            self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def next(self):
        # nextResponse will be -1 when the end of the tracklist has been reached.
        # To make the player go back to the first track, next() must be called again.
        nextResponse = self.player.next()
        if nextResponse == -1:
            self.player.next()

    def previous(self):
        self.player.previous()

    # Creates Media objects and adds them to a MediaList. The created MediaList
    # is then assigned to the MediaListPlayer.
    def setPlayerTracklist(self, tracklist):
        mediaList = self.instance.media_list_new()
        for key in tracklist:
            path = self.musicDirectory + tracklist[key]
            media = self.instance.media_new(path)
            mediaList.add_media(media)
        self.player.set_media_list(mediaList)
