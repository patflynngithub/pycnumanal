# Runs C algorithm for a problem size and stores timing in the database

import os
import sqlite3

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

    # setup for running external program (e.g., C program) to get timing
    name         = 'l2 vector norm'
    description  = 'l2 vector norm in C'
    command      = 'l2vecnorm'
    problem_size = 1000000
    command_line = "./" + command + " " + str(problem_size)

    # call the external program; it is assumed that the external program
    # outputs only the timing in the first line of console output
    retvalue = os.popen(command_line).readlines()
    timing = float(retvalue[0].strip())

    cur = conn.cursor()  # database table cursor

    # insert algorithm into algorithms table
    cur.execute("INSERT OR IGNORE INTO algorithms (name, description, command_line) VALUES (?, ?, ?)",
                (name, description, command) )

    # insert timing into timings table
    cur.execute("INSERT OR IGNORE INTO timings (problem_size, time, algorithm) VALUES (?, ?, ?)",
                (problem_size, timing, name) )

    conn.commit()

