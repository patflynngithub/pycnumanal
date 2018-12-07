# pycnumanal: Excution timings for external programs with different problem sizes
#
#    pyc:     Python/C program
#    numanal: timed numerical analysis routines written in C (could be other languages as well)
#
#    - displays programs in the database
#    - stores programs in the database: names, descriptions, external program name
#    - displays a program's timings for different problem sizes in the database
#    - generates/stores program timings for different problem sizes; 
#      (calls the associated external program with a user-specified problem size;)
#      (timing assumed outputted to console by the external program; only timing is on first line of output)
#    - plots the stored timings for programs (one plot can have multiple programs included)
#

# --------------------------------------------------------
#
# Change log:
#
#    11/25/2018 (pf)   Version 1.0:
#                      - runs on Linux (not tested on Windows)
#                      - Python 3.x (not tested with Python 2.x)
#                      - text-based interface
#                      - SQlite (sqlite3) database used for storage
#                      - very little error checking
#
#
# (pf) Patrick Flynn
#
# ---------------------------------------------------------

import sys
import os
import sqlite3
import matplotlib.pyplot as plt

# -----------------------------------------------------------------

def top_menu() :   
    """ Top menu of the pycnumanal application

        In:  nothing 
        Out: menu selection (string)
    """

    while 1 :
        print("")
        print("(1) Display programs in database")
        print("(2) Input a program into database")
        print("(3) Display timings for a program")
        print("(4) Generate a timing for a program")
        print("(5) Plot timings for a program")
        print("")
  
        selection = input("Enter selection (0 to exit) : ")

        if selection in ("0", "1", "2", "3", "4", "5") :
            return selection
        else : 
            print("BAD ENTRY!")
            continue

# end function: top_menu

# -----------------------------------------------------------------

def get_programs(conn) :
    """ Get all the programs from the database

        In:  conn  - timings database connection
        Out: progs - all programs in database (list of tuples)
    """

    cur = conn.cursor()  # database table cursor

    # get all programs in the database
    cur.execute("SELECT program_name, description, cmd_line_name FROM programs")    
    progs  = cur.fetchall()

    return progs

# end function: get_programs

# -----------------------------------------------------------------

def display_programs(progs) :   
    """ Display all the programs in the database

        In:  progs - all programs in database (list of 3-tuples)
        Out: nothing
    """

    print
    print("\t\tPrograms in database")
    print
    print("    Name                 Description                    Program")
    print("    -------------------- ------------------------------ --------------------")

    k = 1
    for prog_info in progs :
        print("{:>2d}) {:<20s} {:<30s} {:<20s}".format(k, prog_info[0], prog_info[1], prog_info[2]))
        k = k + 1

    print

# end function: display_programs

# -----------------------------------------------------------------

def get_timings(conn, prog_name) :
    """ Get a program's timings from the database

        In:  conn      - timings database connection
             prog_name - name of the program getting timings for (string)
        Out: timings   - all timings for the given program (list of 2-tuples)
    """
    
    cur = conn.cursor()  # database table cursor

    # get a program's timings from the database
    cur.execute("SELECT problem_size, timing FROM timings WHERE program_name = ? ORDER BY problem_size ASC",
                (prog_name,) )
    timings = cur.fetchall()

    return timings

# end function: get_timings

# -----------------------------------------------------------------

def display_timings(prog_name, timings) :   
    """ Display all of a program's timings in the database

        In:  prog_name - name of the program displaying timings for (string)
             timings   - all timings for the given program (list of tuples)
        Out: nothing
    """

    print
    print("     \"" + prog_name + "\" timings in database")
    print
    print("  Problem size        Time")
    print("  ------------   ---------------")

    for timing_info in timings :
        print("  {:>12d}   {:>15.6f}".format(timing_info[0], timing_info[1]))

    print        

# end function: display_timings

# -----------------------------------------------------------------

def do_display_programs(conn) :   
    """ Manages the steps of displaying all the programs in the database

        In:  conn - programs/timings database connection
        Out: nothing
    """

    # get all programs from database
    progs = get_programs(conn)

    # check if any programs were found
    if len(progs) == 0 :
        print("\nNo programs in database")
        return
    
    # display all found programs
    display_programs(progs)

# end function: do_display_programs

# -----------------------------------------------------------------

def add_program(conn) :   
    """ Add a new program to the database

        In:  conn - programs/timings database connection
        Out: nothing
    """

    # display programs already in database
    progs = get_programs(conn)
    display_programs(progs)

    # user inputs new program info
    prog_name     = input("New program name : ")
    prog_desc     = input("Description : ")
    cmd_line_name = input("Command line name (e.g. \"l2vecnorm\") : ")

    cur = conn.cursor()  # database table cursor

    # insert the new program into programs table
    cur.execute("INSERT INTO programs (program_name, description, cmd_line_name) VALUES (?, ?, ?)",
                (prog_name, prog_desc, prog_prog) )

    # finalize the database data addition
    conn.commit()

# end function: add_program

# -----------------------------------------------------------------

