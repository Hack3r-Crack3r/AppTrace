#!/usr/bin/env python3

"""
This module provides a command-line interface for retrieving the slowest actions recorded by an application.

Usage:
    python3 solution.py [SERVER_NAME] [LIMIT]

    SERVER_NAME: (optional) name of the sqlite3 db server to retrieve data from
    LIMIT: (optional) maximum number of records to retrieve
"""

import datetime
import logging
import sys
import traceback

from app.app import ApplicationTrace
from common.configparser_lib import ConfigReader
from common.constants import ERROR, LIMIT, MESSAGE, RETRIEVE, RESULTS


def main():
    """
    Retrieve the slowest actions recorded by an application and print them to the console.
    """
    time_now = datetime.datetime.now().strftime("%Y_%m_%d")

    # Every time new file will create with current time of application runs
    filepath = f"logs/application_trace_{time_now}.log"

    logging.basicConfig(filename=filepath, level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
    logging.info("----------------------")
    logging.info("Program Started")

    try:
        # Get the command line arguments
        args = sys.argv
        server_name = None
        limit = None

        # Check if there are 2 command line arguments i.e. filename & limit
        if len(args) == 3:
            server_name = args[1]
            try:
                limit = int(args[2])
            except ValueError:
                limit = None

        # Check if there is 1 command line argument i.e. either filename or limit
        elif len(args) == 2:
            try:
                limit = int(args[1])
            except ValueError:
                server_name = args[1]
                limit = None

        # Check if limit is not a digit
        if limit is None or not str(limit).isdigit():
            limit = ConfigReader.getconfig(RETRIEVE, LIMIT, 1)

        # Retrieve the slowest action data
        output = ApplicationTrace.retrieve_slowest_action(limit, server_name)

        if not output[ERROR]:
            # Print the data in the required format
            for item in output[RESULTS]:
                output_str = f"{item['id']} {item['duration']} {item['action']} {item['page']}"
                print(output_str)
        else:
            print(output[MESSAGE])
    except Exception as e:
        # Log any exceptions that occur
        exc_type, exc_obj, exc_tb = sys.exc_info()
        tb_msg = traceback.format_exc()
        logging.error("Exception occurred\nType: {}\nName:{}\nTraceback:{}".format(exc_type, exc_obj, tb_msg))


if __name__ == '__main__':
    main()
