# user_interface.py: pycnumanal text-based user interface system
# 
#     VERSION 0.11
#
#    - menus for:
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
#    12/06/2018 (pf)   Version 0.11:
#                      - implemented adding/displaying programs in the database
#
# (pf) Patrick Flynn
#
# ---------------------------------------------------------

def top_menu(conn) :
    """ Top text menu of the pycnumanal application

        In:  conn    - programs/timings database connection
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

        In:  conn  - programs/timings database connection
        Out: progs - all programs in database (list of tuples)
    """

    progs = main.get_programs(conn)

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

        In:  conn    - programs/timings database connection
        Out: nothing
    """

    display_programs(conn)
    print()
    
    # user inputs new program info
    prog_name     = input("New program name : ")
    prog_desc     = input("Description : ")
    cmd_line_name = input("Command line name (e.g. \"l2vecnorm\") : ")

    main.add_program(conn, prog_name, prog_desc, cmd_line_name)

# end function: add_program

# -----------------------------------------------------------------

import pycnumanal as main
