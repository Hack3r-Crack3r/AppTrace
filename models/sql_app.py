import os
import sys
from common.constants import log_err_message
from common.sqlite import SQLite3

sys.path.append(os.getcwd())


class SQLApplicationTrace:
    """
    This class contains methods to interact with the SQLite database that stores application trace data.
    """

    server_file = None

    @classmethod
    def set_server_file(cls, value):
        """
        Sets the path to the SQLite database file.
        """
        cls.server_file = value

    @classmethod
    def get_server_file(cls):
        """
        Returns the path to the SQLite database file.
        """
        return cls.server_file

    @staticmethod
    def check_sql_db_exists():
        """
        Checks if the SQLite database file exists.
        """
        func_name = __name__ + "SqlApplicationTrace.check_sql_db_exists"
        try:
            if os.path.isfile(SQLApplicationTrace.get_server_file()):
                return True
            else:
                return False
        except Exception as e:
            log_err_message(func_name, str(e))

    @staticmethod
    def sql_retrieve_slowest_action(limit=1):
        """
        Retrieves the slowest action from the SQLite database.
        """
        func_name = __name__ + "SqlApplicationTrace.sql_retrieve_slowest_action"
        conn = None
        data = None
        try:
            conn = SQLite3.connect(SQLApplicationTrace.get_server_file())
            query = """
            SELECT id, 
                (endTimeStamp-startTimestamp) AS duration,
                json_extract(data, '$.action') AS action, 
                json_extract(data, '$.navigation_history[#-1]') AS page
            FROM  AppTrace
            ORDER by duration DESC
            LIMIT :limit
            """
            data = SQLite3.execute_query_with_params(conn, query, limit=limit)

        except Exception as e:
            log_err_message(func_name, str(e))
        finally:
            if conn is not None:
                conn.close()
        return data
