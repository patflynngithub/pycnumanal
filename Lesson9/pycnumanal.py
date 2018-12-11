# pycnumanal: Generate/Plot excution timings of external programs for different problem sizes
# 
#     VERSION 0.10
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
#                      - implemented adding/displaying programs in the database
#
# (pf) Patrick Flynn
#
# ---------------------------------------------------------

import sys
import os
import sqlite3

# -----------------------------------------------------------------

def top_menu(conn) :   
    """ Top text menu of the pycnumanal application

        In:  conn  - timings database connection
        Out: nothing
    """

    while 1 :
        print("")
        print("(1) Add a program to the database")
        print("(2) Display programs in the database")
        print("")
  
        selection = input("Enter selection number (0 to exit) : ")

        if selection == "0" :    # exit program
            return

        elif selection == "1" :  # add a program
            add_program(conn)

        elif selection == "2" :  # display programs
            display_programs(conn)

        else : 
            print("\nBAD ENTRY!")

# end function: top_menu

# -----------------------------------------------------------------

def get_programs(conn) :
    """ Get all the programs from the database

        In:  conn  - timings database connection
        Out: progs - all programs in database (list of tuples)
    """

    cur = conn.cursor()  # database table cursor

    # get all programs in the database
    cur.execute("SELECT program_name, description, cmd_line_prefix FROM programs")    
    progs  = cur.fetchall()

    return progs

# end function: get_programs

# -----------------------------------------------------------------

def display_programs(conn) :   
    """ Displays all the programs in the database

        In:  conn  - programs/timings database connection
        Out: progs - all programs in database (list of 3-tuples)
    """

    # get all programs from database
    progs = get_programs(conn)

    print()
    # check if any programs were found
    if len(progs) == 0 :
        print("No programs in database")
    else : # display all found programs
        print
        print("\t\tPrograms in database")
        print()
        print("    Name                 Description                    Program")
        print("    -------------------- ------------------------------ --------------------")

        k = 1
        for prog_info in progs :
            print("{:>2d}) {:<20s} {:<30s} {:<20s}".format(k, prog_info[0], prog_info[1], prog_info[2]))
            k = k + 1

        print

    return progs

# end function: display_programs

# -----------------------------------------------------------------

def add_program(conn) :   
    """ Add a new program to the database

        In:  conn - programs/timings database connection
        Out: nothing
    """

    display_programs(conn)
    print()
    
    # user inputs new program info
    prog_name       = input("New program name : ")
    prog_desc       = input("Description : ")
    cmd_line_prefix = input("Command line prefix (e.g. \"l2vecnorm\") : ")

    cur = conn.cursor()  # database table cursor

    # insert the new program into programs table
    cur.execute("INSERT INTO programs (program_name, description, cmd_line_prefix) VALUES (?, ?, ?)",
                (prog_name, prog_desc, cmd_line_prefix) )

    # finalize the database data addition
    conn.commit()

# end function: add_program

# -----------------------------------------------------------------

# ===============================================================================================
#
#  Execution starts here
#

# database info
db_filename     = 'timings.db'  # database of all programs and their timings
schema_filename = 'schema.sql'  # structure of the programs/timings tables in the database

# does the database file exist in the current working directory?
print
print(os.getcwd())
db_is_new = not os.path.exists(db_filename)

# setup connection to the database
with sqlite3.connect(db_filename) as conn:  # "connect" creates the database if it doesn't yet exist

    if db_is_new :  # create the tables if the database is newly created
        print('Creating database')
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)

    else :  # database file already exists
        print('Database exists, assuming contains proper table structure.')
    
    # start application's menuing system
    top_menu(conn)
    print()

# end program

# ===============================================================================================