def do_display_timings(conn) :
    """ Higher level process of displaying all of a program's timings

        In:  conn - programs/timings database connection
        Out: nothing
    """

    # get all programs from database
    progs = get_programs( conn )

    # check to see if any programs were found
    if len(progs) == 0 :
        print("\nNo programs in database")
        return

    # display the found programs
    display_programs( progs )

    # choose the program to display timings for
    prog_num = int( input("Enter program # (0 to return to menu) : "))
    if prog_num == 0 : return

    # get the chosen program's timings
    prog_name = progs[prog_num-1][0]
    timings  = get_timings(conn, prog_name)

    # check if the chosen program has any timings
    if len(timings) == 0 :
        print ("\nNo timings in database for " + prog_name + " \n")
        return

    # display the chosen program's timings
    display_timings(prog_name,timings)

# end function: do_display_timings

# -----------------------------------------------------------------

def add_timing(conn) :   
    """ Add a new timing for a program in the database

        In:  conn - programs/timings database connection
        Out: nothing
    """

    # get programs in the database
    progs = get_programs( conn )

    # check to see if any programs were found
    if len(progs) == 0 :
        print("\nNo programs in database")
        return

    display_programs( progs )

    # choose the program to add timing for
    prog_num = int( input("Enter program # to add a timing for (0 to return to menu) : "))
    if prog_num == 0 : return

    # extract desired program information
    prog_info = progs[prog_num-1]
    prog_name = prog_info[0]
    program  = prog_info[2] 

    # display the program's timings already in the database
    timings  = get_timings(conn, prog_name)
    display_timings(prog_name, timings)
    
    # user inputs a new program size for the program
    print
    prob_size = int( input("New problem size (positive integer) : ") )

    # prepare OS command-line style command
    command_line = "./" + program + " " + str(prob_size)

    # call the external program; it is assumed that the external program
    # outputs only the timing in the first line of its console output
    retvalue = os.popen(command_line).readlines()
    timing   = float(retvalue[0].strip())
    print("Timing: ", timing)

    # get database table cursor
    cur = conn.cursor()  

    # insert the new timing into the timings table
    cur.execute("INSERT INTO timings (problem_size, timing, program_name) VALUES (?, ?, ?)",
                (prob_size, timing, prog_name) )

    # finalize the database data addition
    conn.commit()

# end function: add_timing

# -----------------------------------------------------------------

def plot_timings(conn) :   
    """ Plot timings for a program in the database

        In:  conn - programs/timings database connection
        Out: nothing
    """

    # display available programs
    progs = get_programs(conn)
    if len(progs) == 0 :
        print("\nNo programs in database")
        return
    display_programs(progs)

    # choose the programs to plot
    prog_nums = []
    while 1 :
        prog_num = int( input("Enter program # to plot timings for (0 to stop entering #'s) : ") )
        if prog_num == 0 : break
        prog_nums.append(prog_num)

    cur = conn.cursor()  # database table cursor

    # start up the plot
    fig = plt.figure()
    fig.canvas.set_window_title('Timing vs Problem size') 

    # plot each program's timings by looping through
    # the chosen programs
    prog_names = []
    for prog_num in prog_nums :

        # get current program's info
        prog_info = progs[prog_num-1]
        prog_name = prog_info[0]
 
        # get current program's timings from timings table
        cur.execute("SELECT problem_size, timing FROM timings " +
                    "INNER JOIN programs ON programs.program_name = timings.program_name " + 
                    "WHERE programs.program_name = ? ORDER BY problem_size ASC", (prog_name,))
        timings = cur.fetchall() 

        # check if current program has any timings
        if len(timings) == 0 :  # no timings were found for current program
            print("\nNo timings in database for " + prog_name + " program\n")
            return

        # add current program's name to the list of chosen programs that timings were found for
        prog_names.append(prog_name)

        # organize current program's timings info for plotting
        sizes   = [timing[0] for timing in timings]
        timings = [timing[1] for timing in timings]

        # plot the current program's timings
        plt.plot(sizes, timings)

    # add overall plotting embellishments 
    plt.xlabel('problem size')
    plt.ylabel('seconds')
    plt.title("Timing vs Problem Size")
    plt.legend(prog_names)
    plt.show()

# end function: plot_timings

# -----------------------------------------------------------------

# ===============================================================================================
#
#  Execution starts here
#

# database info
db_filename     = 'timings.db'  # database of all programs and their timings
schema_filename = 'schema.sql'  # structure of the programs/timings tables in the database

# does database file exist in current working directory?
print
print(os.getcwd())
db_is_new = not os.path.exists(db_filename)

# setup connection to the database
with sqlite3.connect(db_filename) as conn:  # database created if it doesn't exist yet

    if db_is_new :  # create the tables in the database
        print('Creating schema')
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)

    else :  # database file already exists
        print('Database exists, assuming schema does, too.')

    # the top menu loop
    while 1 :

        selection = top_menu()   # selected action from the menu

        if   selection == "0" :  # exit program
            print
            exit()

        elif selection == "1" :  # display programs
            do_display_programs(conn)

        elif selection == "2" :  # add a program
            add_program(conn)

        elif selection == "3" :  # display a program's timings
            do_display_timings(conn)

        elif selection == "4" :  # add a timing for a program
            add_timing(conn)

        elif selection == "5" :  # plot timings for one or more programs
            plot_timings(conn)

        else :                   # unexpected menu input
            print("\nInput error\n")

# end program

# ===============================================================================================

