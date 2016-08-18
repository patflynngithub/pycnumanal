# Algorithm timings for external programs
#
#    - stores algorithms: names, descriptions, external program name
#    - calls the external programs with problem sizes (timings returned by the external programs);
#      stores the timings
#    - plots stored timings for algorithms (one plot can have multiple algorithms included)
#

import os
import sqlite3

# -----------------------------------------------------------------

def top_menu() :   
    """Top menu of the pycnumanal application"""

    while 1 :
        print("")
        print("(1) Input algorithm into database")
        print("(2) Generate timings for an algorithm")
        print("(3) Plot timings for an algorithm")
        print("")
  
        selection = raw_input("Enter selection (0 to exit) : ")

        if selection in ("0", "1", "2", "3") :
            return selection
        else : 
            continue

# end function: top_menu

# -----------------------------------------------------------------

def add_algorithm(conn) :   
    """Add a new algorithm to the database"""

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

def add_timing(conn) :   
    """Add a new timing to the database"""
    
    # user inputs algorithm name and program size
    alg_name  = raw_input("Algorithm name : ")
    prob_size = int( raw_input("New problem size (positive integer) : ") )

    cur = conn.cursor()  # database table cursor

    # extract corresponding program name from algorithms table
    cur.execute("SELECT program FROM algorithms " +
                "WHERE algorithms.name = ? ", (alg_name,))    
    record  = cur.fetchone()
    program = record[0]
    print "Program name fetched from database : ", program

    # prepare OS command-line style command
    command_line = "./" + program + " " + str(prob_size)

    # call the external program; it is assumed that the external program
    # outputs only the timing in the first line of its console output
    retvalue = os.popen(command_line).readlines()
    timing   = float(retvalue[0].strip())
    print "Timing: ", timing

    # insert the new timing into timings table
    cur.execute("INSERT INTO timings (problem_size, time, algorithm) VALUES (?, ?, ?)",
                (prob_size, timing, alg_name) )

    conn.commit()

# end function: add_timing

# -----------------------------------------------------------------

# ===============================================================================================
#
#  Execution starts here
#

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

    selection = top_menu()
    print (selection)

    if   selection == "0" :
        print "0"
        exit()

    elif selection == "1" :
        add_algorithm(conn)

    elif selection == "2" :
        add_timing(conn)

    elif selection == "3" :
        print "3"

    else :
        print("Input error")
        exit()

