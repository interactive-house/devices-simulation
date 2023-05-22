import unittest
from unittest.mock import Mock, patch
from src.testClient import config
import pyrebase

class TestTestClient(unittest.TestCase):

    @patch('src.testClient.pyrebase.initialize_app')
    @patch('src.testClient.input', create=True)
    def test_valid_action(self, mock_input, mock_initialize_app):
        # Setting up mocks
        mock_db = Mock()
        mock_initialize_app.return_value.database.return_value = mock_db
        mock_db.child().child().get().val.return_value = [{'trackId': '1'}]
        mock_input.side_effect = ['play-0', 'q']

        # Importing and running the script
        import testClient

        # Asserting the correct calls were made
        mock_db.child().child().set.assert_called_once_with({
            'id': unittest.mock.ANY,  # don't care about the exact uuid
            'type': 'play',
            'trackId': '1'
        })

    @patch('src.testClient.pyrebase.initialize_app')
    @patch('src.testClient.input', create=True)
    def test_invalid_action(self, mock_input, mock_initialize_app):
        # Setting up mocks
        mock_db = Mock()
        mock_initialize_app.return_value.database.return_value = mock_db
        mock_db.child().child().get().val.return_value = [{'trackId': '1'}]
        mock_input.side_effect = ['invalid', 'q']

        # Importing and running the script
        import testClient

        # Asserting the database set method was not called
        mock_db.child().child().set.assert_not_called()

    # Similarly, other tests can be written for 'pause', 'stop', 'next', 'prev', and boundary conditions

if __name__ == "__main__":
    unittest.main()
