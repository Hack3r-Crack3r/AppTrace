import unittest
from unittest.mock import patch
from app.app import ApplicationTrace
from common.constants import ERROR, MESSAGE, RESULTS, SUCCESSFUL, DATABASE, FILENAME, APP_TRACE_DB


class TestApplicationTrace(unittest.TestCase):

    # Arrange
    @patch('app.app.ConfigReader.getconfig', return_value='test_server')
    @patch('app.app.SQLApplicationTrace.check_sql_db_exists', return_value=True)
    @patch('app.app.SQLApplicationTrace.sql_retrieve_slowest_action', return_value=[{'action': 'test_action'}])
    def test_retrieve_slowest_action(self, mock_retrieve_slowest_action,
                                     mock_check_sql_db_exists, mock_getconfig):
        # Act
        result = ApplicationTrace.retrieve_slowest_action(1, None)

        # Assert
        self.assertEqual(result[ERROR], False)
        self.assertEqual(result[MESSAGE], SUCCESSFUL)
        self.assertEqual(result[RESULTS], [{'action': 'test_action'}])
        mock_getconfig.assert_called_once_with(DATABASE, FILENAME, APP_TRACE_DB)
        mock_check_sql_db_exists.assert_called_once()
        mock_retrieve_slowest_action.assert_called_once_with(1)

    # Arrange
    @patch('app.app.ConfigReader.getconfig', return_value='test_server')
    @patch('app.app.SQLApplicationTrace.check_sql_db_exists', return_value=False)
    def test_retrieve_slowest_action_with_error(self, mock_check_sql_db_exists, mock_getconfig):
        # Act
        result = ApplicationTrace.retrieve_slowest_action(1, None)

        # Arrange
        self.assertEqual(result[ERROR], True)
        self.assertEqual(result[MESSAGE], 'Something went wrong !!!')
        self.assertIsNone(result[RESULTS])
        mock_getconfig.assert_called_once_with(DATABASE, FILENAME, APP_TRACE_DB)
        mock_check_sql_db_exists.assert_called_once()
