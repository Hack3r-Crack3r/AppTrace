import unittest
from unittest.mock import patch
from solution import main


class TestSolution(unittest.TestCase):

    @patch('sys.argv', [])
    @patch('common.configparser_lib.ConfigReader.getconfig')
    @patch('app.app.ApplicationTrace.retrieve_slowest_action')
    @patch('builtins.print')
    def test_main_no_arguments(self, mock_print, mock_retrieve_slowest_action, mock_getconfig):
        """
        Test for main() function when there are no command line arguments passed.

        Args:
            mock_print (unittest.mock.Mock): A mock for the built-in `print` function.
            mock_retrieve_slowest_action (unittest.mock.Mock): A mock for the `retrieve_slowest_action` method of the
                                                               `ApplicationTrace` class.
            mock_getconfig (unittest.mock.Mock): A mock for the `getconfig` method of the `ConfigReader` class.
        """
        # Arrange
        mock_getconfig.return_value = 1
        mock_retrieve_slowest_action.return_value = {
            'error': False,
            'results': [
                {
                    'id': 1,
                    'duration': 100,
                    'action': 'action1',
                    'page': 'page1'
                },
                {
                    'id': 2,
                    'duration': 200,
                    'action': 'action2',
                    'page': 'page2'
                }
            ]
        }

        # Act
        main()

        # Assert
        mock_getconfig.assert_called_once_with('retrieve', 'limit', 1)
        mock_retrieve_slowest_action.assert_called_once_with(1, None)
        mock_print.assert_has_calls([
            unittest.mock.call('1 100 action1 page1'),
            unittest.mock.call('2 200 action2 page2'),
        ])

    @patch('sys.argv', ['', 'server_name', '2'])
    @patch('common.configparser_lib.ConfigReader.getconfig')
    @patch('app.app.ApplicationTrace.retrieve_slowest_action')
    @patch('builtins.print')
    def test_main_with_arguments(self, mock_print, mock_retrieve_slowest_action, mock_getconfig):
        """
        Test for main() function when server name and limit are passed as command line arguments.

        Args:
            mock_print (unittest.mock.Mock): A mock for the built-in `print` function.
            mock_retrieve_slowest_action (unittest.mock.Mock): A mock for the `retrieve_slowest_action` method of the
                                                               `ApplicationTrace` class.
            mock_getconfig (unittest.mock.Mock): A mock for the `getconfig` method of the `ConfigReader` class.
        """
        # Arrange
        mock_getconfig.return_value = 1
        mock_retrieve_slowest_action.return_value = {
            'error': False,
            'results': [
                {
                    'id': 1,
                    'duration': 100,
                    'action': 'action1',
                    'page': 'page1'
                },
                {
                    'id': 2,
                    'duration': 200,
                    'action': 'action2',
                    'page': 'page2'
                }
            ]
        }

        # Act
        main()

        # Assert
        mock_getconfig.assert_not_called()
        mock_retrieve_slowest_action.assert_called_once_with(2, 'server_name')
        mock_print.assert_has_calls([
            unittest.mock.call('1 100 action1 page1'),
            unittest.mock.call('2 200 action2 page2'),
        ])

    @patch('sys.argv', ['', 'server_name', 'invalid_limit'])
    @patch('common.configparser_lib.ConfigReader.getconfig')
    @patch('app.app.ApplicationTrace.retrieve_slowest_action')
    @patch('builtins.print')
    def test_main_with_invalid_limit(self, mock_print, mock_retrieve_slowest_action, mock_getconfig):
        """
        Test for main() function when server name and limit are passed as command line arguments.

        Args:
            mock_print (unittest.mock.Mock): A mock for the built-in `print` function.
            mock_retrieve_slowest_action (unittest.mock.Mock): A mock for the `retrieve_slowest_action` method of the
                                                               `ApplicationTrace` class.
            mock_getconfig (unittest.mock.Mock): A mock for the `getconfig` method of the `ConfigReader` class.
        """
        # Arrange
        mock_getconfig.return_value = 1
        mock_retrieve_slowest_action.return_value = {
            'error': False,
            'results': [
                {
                    'id': 1,
                    'duration': 100,
                    'action': 'action1',
                    'page': 'page1'
                },
                {
                    'id': 2,
                    'duration': 200,
                    'action': 'action2',
                    'page': 'page2'
                }
            ]
        }

        # Act
        main()

        # Assert
        mock_getconfig.assert_called_once_with('retrieve', 'limit', 1)
        mock_retrieve_slowest_action.assert_called_once_with(1, 'server_name')
