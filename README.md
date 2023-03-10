# AppTrace SQLite Database

## Description
The AppTrace database is a SQLite database has performance metrics of a mobile application. The database stores records of each user action, including the start and end times of the action, the duration, the action name, and the page navigated to after the action.

## Schema
The AppTrace database has a single table named `AppTrace`, which contains the following columns:
- `id`: integer (primary key)
- `startTimestamp`: timestamp
- `endTimeStamp`: timestamp
- `duration`: integer
- `data`: JSON object
  - `action`: string
  - `navigation_history`: array of strings

## Usage
The `app.py` file contains methods for interacting with the AppTrace database, retrieving the slowest actions. The `SQLApplicationTrace` class provides methods for checking if the database file exists and for retrieving the slowest actions. 

To retrieve the slowest actions, use the `SQLApplicationTrace` class's `sql_retrieve_slowest_action` method, passing in the number of results to retrieve and the path to the database file (if not in the same directory as `app.py`) as arguments.


# Dependencies

#### The AppTrace uses the following dependencies:

- Python 3.11.2
- SQLite3


## Getting Started


### Installation

1. Clone the repository: `git clone https://github.com/Hack3r-Crack3r/AppTrace.git`
2. Change into the directory: `cd AppTrace`

### Running the Application

To execute the application, run `python3 solution.py` using the command line
or any IDE like pycharm and set python interpreter v3.11.2 `[venv or system]` 

The default values of the command line arguments are:
- server_name/DB_name: apptrace.db
- limit: 1

### Entry Point of Application

The entry point of the application is `solution.py`. It can take two command line arguments:
- server_name/DB_name
- limit

### Example Usage

- `python3 solution.py apptrace.db 1`: Takes user requested arguments.
- `python3 solution.py apptrace.db`: Takes server_name as user requested, and limit as default value.
- `python3 solution.py 10`: Takes limit as user requested, and server_name as default value.