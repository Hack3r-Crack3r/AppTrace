#!/usr/bin/env python

import logging
import os
from models.sql_app import SQLApplicationTrace
from common.configparser_lib import ConfigReader
from common.constants import (DATABASE, APP_TRACE_DB, FILENAME,
                              ERROR, MESSAGE, RESULTS, SUCCESSFUL,
                              ERR_MSG)


class ApplicationTrace:
    """This class retrieves the slowest action from the SQL database and provides a summary of the data."""

    @staticmethod
    def retrieve_slowest_action(limit, server_name):
        """
        This method retrieves the slowest actions from the SQL database and returns a dictionary containing the results.

        Args:
            limit (int): Maximum number of results to retrieve.
            server_name (str): The name of the server on which the SQL database is stored.

        Returns:
            dict: A dictionary containing the results of the SQL query.
        """
        func_name = __name__ + 'ApplicationTrace.retrieve_slowest_action'
        result = {ERROR: True, MESSAGE: None, RESULTS: None}
        data = None
        try:
            if server_name is None:
                server_name = ConfigReader.getconfig(DATABASE, FILENAME, APP_TRACE_DB)

            file_path = os.path.join(os.getcwd(), server_name)
            SQLApplicationTrace.set_server_file(file_path)

            if not SQLApplicationTrace.check_sql_db_exists():
                logging.error("Database file missing in the directory")
                result[MESSAGE] = "Something went wrong !!!"
                return result

            data = SQLApplicationTrace.sql_retrieve_slowest_action(limit)
            if data is not None:
                result[ERROR] = False
                result[MESSAGE] = SUCCESSFUL
                result[RESULTS] = data
        except Exception as e:
            err_str = ERR_MSG.format(module_name=func_name, error_msg=str(e))
            logging.error(err_str)
            result[MESSAGE] = 'Something went wrong !!!'
        return result
