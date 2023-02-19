import unittest
from unittest.mock import patch, MagicMock
from common.sqlite import SQLite3


class TestSQLite3(unittest.TestCase):
    @patch('common.sqlite.sqlite3.connect')
    def test_connect(self, mock_connect):
        server = 'test.db'
        conn = MagicMock()
        mock_connect.return_value = conn

        returned_conn = SQLite3.connect(server)

        mock_connect.assert_called_once_with(server)
        self.assertEqual(returned_conn, conn)

    def test_execute_query_with_params(self):
        conn = MagicMock()
        query = """
            SELECT * FROM test_table WHERE id = :id
        """
        params = {'id': 1}
        expected_data = [{'id': 1, 'name': 'test'}]
        cursor = conn.cursor()
        cursor.description = [('id',), ('name',)]
        cursor.fetchall.return_value = [(1, 'test')]
        conn.cursor.return_value = cursor

        with patch.object(cursor, 'execute', return_value=None) as mock_execute:
            data = SQLite3.execute_query_with_params(conn, query, **params)

            mock_execute.assert_called_once_with(query, params)
            self.assertEqual(data, expected_data)