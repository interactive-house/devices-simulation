import unittest
from unittest.mock import Mock, patch
from src.musicPlayer import MusicPlayer
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3 
import os

class TestMusicPlayer(unittest.TestCase):

    @patch('src.musicPlayer.vlc.MediaListPlayer')
    @patch('src.musicPlayer.vlc.Instance')
    def setUp(self, mock_instance, mock_media_list_player):
        self.mock_instance = mock_instance
        self.mock_media_list_player = mock_media_list_player
        self.music_player = MusicPlayer()

    def test_play(self):
        self.music_player.tracklist = [{'trackId': '1'}, {'trackId': '2'}]

        self.music_player.play('2')

        self.mock_media_list_player.play_item_at_index.assert_called_once_with(1)

    def test_pause(self):
        self.music_player.pause()

        self.mock_media_list_player.pause.assert_called_once()

    def test_stop(self):
        self.music_player.stop()

        self.mock_media_list_player.stop.assert_called_once()

    @patch('src.musicPlayer.vlc.MediaListPlayer.next')
    def test_next(self, mock_next):
        mock_next.return_value = -1

        self.music_player.next()

        self.mock_media_list_player.next.assert_called_once()
        self.mock_media_list_player.play_item_at_index.assert_called_once_with(0)

    @patch('src.musicPlayer.vlc.MediaListPlayer.previous')
    def test_prev(self, mock_prev):
        self.music_player.tracklist = [{'trackId': '1'}, {'trackId': '2'}]
        mock_prev.return_value = -1

        self.music_player.prev()

        mock_prev.assert_called_once()
        self.mock_media_list_player.play_item_at_index.assert_called_once_with(1)

    @patch('src.musicPlayer.os.listdir')
    @patch('src.musicPlayer.MP3')
    def test_setTrackList(self, mock_MP3, mock_listdir):
        mock_MP3.return_value = MP3('music/song1.mp3', ID3=EasyID3)
        mock_MP3.return_value['artist'] = ['Artist 1']
        mock_MP3.return_value['title'] = ['Song 1']
        mock_listdir.return_value = ['song1.mp3']

        self.music_player.setTrackList([{'artist': 'Artist 1', 'song': 'Song 1', 'trackId': '1'}])

        self.mock_instance.media_list_new.assert_called_once()
        self.mock_instance.media_new.assert_called_once_with('music/song1.mp3')
        self.mock_instance.media_list_new().add_media.assert_called_once_with(self.mock_instance.media_new())
        self.mock_media_list_player.set_media_list.assert_called_once_with(self.mock_instance.media_list_new())
