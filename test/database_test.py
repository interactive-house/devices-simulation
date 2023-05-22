import unittest
from unittest.mock import Mock, patch
from src.databaseInteractor import DatabaseInteractor, Action
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import os

class TestDatabaseInteractor(unittest.TestCase):

    @patch('src.databaseInteractor.MusicPlayer')
    @patch('pyrebase.Database')
    def setUp(self, mock_database, mock_music_player):
        self.database_interactor = DatabaseInteractor(mock_database, mock_music_player)
        self.mock_database = mock_database
        self.mock_music_player = mock_music_player

    @patch('src.databaseInteractor.DatabaseInteractor.updatePlayerState')
    @patch('src.databaseInteractor.DatabaseInteractor.updateDeviceStatus')
    def test_observe(self, mock_updateDeviceStatus, mock_updatePlayerState):
        mock_datastream = Mock()
        self.mock_database.child().stream.return_value = mock_datastream

        result = self.database_interactor.observe("simulatedDevices")

        self.mock_database.child.assert_called_with("simulatedDevices")
        self.mock_database.child().stream.assert_called_once_with(self.database_interactor.onChange)
        self.assertEqual(result, mock_datastream)

    @patch('src.databaseInteractor.time.sleep')
    def test_onChange(self, mock_sleep):
        mock_message = {"path": "/action", "data": {"type": Action.PLAY.value, "trackId": "1"}}
        
        self.database_interactor.onChange(mock_message)

        self.mock_music_player.play.assert_called_once_with("1")
        mock_sleep.assert_called_once_with(1)

    # Add more tests for onChange for other action types...

    @patch('src.databaseInteractor.os.listdir')
    @patch('src.databaseInteractor.MP3')
    def test_discoverLocalMusic(self, mock_MP3, mock_listdir):
        mock_MP3.return_value = MP3('music/song1.mp3', ID3=EasyID3)
        mock_MP3.return_value['artist'] = 'Artist 1'
        mock_MP3.return_value['title'] = 'Song 1'
        mock_listdir.return_value = ['song1.mp3']

        result = self.database_interactor.discoverLocalMusic()

        mock_listdir.assert_called_once_with('music')
        mock_MP3.assert_called_once_with('./music/song1.mp3', ID3=EasyID3)
        self.assertEqual(result, [{'artist': 'Artist 1', 'song': 'Song 1'}])
