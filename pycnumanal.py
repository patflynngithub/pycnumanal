# pycnumanal: Generate/Plot excution timings of external programs for different problem sizes
# 
#    VERSION 1.00
#
#    pyc:     Python/C program
#    numanal: timed numerical analysis routines written in C (could be other languages as well)
#
#    - adds program to the database
#    - delete a program from the database (and its timings)
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
#    12/20/2018 (pf)   - added delete_program()
#
#    12/22/2018 (pf)   - added get_cmd_line_prefix()
#
#    12/27/2018 (pf)   - added get_program_info_from_DB()
#
#    12/29/2018 (pf)   - changed name of get_program_info_from_DB() to get_program_info()
#                      - modified get_program_info()
#                           - accomodates modifications to db.get_program_info()
#                               - data is returned with each field's values having their own separate list
#                                 rather than each data row having its own list, which is inside of the overall list
#                               - avoids calling functions in other modules having to know the order (list indices)
#                                 of entries in a list inside of an overall list
#
#    12/30/2018 (pf)   - modified get_programs()     (and db.get_programs())
#                                 get_timings()      (and db.get_timings())
#                           - accomodates modifications to db.get_programs() and db.get_timings()
#                               - data is returned with each field's values having their own separate list
#                                 rather than each data row having its own list, which is inside of the overall list
#                               - avoids calling functions in other modules having to know the order (list indices)
#                                 of entries in a list inside of an overall list
#                      - modified intial execution section
#                          - added call to db.close_db()
#
#    12/31/2018 (pf)   - RELEASING AS VERSION 1.0
#
# (pf) Patrick Flynn
#
# ---------------------------------------------------------

# standard modules
import os

# custom modules
import database as db
import user_interface as ui

# -----------------------------------------------------------------

def get_program_info(prog_name) :
    """ Get a program's info from the database

        In:  prog_name       - name of the program getting info for (string)
        Out: prog_desc       - program description (string)
             cmd_line_prefix - command line prefix (string)
    """

    [prog_desc, cmd_line_prefix] = db.get_program_info(prog_name)
    
    return [prog_desc, cmd_line_prefix]

# end function: get_program_info

# -----------------------------------------------------------------

def get_cmd_line_prefix(prog_name) :
    """ Get a program's command line prefix from the database

        In:  prog_name       - name of the program getting timings for (string)
        Out: cmd_line_prefix - the program's command line prefix (string)
    """

    cmd_line_prefix = db.get_cmd_line_prefix(prog_name)
    
    return cmd_line_prefix

# end function: get_cmd_line_prefix

# -----------------------------------------------------------------

def get_programs() :
    """ Get all the programs from the database

        In:  nothing
        Out: prog_names        - program names (list)
             descriptions      - program descriptions (list)
             cmd_line_prefixes - command line prefixes (list)        
    """

    [prog_names, descriptions, cmd_line_prefixes] = db.get_programs()

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

    db.add_program(prog_name, prog_desc, cmd_line_prefix)

# end function: add_program

# -----------------------------------------------------------------

def delete_program(prog_name) :   
    """ Delete a program from the database

        In:  prog_name       - program name (string)
        Out: nothing
    """

    db.delete_program(prog_name)

# end function: delete_program

# -----------------------------------------------------------------

def get_timings(prog_name) :
    """ Get a program's timings from the database

        In:  prog_name   - name of the program getting timings for (string)
        Out: prob_sizes  - all problem sizes for the program (list)
             timings     - all timings for the program (list)
   """

    [prob_sizes, timings] = db.get_timings(prog_name)
    
    return [prob_sizes, timings]

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
#  Initial execution starts here
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
    
    db.close_db()

# ===============================================================================================
