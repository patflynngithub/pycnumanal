# pycnumanal: Generate/Plot excution timings of external programs for different problem sizes
# 
#     VERSION 0.11
#
#    pyc:     Python/C program
#    numanal: timed numerical analysis routines written in C (could be other languages as well)
#
#    - adds programs to the database: names, descriptions, command line names
#    - displays programs in the database
#
#    - runs on Linux (not tested on Windows)
#    - Python 3.x (not tested with Python 2.x)
#    - text-based interface
#    - SQlite (sqlite3) database used for storage
#    - very little error checking
#
# --------------------------------------------------------
#
# Change log:
#
#    12/06/2018 (pf)   Version 0.1:
#                      - first version of the pycnumanal program
#                      - implemented adding/displaying programs in the database
#
#    12/07/2018 (pf)   Version 0.11:
#                      - reorganized program functionalities into three modules:
#                           - pycnumanal     ("controller")
#                           - database       ("model")
#                           - user_interface ("view")
#                      - added application settings dictionary (config) that can 
#                        be passed between the modules
#
# (pf) Patrick Flynn
#
# ---------------------------------------------------------

#standard modules
import sys
import os

# custom modules
import database as db
import user_interface as ui

# -----------------------------------------------------------------

def get_programs(config) :
    """ Get all the programs from the database

        In:  conn  - programs/timings database connection
        Out: progs - all programs in database (list of tuples)
    """

    progs = db.get_programs(config["db_connection"])

    return progs

# end function: get_programs

# -----------------------------------------------------------------

def add_program(config, prog_name, prog_desc, cmd_line_name) :   
    """ Add a new program to the database

        In:  conn    - programs/timings database connection
        Out: nothing
    """

    db.add_program(config["db_connection"], prog_name, prog_desc, cmd_line_name)

# end function: add_program

# -----------------------------------------------------------------

# ===============================================================================================
#
#  Execution starts here
#

if __name__ == "__main__":

    print()
    print("working dirctory:", os.getcwd())

    # database setup
    db_filename     = 'timings.db'  # database of all programs and their timings
    schema_filename = 'schema.sql'  # structure of the programs/timings tables in the database
    
    conn = db.create_db_connection(db_filename, schema_filename)

    # the application's configuration settings stored in this dictionary
    config = {}
    config["db_connection"] = conn

    # start application's menuing system
    ui.top_menu(config)

# ===============================================================================================
