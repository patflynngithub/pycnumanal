# user_interface.py: pycnumanal text-based user interface system
# 
#     VERSION 0.11
#
#    - text-based menus for:
#
#         - adding a program to the database
#         - displaying programs in the database
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
#    12/07/2018 (pf)   Version 0.11:
#                      - created this module as part of this version's
#                        "separating the concerns" of the core, database,
#                        and user_interface operations of pycnumanal version 0.10
#
# (pf) Patrick Flynn
#
# ---------------------------------------------------------

def top_menu() :
    """ Top text menu of the pycnumanal application

        In:  nothing
        Out: nothing
    """

    while 1 :
        print("")
        print("(1) Add a program to the database")
        print("(2) Display programs in the database")
        print("")
  
        selection = input("Enter selection number (0 to exit) : ")

        if selection == "0" :    # exit program
            print()
            return

        elif selection == "1" :  # add a program
            add_program()

        elif selection == "2" :  # display programs
            display_programs()

        else : 
            print("\nBAD ENTRY!")

# end function: top_menu

# -----------------------------------------------------------------

def get_programs() :
    """ Get all the programs from the database

        In:  nothing
        Out: progs - all programs in database (list of tuples)
    """

    progs = main.get_programs()

    return progs

# end function: get_programs

# -----------------------------------------------------------------

def display_programs() :   
    """ Displays all the programs in the database

        In:  nothing
        Out: progs - all programs in database (list of tuples)
    """

    # get all programs from database
    progs = get_programs()

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

def add_program() :
    """ Add a new program to the database

        In:  nothing
        Out: nothing
    """

    display_programs()
    print()
    
    # user inputs new program info
    prog_name       = input("New program name : ")
    prog_desc       = input("Description : ")
    cmd_line_prefix = input("Command line prefix (e.g. \"l2vecnorm\") : ")

    main.add_program(prog_name, prog_desc, cmd_line_prefix)

# end function: add_program

# -----------------------------------------------------------------

import pycnumanal as main

