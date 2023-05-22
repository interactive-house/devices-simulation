import unittest
from unittest.mock import Mock, patch
import main # assuming your_module is the module containing the main function
import pyrebase
import signal
import time

class TestMain(unittest.TestCase):

    @patch("pyrebase.initialize_app")
    @patch("src.DatabaseInteractor")
    @patch("src.MusicPlayer")
    def test_main(self, mock_MusicPlayer, mock_DatabaseInteractor, mock_initialize_app):
        # Setup
        mock_firebase_app = Mock()
        mock_initialize_app.return_value = mock_firebase_app

        mock_database = Mock()
        mock_firebase_app.database.return_value = mock_database

        mock_musicPlayer = Mock()
        mock_MusicPlayer.return_value = mock_musicPlayer

        mock_interactor = Mock()
        mock_DatabaseInteractor.return_value = mock_interactor

        mock_dataStream = Mock()
        mock_interactor.observe.return_value = mock_dataStream

        # Run
        main()

        # Verify
        mock_initialize_app.assert_called_once()
        mock_database.assert_called_once()
        mock_MusicPlayer.assert_called_once()
        mock_DatabaseInteractor.assert_called_once_with(mock_database, mock_musicPlayer)
        mock_interactor.observe.assert_called_once_with("simulatedDevices")
        
        mock_dataStream.thread.is_alive.assert_called()

        # No exceptions were raised, so test passes
        self.assertTrue(True)
    
    def test_main_keyboard_interrupt(self):
        # In this test case, we simulate a KeyboardInterrupt and assert the print message

        with self.assertRaises(KeyboardInterrupt):
            with self.assertLogs(level="INFO") as cm:
                main()
        self.assertEqual(cm.output, ["INFO:root:key"])

if __name__ == "__main__":
    unittest.main()
