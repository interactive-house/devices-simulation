# Music player class that will set up the player and have functions executed
# by the DatabaseInteractor class when changes occur in the database.

import pygame
import os
from enum import Enum

class MusicPlayer:
    
    musicDirectory = "music/"
    
    def __init__(self):
        print("Setting up the music player")
        self.trackList = self.setTrackList()
        self.playerState = PlayerState.STOP
        self.currentTrack = None
        pygame.init()
        pygame.mixer.init()
        self.initUI()

    # # # #
    
    def play(self):
        
        # Do nothing if player is already playing
        if(self.playerState == PlayerState.PLAY):
            return
        
        # If no track is loaded, play first in music directory
        if(self.currentTrack is None):
          pygame.mixer.music.play(self.musicDirectory + self.trackList[0])

        # Resume playing
        pygame.mixer.music.play()

        self.playerState = PlayerState.PLAY

    # # # #

    def pause(self):
        print("Executing pause in the music player instance")

    # # # #

    def stop(self):
        print("Executing stop in the music player instance")

    # # # #

    def changeTrack(self, track):
        print(f"Changing track in music player to {track}")

    # # # #

    def initUI(self):

      # set up the window
      win_width = 600
      win_height = 400
      win = pygame.display.set_mode((win_width, win_height))
      pygame.display.set_caption("Music Player")

      # set up the buttons
      play_button = pygame.Rect(50, 50, 150, 50)
      pause_button = pygame.Rect(225, 50, 150, 50)
      stop_button = pygame.Rect(400, 50, 150, 50)

      # set up the font
      font = pygame.font.SysFont(None, 48)

      # set up the progress bar
      progress_width = 500
      progress_height = 20
      progress_x = (win_width - progress_width) // 2
      progress_y = (win_height - progress_height) // 2
      progress_border_width = 2
      progress_border_color = (255, 255, 255)
      progress_color = (0, 255, 0)
      progress_rect = pygame.Rect(progress_x, progress_y, progress_width, progress_height)

      # set up the clock
      clock = pygame.time.Clock()

      # clear the screen
      win.fill((0, 0, 0))

      # draw the buttons
      pygame.draw.rect(win, (0, 255, 0), play_button)
      pygame.draw.rect(win, (255, 255, 0), pause_button)
      pygame.draw.rect(win, (255, 0, 0), stop_button)

      # draw the button text
      play_text = font.render("Play", True, (255, 255, 255))
      pause_text = font.render("Pause", True, (0, 0, 0))
      stop_text = font.render("Stop", True, (255, 255, 255))
      win.blit(play_text, (play_button.x + 10, play_button.y + 10))
      win.blit(pause_text, (pause_button.x + 10, pause_button.y + 10))
      win.blit(stop_text, (stop_button.x + 10, stop_button.y + 10))

      # update the display  
      pygame.display.update()

    # # # #

    def setTrackList(self):
        discoveredTracks = []
        try:
          for file in os.listdir(self.musicDirectory):
            if file.endswith(".mp3"):
                discoveredTracks.append(file)
          # TODO Update firebase with the tracklist
          return discoveredTracks
        except(Exception):
            print("An error occurred during track discovery")

    # # # #

# Enum Class to hold player state values
class PlayerState(Enum):
    STOP = "stop"
    PLAY = "play"
    PAUSE = "pause"
