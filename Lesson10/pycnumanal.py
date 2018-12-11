# pycnumanal: Generate/Plot excution timings of external programs for different problem sizes. This timing info
#             is stored in a database
# 
#     VERSION 0.11
#
#    pyc:     Python/C program
#    numanal: timed numerical analysis routines written in C (could be other languages as well)
#
#    - adds programs to the database
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
#    12/06/2018 (pf)   Version 0.10:
#                      - first version of the pycnumanal program
#                      - implemented adding/displaying programs in the database
#
#    12/07/2018 (pf)   Version 0.11:
#                      - reorganized version 0.10 general functionalities into three modules (files):
#                           - pycnumanal.py     ("core/controller")
#                           - database.py       ("model")
#                           - user_interface.py ("view")
#                      - now using the "conn" variable as a global variable in database.py
#                      - improved some commenting
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

def get_programs() :
    """ Get all the programs from the database

        In:  nothing
        Out: progs - all programs in database (list of tuples)
    """

    progs = db.get_programs()

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

    db.add_program(prog_name, prog_desc, cmd_line_prefix)

# end function: add_program

# -----------------------------------------------------------------

# ===============================================================================================
#
#  Execution starts here
#

if __name__ == "__main__":

    print()
    print("working dirctory:", os.getcwd())

    # database setup info
    db_filename     = 'timings.db'  # database of all programs and their timings
    schema_filename = 'schema.sql'  # setup script for the programs/timings tables in the database
    
    db.create_db_connection(db_filename, schema_filename)

    # start application's menuing system
    ui.top_menu()

# ===============================================================================================

