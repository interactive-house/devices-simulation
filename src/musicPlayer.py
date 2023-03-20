# Music player class that will set up the player and have functions executed
# by the DatabaseInteractor class when changes occur in the database.

class MusicPlayer:
    
    def __init__(self):
        print("Setting up the music player")
    
    def play(self):
        print("Executing play in the music player instance")

    def pause(self):
        print("Executing pause in the music player instance")

    def stop(self):
        print("Executing stop in the music player instance")

    def changeTrack(self, track):
        print(f"Changing track in music player to {track}")