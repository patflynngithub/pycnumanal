# pycnumanal: Algorithm timings for external programs
#
#    pyc:     Python/C program
#    numanal: timed numerical analysis routines written in C (could be other languages as well)
#
#    - displays algorithms in the database
#    - stores algorithms in the database: names, descriptions, external program name
#    - displays an algorithm's timings for different problem sizes in the database
#    - generates/stores algorithm timings for different problem sizes; 
#      (calls the associated external program with a user-specified problem size;)
#      (timing assumed outputted to console by the external program; only timing is on first line of output)
#    - plots the stored timings for algorithms (one plot can have multiple algorithms included)
#

# --------------------------------------------------------
#
# Change log:
#
#    08/20/2016    Version 1.0: (pf)
#                    - runs on Linux (not tested on Windows)
#                    - Python 2.7.x (not tested with Python 3)
#                    - text-based interface
#                    - SQlite (sqlite3) database used for storage
#                    - very little error checking
#
#    01/04/2017    - improved function documentation (In/Out for each function)
#
# (pf) Patrick Flynn
# (dh) Dan Hallman (done nothing at all)
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
        print("(1) Display algorithms in database")
        print("(2) Input an algorithm into database")
        print("(3) Display timings for an algorithm")
        print("(4) Generate a timing for an algorithm")
        print("(5) Plot timings for an algorithm")
        print("")
  
        selection = input("Enter selection (0 to exit) : ")

        if selection in ("0", "1", "2", "3", "4", "5") :
            return selection
        else : 
            print("BAD ENTRY!")
            continue

# end function: top_menu

# -----------------------------------------------------------------

def get_algorithms(conn) :
    """ Get all the algorithms from the database

        In:  conn - algorithms/timings database connection
        Out: algs - all algorithms in database (list of tuples)
    """

    cur = conn.cursor()  # database table cursor

    # get all algorithms in the database
    cur.execute("SELECT name, description, program FROM algorithms")    
    algs  = cur.fetchall()

    return algs

# end function: get_algorithms

# -----------------------------------------------------------------

def display_algorithms(algs) :   
    """ Display all the algorithms in the database

        In:  algs - all algorithms in database (list of tuples)
        Out: nothing
    """

    print
    print("\t\tAlgorithms in database")
    print
    print("    Name                 Description                    Program")
    print("    -------------------- ------------------------------ --------------------")

    k = 1
    for alg_info in algs :
        print("{:>2d}) {:<20s} {:<30s} {:<20s}".format(k, alg_info[0], alg_info[1], alg_info[2]))
        k = k + 1

    print

# end function: display_algorithms

# -----------------------------------------------------------------

def get_timings(conn, alg_name) :
    """ Get an algorithm's timings from the database

        In:  conn     - algorithms/timings database connection
             alg_name - name of algorithm getting timings for (string)
        Out: timings  - all timings for the given algorithm (list of tuples)
    """
    
    cur = conn.cursor()  # database table cursor

    # get an algorithm's timings from the database
    cur.execute("SELECT problem_size, time FROM timings WHERE algorithm = ? ORDER BY problem_size ASC",
                (alg_name,) )
    timings = cur.fetchall()

    return timings

# end function: get_timings

# -----------------------------------------------------------------

def display_timings(alg_name, timings) :   
    """ Display all of an algorithm's timings in the database

        In:  alg_name - name of algorithm displaying timings for (string)
             timings  - all timings for the given algorithm (list of tuples)
        Out: nothing
    """

    print
    print("     \"" + alg_name + "\" timings in database")
    print
    print("  Problem size        Time")
    print("  ------------   ---------------")

    for timing_info in timings :
        print("  {:>12d}   {:>15.6f}".format(timing_info[0], timing_info[1]))

    print        

# end function: display_timings

# -----------------------------------------------------------------

def do_display_algorithms(conn) :   
    """ Higher level process of displaying all the algorithms in the database

        In:  conn - algorithms/timings database connection
        Out: nothing
    """

    # get all algorithms from database
    algs = get_algorithms(conn)

    # check if any algorithms were found
    if len(algs) == 0 :
        print("\nNo algorithms in database")
        return
    
    # display all found algorithms
    display_algorithms(algs)

# end function: do_display_algorithms

# -----------------------------------------------------------------

def add_algorithm(conn) :   
    """ Add a new algorithm to the database

        In:  conn - algorithms/timings database connection
        Out: nothing
    """

    # display algorithms already in database
    algs = get_algorithms(conn)
    display_algorithms(algs)

    # user inputs new algorithm info
    alg_name = input("New algorithm name : ")
    alg_desc = input("Description : ")
    alg_prog = input("Program name (e.g. \"l2vecnorm\") : ")

    cur = conn.cursor()  # database table cursor

    # insert the new algorithm into algorithms table
    cur.execute("INSERT INTO algorithms (name, description, program) VALUES (?, ?, ?)",
                (alg_name, alg_desc, alg_prog) )

    # finalize the database data addition
    conn.commit()

