import os
import unittest
from unittest.mock import patch, MagicMock
from models.sql_app import SQLApplicationTrace


class TestSQLApplicationTrace(unittest.TestCase):

    def setUp(self):
        SQLApplicationTrace.set_server_file('test_db.sqlite')

    @patch('models.sql_app.os.path.isfile', return_value=True)
    def test_check_sql_db_exists(self, mock_isfile):
        # Arrange

        # Act
        result = SQLApplicationTrace.check_sql_db_exists()

        # Assert
        self.assertTrue(result)
        mock_isfile.assert_called_once_with('test_db.sqlite')

    @patch('models.sql_app.os.path.isfile', return_value=False)
    def test_check_sql_db_not_exists(self, mock_isfile):
        # Arrange

        # Act
        result = SQLApplicationTrace.check_sql_db_exists()

        # Assert
        self.assertFalse(result)
        mock_isfile.assert_called_once_with('test_db.sqlite')

    @patch('models.sql_app.SQLite3.connect')
    @patch('models.sql_app.SQLite3.execute_query_with_params')
    def test_sql_retrieve_slowest_action(self, mock_execute_query, mock_connect):
        # Arrange
        mock_connect.return_value = MagicMock()
        mock_execute_query.return_value = [{
            'id': 1,
            'duration': 10,
            'action': 'test_action',
            'page': 'test_page'
        }]

        # Act
        result = SQLApplicationTrace.sql_retrieve_slowest_action()

        # Assert
        self.assertEqual(result, [{
            'id': 1,
            'duration': 10,
            'action': 'test_action',
            'page': 'test_page'
        }])
        mock_execute_query.assert_called_once_with(
            mock_connect.return_value,
            """
            SELECT id, 
                (endTimeStamp-startTimestamp) AS duration,
                json_extract(data, '$.action') AS action, 
                json_extract(data, '$.navigation_history[#-1]') AS page
            FROM  AppTrace
            ORDER by duration DESC
            LIMIT :limit
            """,
            limit=1
        )
