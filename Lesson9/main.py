# Algorithm timings for external programs
#
#    - displays algorithms in the database
#    - stores algorithms in the database: names, descriptions, external program name
#    - displays an algorithm's timings in the database
#    - generates/stores a timing for an algorithm; calls the associated external program with an inputted problem size
#                                                  (timing outputed to console by the external program);
#    - plots stored timings for algorithms (one plot can have multiple algorithms included)
#

import os
import sqlite3

# -----------------------------------------------------------------

def top_menu() :   
    """ Top menu of the pycnumanal application """

    while 1 :
        print("")
        print("(1) Display algorithms in database")
        print("(2) Input an algorithm into database")
        print("(3) Display timings for an algorithm")
        print("(4) Generate a timing for an algorithm")
        print("(5) Plot timings for an algorithm")
        print("")
  
        selection = raw_input("Enter selection (0 to exit) : ")

        if selection in ("0", "1", "2", "3", "4", "5") :
            return selection
        else : 
            continue

# end function: top_menu

# -----------------------------------------------------------------

def get_algorithms(conn) :
    """ Get all the algorithms from the database """

    cur = conn.cursor()  # database table cursor

    # get all algorithms in the database
    cur.execute("SELECT name, description, program FROM algorithms")    
    algs  = cur.fetchall()

    return algs

# end function: get_algorithms

# -----------------------------------------------------------------

def display_algorithms(algs) :   
    """ Display all the algorithms in the database """

    print
    print "\t\tAlgorithms in database"
    print
    print "\tName\t\t\tDescription"
    print "\t----\t\t\t-----------"

    k = 1
    for alg_info in algs :
        print str(k) + ") " + alg_info[0] + "\t\t" + alg_info[1]
        k = k + 1

    print

# end function: display_algorithms

# -----------------------------------------------------------------

def add_algorithm(conn) :   
    """ Add a new algorithm to the database """

    algs = get_algorithms(conn)
    display_algorithms(algs)

    # user inputs new algorithm info
    alg_name = raw_input("New algorithm name : ")
    alg_desc = raw_input("Description : ")
    alg_prog = raw_input("Program name (e.g. \"l2vecnorm\") : ")

    cur = conn.cursor()  # database table cursor

    # insert the new algorithm into algorithms table
    cur.execute("INSERT INTO algorithms (name, description, program) VALUES (?, ?, ?)",
                (alg_name, alg_desc, alg_prog) )

    conn.commit()

# end function: add_algorithm

# -----------------------------------------------------------------

def get_timings(conn, alg_name) :
    """ Get an algorithm's timings from the database """
    
    cur = conn.cursor()  # database table cursor

    # get an algorithm's timings from the database
    cur.execute("SELECT problem_size, time FROM timings WHERE algorithm = ? ORDER BY problem_size ASC",
                (alg_name,) )
    timings = cur.fetchall()

    return timings

# end function: get_timings

# -----------------------------------------------------------------

def display_timings(alg_name, timings) :   
    """ Display all of an algorithm's timings in the database """

    print
    print "\t\"" + alg_name + "\" timings in database"
    print
    print "Problem size\t\tTime"
    print "------------\t\t----"

    for timing_info in timings :
        print str(timing_info[0]) + "\t\t\t" + str(timing_info[1])

    print

# end function: display_timings

# -----------------------------------------------------------------

def add_timing(conn) :   
    """ Add a new timing for an algorithm """

    algs = get_algorithms( conn )
    display_algorithms( algs )

    alg_num = int( raw_input("Enter algorithm # to add a timing for (0 to exit) : "))
    if alg_num == 0 : return

    alg_info = algs[alg_num-1]
    alg_name = alg_info[0]
    timings  = get_timings(conn, alg_name)
    display_timings(alg_name, timings)
    
    # user inputs a new program size
    print
    prob_size = int( raw_input("New problem size (positive integer) : ") )

    # prepare OS command-line style command
    program = alg_info[2] 
    command_line = "./" + program + " " + str(prob_size)

    # call the external program; it is assumed that the external program
    # outputs only the timing in the first line of its console output
    retvalue = os.popen(command_line).readlines()
    timing   = float(retvalue[0].strip())
    print "Timing: ", timing

    cur = conn.cursor()  # database table cursor

    # insert the new timing into the timings table
    cur.execute("INSERT INTO timings (problem_size, time, algorithm) VALUES (?, ?, ?)",
                (prob_size, timing, alg_name) )

    conn.commit()

# end function: add_timing

# -----------------------------------------------------------------

# ===============================================================================================
#
#  Execution starts here
#

print
print os.getcwd()

db_filename     = 'timings.db'
schema_filename = 'schema.sql'

# does database file exist?
db_is_new = not os.path.exists(db_filename)

with sqlite3.connect(db_filename) as conn:
    if db_is_new:  # create the database file
        print 'Creating schema'
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)
    else:
        print 'Database exists, assume schema does, too.'

    while 1 :

        selection = top_menu()

        if   selection == "0" :
            print "0"
            exit()

        elif selection == "1" :  # display algorithms
            display_algorithms( get_algorithms(conn) )

        elif selection == "2" :  # add an algorithm
            add_algorithm(conn)

        elif selection == "3" :  # display an algorithm's timings
            algs = get_algorithms( conn )
            display_algorithms( algs )
            alg_num = int( raw_input("Enter algorithm # (0 to exit) : "))
            alg_name = algs[alg_num-1][0]
            timings = get_timings(conn, alg_name)
            display_timings(alg_name,timings)

        elif selection == "4" :  # add timings to an algorithm
            add_timing(conn)

        elif selection == "5" :  # plot timings
            print "5"

        else :
            print("Input error")
            exit()