# end function: add_algorithm

# -----------------------------------------------------------------

def do_display_timings(conn) :
    """ Higher level process of displaying all of an algorithm's timings

        In:  conn - algorithms/timings database connection
        Out: nothing
    """

    # get all algorithms from database
    algs = get_algorithms( conn )

    # check to see if any algorithms were found
    if len(algs) == 0 :
        print("\nNo algorithms in database")
        return

    # display the found algorithms
    display_algorithms( algs )

    # choose the algorithm to display timings for
    alg_num = int( input("Enter algorithm # (0 to return to menu) : "))
    if alg_num == 0 : return

    # get the chosen algorithm's timings
    alg_name = algs[alg_num-1][0]
    timings  = get_timings(conn, alg_name)

    # check if the chosen algorithm has any timings
    if len(timings) == 0 :
        print ("\nNo timings in database for " + alg_name + " \n")
        return

    # display the chosen algorithm's timings
    display_timings(alg_name,timings)

# end function: do_display_timings

# -----------------------------------------------------------------

def add_timing(conn) :   
    """ Add a new timing for an algorithm in the database

        In:  conn - algorithms/timings database connection
        Out: nothing
    """

    # get available algorithms
    algs = get_algorithms( conn )

    # check to see if any algorithms were found
    if len(algs) == 0 :
        print("\nNo algorithms in database")
        return

    display_algorithms( algs )

    # choose the algorithm to add timing for
    alg_num = int( input("Enter algorithm # to add a timing for (0 to return to menu) : "))
    if alg_num == 0 : return

    # extract desired algorithm information
    alg_info = algs[alg_num-1]
    alg_name = alg_info[0]
    program  = alg_info[2] 

    # display the algorithm's timings already in the database
    timings  = get_timings(conn, alg_name)
    display_timings(alg_name, timings)
    
    # user inputs a new program size for the algorithm
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
    cur.execute("INSERT INTO timings (problem_size, time, algorithm) VALUES (?, ?, ?)",
                (prob_size, timing, alg_name) )

    # finalize the database data addition
    conn.commit()

# end function: add_timing

# -----------------------------------------------------------------

def plot_timings(conn) :   
    """ Plot timings for an algorithm in the database

        In:  conn - algorithms/timings database connection
        Out: nothing
    """

    # display available algorithms
    algs = get_algorithms(conn)
    if len(algs) == 0 :
        print("\nNo algorithms in database\n")
        return
    display_algorithms(algs)

    # choose the algorithms to plot
    alg_nums = []
    while 1 :
        alg_num = int( input("Enter algorithm # to plot timings for (0 to stop entering #'s) : ") )
        if alg_num == 0 : break
        alg_nums.append(alg_num)

    cur = conn.cursor()  # database table cursor

    # start up the plot
    fig = plt.figure()
    fig.canvas.set_window_title('Timing vs Problem size') 

    # plot each algorithm's timings by looping through
    # the chosen algorithms
    alg_names = []
    for alg_num in alg_nums :

        # get current algorithm's info
        alg_info = algs[alg_num-1]
        alg_name = alg_info[0]
 
        # get current algorithm's timings from timings table
        cur.execute("SELECT problem_size, time FROM timings " +
                    "INNER JOIN algorithms ON algorithms.name = timings.algorithm WHERE algorithms.name = ? " + 
                    "ORDER BY problem_size ASC", (alg_name,))
        timings = cur.fetchall() 

        # check if current algorithm has any timings
        if len(timings) == 0 :  # no timings were found for current algorithm
            print("\nNo timings in database for " + alg_name + " algorithm\n")
            return

        # add current algorithm's name to the list of chosen algorithms that timings were found for
        alg_names.append(alg_name)

        # organize current algorithm's timings info for plotting
        sizes   = [timing[0] for timing in timings]
        timings = [timing[1] for timing in timings]

        # plot the current algorithm's timings
        plt.plot(sizes, timings)

    # add overall plotting embellishments 
    plt.xlabel('problem size')
    plt.ylabel('seconds')
    plt.title("Timing vs Problem Size")
    plt.legend(alg_names)
    plt.show()

# end function: plot_timings

# -----------------------------------------------------------------

# ===============================================================================================
#
#  Execution starts here
#

# database info
db_filename     = 'timings.db'  # database of all algorithms and their timings
schema_filename = 'schema.sql'  # structure of the algorithms/timings tables in the database

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

        elif selection == "1" :  # display algorithms
            do_display_algorithms(conn)

        elif selection == "2" :  # add an algorithm
            add_algorithm(conn)

        elif selection == "3" :  # display an algorithm's timings
            do_display_timings(conn)

        elif selection == "4" :  # add a timing for an algorithm
            add_timing(conn)

        elif selection == "5" :  # plot timings for one or more algorithms
            plot_timings(conn)

        else :                   # unexpected menu input
            print("\nInput error\n")

# end program

# ===============================================================================================

