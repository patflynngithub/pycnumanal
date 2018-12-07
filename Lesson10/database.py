# database: Implements the database portion of the pycnumanal application
# 
#     VERSION 0.11
#
#    - creates database if doesn't already exist
#    - adds programs to the database: names, descriptions, command line names
#    - displays programs in the database
#
#    - runs on Linux (not tested on Windows)
#    - Python 3.x (not tested with Python 2.x)
#    - SQlite (sqlite3) database used for storage
#    - no error checking
#
# --------------------------------------------------------
#
# Change log:
#
#    12/07/2018 (pf)   Version 0.11:
#                      - created this module as part of this version's
#                        "separating the concerns" of central, database,
#                        and user_interface operations
#                      - checks to see if database file exists
#                      - creates database/tables, if needed
#                      - adds programs to database
#                      - gets all programs from database
#
# (pf) Patrick Flynn
#
# ---------------------------------------------------------

import sys
import os
import sqlite3

# -----------------------------------------------------------------

def create_db_connection(db_filename, schema_filename) :
    """ Creates the database connection
    
        In:  db_filename     - database of all programs and their timings
             schema_filename - structure of the programs/timings tables in the database
        Out: conn            - programs/timings database connection
    """
    
    # does the database file exist in the current working directory?
    db_is_new = not os.path.exists(db_filename)

    # setup connection to the database
    with sqlite3.connect(db_filename) as conn:  # "connect" creates the database if it doesn't yet exist

        if db_is_new :  # create the tables if the database is newly created
            print('Created database, setting up tables')
            with open(schema_filename, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)

        else :  # database file already exists
            print('Database exists, assuming contains proper table structures.')
    
    return conn

# end program

# -----------------------------------------------------------------

def get_programs(conn) :
    """ Get all the programs from the database

        In:  conn  - programs/timings database connection
        Out: progs - all programs in database (list of tuples)
    """

    cur = conn.cursor()  # database table cursor

    # get all programs in the database
    cur.execute("SELECT program_name, description, cmd_line_name FROM programs")    
    progs  = cur.fetchall()

    return progs

# end function: get_programs

# -----------------------------------------------------------------

def add_program(conn, prog_name, prog_desc, cmd_line_name) :
    """ Add a new program to the database

        In:  conn          - programs/timings database connection
             prog_name     - program name
             prog_desc     - program description
             cmd_line_name - command line name
        Out: nothing
    """

    cur = conn.cursor()  # database table cursor

    # insert the new program into programs table
    cur.execute("INSERT INTO programs (program_name, description, cmd_line_name) VALUES (?, ?, ?)",
                (prog_name, prog_desc, cmd_line_name) )

    # finalize the database data addition
    conn.commit()

# end function: add_program

# -----------------------------------------------------------------
