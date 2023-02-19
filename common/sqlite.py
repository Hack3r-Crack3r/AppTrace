import logging
import sqlite3
import uuid
from common.constants import log_err_message
from datetime import datetime


class SQLite3:
    """
    A utility class for SQLite3 database operations.
    """
    @staticmethod
    def connect(server):
        """
        Creates a connection to the given SQLite3 server.

        Args:
            server (str): The path to the SQLite3 database file.

        Returns:
            sqlite3.Connection: The connection to the SQLite3 server.
        """
        conn = None
        func_name = f"{__name__}.SQLite3.connect"
        try:
            conn = sqlite3.connect(server)
        except Exception as e:
            log_err_message(func_name, str(e))
        return conn

    @staticmethod
    def execute_query_with_params(conn, query, **kwargs):
        """
        Executes a parameterized query on a SQLite3 connection.

        Args:
            conn (sqlite3.Connection): The connection to the SQLite3 server.
            query (str): The parameterized query to execute.
            **kwargs: The parameter values to substitute in the query.

        Returns:
            list: The results of the query as a list of dictionaries.
        """
        func_name = f"{__name__}.SQLite3.execute_query_with_params"
        cursor = None
        data = []
        sql = query
        try:
            cursor = conn.cursor()
            params = {k: v for k, v in kwargs.items()}
            cursor.execute(query, params)
            cols = [d[0].lower() for d in cursor.description]
            fetch_result = cursor.fetchall()
            for row in fetch_result:
                for i, j in enumerate(row):
                    try:
                        if isinstance(j, memoryview):
                            row[i] = str(uuid.UUID(bytes_le=str(j)))
                        elif type(j) == datetime:
                            row[i] = j.isoformat()
                        elif type(j) == bytearray:
                            row[i] = str(uuid.UUID(bytes_le=str(j)))
                    except Exception as e:
                        row[i] = None
            for rs in fetch_result:
                zip_data = dict(zip(cols, rs))
                data.append(zip_data)
        except Exception as e:
            log_err_message(func_name, str(e))
        return data
