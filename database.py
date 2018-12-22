# database: Implements the database portion of the pycnumanal application
# 
#    VERSION 0.13
#
#    - create database/tables if they don't already exist
#    - add program to the database
#    - delete program from the database (and its timings)
#    - display programs in the database
#    - manually enter timings for a program
#    - generate/store timings for a program
#    - display timings for a program
#    - delete all of a program's timings
#    - plot timings for a program
#
#    - runs on Linux (not tested on Windows)
#    - Python 3.x (not tested with Python 2.x)
#    - SQlite (sqlite3) database used for storage
#    - no database operations error checking (as of yet)
#
# --------------------------------------------------------
#
# Change log:
#
#    12/07/2018 (pf)   Version 0.11:
#                      - created this module as part of this version's
#                        "separating the concerns" of the core, database,
#                        and user interface operations of pycnumanal version 0.10
#                      - stores database connection in GLOBAL VARIABLE: conn
#
#    12/08/2018 (pf)   Version 0.12:
#                      - added new functionalities to the overall application
#                          - manually entering in timings for a program
#                          - generating timings for a program
#                          - displaying timings for a program
#                      - added functions to support the new functionalities
#                          - get_timings()
#                          - add_timing()
#                          - get_cmd_line_prefix()
#
#    THIS CODE IS NOW pycnumanal VERSION, NOT pycnumanal-lessons VERSION
#
#    12/12/2018 (pf)   - added delete_program_timings()
#                      - timings table creation in schema.sql: 
#                          - added "on delete cascade" to program_name foreign key
#                      - gave the sqlite3 module import an abbreviation of "sql"
#                      - professionalized the commenting
#                          - pycnumanal-lessons version has more commenting for the student
#
#    12/20/2018 (pf)   - added delete_program()
#                      - modified create_db_connection() to support cascase deletion
#                          - conn.execute("PRAGMA foreign_keys = ON")
#
# (pf) Patrick Flynn
#
# ---------------------------------------------------------

import os
import sqlite3 as sql

# -----------------------------------------------------------------

def create_db_connection(db_filename, schema_filename) :
    """ Creates the database connection (database file created if needed)
    
        In:  db_filename     - database of all programs and their timings (string)
             schema_filename - structure of the programs/timings tables in the database (string)
        Out: nothing
        
        Side affect: intializes the global variable: conn
    """

    # GLOBAL VARIABLE
    global conn  # programs/timings database connection
    
    # does the database file exist in the current working directory?
    db_is_new = not os.path.exists(db_filename)

    # setup connection to the database
    # "connect" creates the database if it doesn't yet exist
    with sql.connect(db_filename) as conn:

        if db_is_new :  # create the tables if the database is newly created
            print('Created database, setting up tables')
            with open(schema_filename, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)

        else :  # database file already exists
            print('Database exists, assuming contains proper table structures.')
 
        # needed to support cascade deletion
        conn.execute("PRAGMA foreign_keys = ON")
        
# end program

# -----------------------------------------------------------------

def get_programs() :
    """ Get all the programs from the database

        In:  nothing
        Out: progs - all programs in database (list of tuples)
    """

    cur = conn.cursor()

    cur.execute("SELECT program_name, description, cmd_line_prefix FROM programs")    
    progs  = cur.fetchall()

    return progs

# end function: get_programs

# -----------------------------------------------------------------

def add_program(prog_name, prog_desc, cmd_line_prefix) :
    """ Add a new program to the database

        In:  prog_name       - program name (string)
             prog_desc       - program description (string)
             cmd_line_prefix - command line prefix (string)
        Out: nothing
    """

    cur = conn.cursor()

    cur.execute("INSERT INTO programs (program_name, description, cmd_line_prefix) VALUES (?, ?, ?)",
                (prog_name, prog_desc, cmd_line_prefix) )

    conn.commit()

# end function: add_program

# -----------------------------------------------------------------

def delete_program(prog_name) :
    """ Delete a program from the database

        In:  prog_name - program name (string)
        Out: nothing
    """

    cur = conn.cursor()

    cur.execute("DELETE FROM programs WHERE program_name = ?",
                (prog_name,) )

    conn.commit()

# end function: delete_program

# -----------------------------------------------------------------

def get_timings(prog_name) :
    """ Get a program's timings from the database

        In:  prog_name - name of the program getting timings for (string)
        Out: timings   - all timings for the given program (list of 2-tuples)
    """
    
    cur = conn.cursor()

    cur.execute("SELECT problem_size, timing FROM timings WHERE program_name = ? ORDER BY problem_size ASC",
                (prog_name,) )
    timings = cur.fetchall()

    return timings

# end function: get_timings

# -----------------------------------------------------------------

def add_timing(prog_name, prob_size, timing) :
    """ Add a program's timing for a problem size to the database

        In:  prog_name - name of the program getting timings for (string)
             prog_size - problem size (integer)
             timing    - timing (float)
        Out: nothing
    """ 

    cur = conn.cursor()  

    cur.execute("INSERT INTO timings (problem_size, timing, program_name) VALUES (?, ?, ?)",
                (prob_size, timing, prog_name) )

    conn.commit()

# end function: add_timing

# -----------------------------------------------------------------

def delete_program_timings(prog_name) :
    """ Delete all of a program's timings

        In:  prog_name - program whose timings are to be deleted (string)
        Out: nothing
    """ 

    cur = conn.cursor()

    cur.execute("DELETE FROM timings WHERE program_name = ?",
                (prog_name,) )

    conn.commit()

# end function: delete_program_timings

# -----------------------------------------------------------------

def get_cmd_line_prefix(prog_name) :
    """ Get a program's command line prefix from the database

        In:  prog_name       - name of the program getting timings for (string)
        Out: cmd_line_prefix - the program's command line prefix
    """
    
    cur = conn.cursor()

    cur.execute("SELECT cmd_line_prefix FROM programs WHERE program_name = ?",
                (prog_name,) )    
    cmd_line_prefix = cur.fetchall()[0][0]
    
    return cmd_line_prefix

# end function: get_cmd_line_prefix

# -----------------------------------------------------------------

