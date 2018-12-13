# pycnumanal: Generate/Plot excution timings of external programs for different problem sizes
# 
#    VERSION 0.13
#
#    pyc:     Python/C program
#    numanal: timed numerical analysis routines written in C (could be other languages as well)
#
#    - adds programs to the database
#    - displays programs in the database
#    - manually add program timings to database
#    - generate/store timings for a program
#    - display a program's timings
#    - delete all of a program's timings
#    - plot timings for a program
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
#                      - reorganized version 0.10 functionalities into three files:
#                           - pycnumanal.py     ("core/controller")
#                           - database.py       ("model")
#                           - user_interface.py ("view")
#                      - added import statements to allow calling functions in other modules
#                      - now using the "conn" variable as a global variable in database.py
#                      - improved some commenting
#
#    12/08/2018 (pf)   Version 0.12:
#                      - added new functionalities to the overall application
#                          - manually enter in timings for a program
#                          - generate timings for a program
#                          - display timings for a program
#                      - added functions to support the new functionalities
#                          - get_timings()
#                          - add_timing()
#                          - generate_timing()
#                          - generate_and_add_timing()
#
#    12/09/2018 (pf)   Version 0.13:
#                      - added new functionality to the overall application
#                          - plot timings (vs problem size)
#
#    THIS CODE IS NOW pycnumanal VERSION, NOT pycnumanal-lessons VERSION
#
#    12/12/2018 (pf)   - added delete_program_timings()
#                      - professionalized the commenting
#                          - pycnumanal-lessons version has more commenting for the student
#
# (pf) Patrick Flynn
#
# ---------------------------------------------------------

#standard modules
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

def get_timings(prog_name) :
    """ Get a program's timings from the database

        In:  prog_name - name of the program getting timings for (string)
        Out: timings   - all timings for the given program (list of 2-tuples)
    """

    timings = db.get_timings(prog_name)
    
    return timings

# end function: get_timings

# -----------------------------------------------------------------

def delete_program_timings(prog_name) :
    """ Delete all of a program's timings

        In:  prog_name - program whose timings are to be deleted (string)
        Out: nothing
    """

    db.delete_program_timings(prog_name)
    
# end function: delete_program_timings

# -----------------------------------------------------------------

def add_timing(prog_name, prob_size, timing) :

    """ Add a program's timing to the database

        In:  prog_name - name of the program getting timings for (string)
             prob_size - problem size (integer)
             timing    - timing for problem size (float)
        Out: nothing
    """

    db.add_timing(prog_name, prob_size, timing)

# end function: add_timing

# -----------------------------------------------------------------
def generate_timing(prog_name, prob_size) :
    """ Generate a timing of a problem size for a program

        In:  prog_name - name of the program getting timings for (string)
             prob_size - problem size (integer)
        Out: timing    - timing for problem size (float)
    """

    cmd_line_prefix = db.get_cmd_line_prefix(prog_name)

    # prepare OS command-line style command that Python will use
    # to call the external program
    command_line = "./" + cmd_line_prefix + " " + str(prob_size)

    # call the external program; it is assumed that the external program
    # outputs only the timing in the first line of its console output
    retvalue = os.popen(command_line).readlines()
    timing   = float(retvalue[0].strip())
    
    return timing

# end function: generate_timing

# -----------------------------------------------------------------

def generate_and_add_timing(prog_name, prob_size) :
    """ Generate and add a program's timing to the database

        In:  prog_name - name of the program getting timings for (string)
             prob_size - problem size (integer)
        Out: timing    - timing for problem size (float)
    """
    
    timing = generate_timing(prog_name, prob_size)
    add_timing(prog_name, prob_size, timing)

    return timing
    
# end function: generate_and_add_timing

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
