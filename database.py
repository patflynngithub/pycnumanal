# database.py : Implements the database portion of the pycnumanal application
# 
#    VERSION 0.13
#
#    - runs on Linux (not tested on Windows)
#    - Python 3.x (not tested with Python 2.x)
#    - SQlite (sqlite3) database used for storage
#    - no database operations error checking (as of yet)
#        - starting to add this
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
#    12/22/2018 (pf)   - started process of adding exception handling to database functions
#                           - get_programs()
#
#    12/27/2018 (pf)   - added get_program_info_from_DB()
#
#    12/29/2018 (pf)   - changed name of get_program_info_from_DB() to get_program_info()
#                      - modified get_program_info()
#                           - data is returned with each field's values having their own separate list
#                             rather than each data row having its own list, which is inside of the overall list
#                           - avoids calling functions in other modules having to know the order (list indices)
#                             of entries in a list inside of an overall list
#
#    12/30/2018 (pf)   - modified get_programs())
#                                 get_timings()
#                           - data is returned with each field's values having their own separate list
#                             rather than each data row having its own list, which is inside of the overall list
#                           - avoids calling functions in other modules having to know the order (list indices)
#                             of entries in a list inside of an overall list
#                      - added close_db()
#                      - modified get_cmd_line_prefix() to account for no prefix found
#
# (pf) Patrick Flynn
#
# ---------------------------------------------------------

# standard modules
import os

# third-party modules
import sqlite3 as sql

# custom modules
import db_exceptions as dbe

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
    
    # does the database file not exist in the current working directory?
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
            print('Database exists, assuming it contains proper table structures.')
 
        # needed to support cascade deletion in SQLite
        conn.execute("PRAGMA foreign_keys = ON")
        
# end create_db_connection()

# -----------------------------------------------------------------

def close_db() :
    """ Closes the database connection
    
        In:  nothing
        Out: nothing        
    """

    conn.close()
        
# end close_db()

# -----------------------------------------------------------------

def get_program_info(prog_name) :
    """ Get a program's info from the database

        In:  prog_name       - name of the program getting info for (string)
        Out: prog_desc       - program description (string)
             cmd_line_prefix - command line prefix (string)
    """

    cur = conn.cursor()

    cur.execute("""SELECT description, cmd_line_prefix 
                   FROM programs WHERE program_name = ?""", (prog_name,) )
    prog_info = cur.fetchall()

    prog_desc = ""
    cmd_line_prefix = ""
    
    if len(prog_info) > 0 :
        prog_desc  = prog_info[0][0]
        cmd_line_prefix = prog_info[0][1]
        
    return [prog_desc, cmd_line_prefix]

# end function: get_program_info

# -----------------------------------------------------------------

def get_cmd_line_prefix(prog_name) :
    """ Get a program's command line prefix from the database

        In:  prog_name       - name of the program getting timings for (string)
        Out: cmd_line_prefix - the program's command line prefix (string)
    """
    
    cur = conn.cursor()

    cur.execute("SELECT cmd_line_prefix FROM programs WHERE program_name = ?",
                (prog_name,) )
    data = cur.fetchall()

    cmd_line_prefix = ""
    if len(data) > 0 :
        cmd_line_prefix = data[0][0]
    
    return cmd_line_prefix

# end function: get_cmd_line_prefix

# -----------------------------------------------------------------

def get_programs() :
    """ Get all the programs from the database

        In:  nothing
        Out: prog_names        - retrieved program names (list)
             descriptions      - retrieved program descriptions (list)
             cmd_line_prefixes - retrieved command line prefixes (list)
        
        Exceptions generated:
            - dbe.DB_Error
    """

    try :
        cur = conn.cursor()
        cur.execute("SELECT program_name, description, cmd_line_prefix FROM programs")
    except sql.Error as e :
        raise dbe.DB_Error("Error getting programs from the database: get_programs()") from e

    progs  = cur.fetchall()

    prog_names        = []
    descriptions      = []
    cmd_line_prefixes = []
    
    for prog_info in progs :
        prog_names.append(prog_info[0])
        descriptions.append(prog_info[1])
        cmd_line_prefixes.append(prog_info[2])
        
    return [prog_names, descriptions, cmd_line_prefixes]

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

        In:  prog_name    - name of the program getting timings for (string)
        Out: prob_sizes   - all problem sizes for the program (list)
             timings      - all timings for the program (list)
    """
    
    cur = conn.cursor()

    cur.execute("SELECT problem_size, timing FROM timings WHERE program_name = ? ORDER BY problem_size ASC",
                (prog_name,) )
    timings_info = cur.fetchall()
    
    prob_sizes = []
    timings    = []

    # build up separate problem sizes and timings lists
    for [prob_size,timing] in timings_info :
        prob_sizes.append(prob_size)
        timings.append(timing)

    return [prob_sizes, timings]

# end function: get_timings

# -----------------------------------------------------------------

def add_timing(prog_name, prob_size, timing) :
    """ Add a program's timing for a problem size to the database

        In:  prog_name - name of the program getting timings for (string)
             prob_size - problem size (integer)
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

    # assumes database is properly set up for cascade deletion
    cur.execute("DELETE FROM timings WHERE program_name = ?",
                (prog_name,) )

    conn.commit()

# end function: delete_program_timings

# -----------------------------------------------------------------

