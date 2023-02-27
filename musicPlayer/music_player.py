import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pygame
import time
import threading
from mutagen.mp3 import MP3

# Initialize Pygame mixer
pygame.mixer.init()

# Initialize Firebase Admin SDK with your Firebase credentials JSON file
cred = credentials.Certificate('musicPlayer/cred/test-4e615-firebase-adminsdk-3xa2x-85d09f9cf0.json') 
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-4e615-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Create a reference to the 'songs' location in your Firebase Realtime Database
ref = db.reference('songs')

# Define the directory where your music files are stored
music_dir = 'musicPlayer/songs/'

# Scan the music directory for music files and store them in a list
songs = []
for file_name in os.listdir(music_dir):
    if file_name.endswith('.mp3'):  # Change to the file format you are using
        songs.append(file_name)

# Send the list of songs to Firebase Realtime Database
ref.set(songs)

pygame.init()

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

# start the music
pygame.mixer.music.load(music_dir + songs[0])
song = MP3(music_dir + songs[0])

# set up the initial song state
song_playing = False
song_paused = False

# main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # check if play button is clicked
            if play_button.collidepoint(event.pos):
                if not song_playing:
                    pygame.mixer.music.play()
                    song_playing = True
                    song_paused = False
            # check if pause button is clicked
            elif pause_button.collidepoint(event.pos):
                if song_playing:
                    if not song_paused:
                        pygame.mixer.music.pause()
                        song_paused = True
                    else:
                        pygame.mixer.music.unpause()
                        song_paused = False
            # check if stop button is clicked
            elif stop_button.collidepoint(event.pos):
                if song_playing:
                    pygame.mixer.music.stop()
                    song_playing = False
                    song_paused = False

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

    # draw the progress bar
    pygame.draw.rect(win, progress_border_color, progress_rect, progress_border_width)
    progress = pygame.mixer.music.get_pos() / 1000  # get the progress of the music in seconds
    progress_width_current = int(progress / song.info.length * progress_width)
    progress_rect_current = pygame.Rect(progress_x, progress_y, progress_width_current, progress_height)
    pygame.draw.rect(win, progress_color, progress_rect_current)

    # draw song name text
    song_text = font.render(songs[0], True, (255, 255, 255))
    win.blit(song_text, (progress_rect.x, progress_rect.y + 30))

    # update the display
    pygame.display.update()

    # tick the clock
    clock.tick(60)

# quit pygame
pygame.quit()

# # Create a reference to the 'instructions' location in your Firebase Realtime Database
# ref = db.reference('instructions')

# # Initialize the current playlist and current index
# playlist = []
# current_index = 0

# # Listen for changes to the 'instructions' location in your Firebase Realtime Database
# def callback(event):
#     global playlist
#     global current_index
    
#     # Retrieve the updated instructions data from the Firebase Realtime Database
#     instructions = ref.get()
    
#     # Parse the instructions data and update the playlist and current index
#     playlist = []
#     for song in instructions:
#         playlist.append(song['filename'])
#     current_index = 0
    
#     # Stop any currently playing music and play the first song in the playlist
#     pygame.mixer.music.stop()
#     pygame.mixer.music.load(playlist[current_index])
#     pygame.mixer.music.play()

# ref.listen(callback)

# # Wait for the music player to finish playing before exiting the script
# while pygame.mixer.music.get_busy():
#     pass

# Stop Pygame mixer and close the Firebase connection
pygame.mixer.quit()
firebase_admin.delete_app(firebase_admin.get_app())
