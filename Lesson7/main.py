# Runs a C algorithm for a problem size and stores its timing in the database

import os
import sqlite3

print(os.getcwd())

db_filename     = 'timings.db'
schema_filename = 'schema.sql'

# does database file exist?
db_is_new = not os.path.exists(db_filename)

with sqlite3.connect(db_filename) as conn:
    if db_is_new:  # create the database file and setup the tables
        print('Creating schema')
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)
    else:
        print('Database exists, assume schema does too.')

    # setup for running external program (e.g., C program) to get timing
    program_name  = 'l2 vector norm'
    description   = 'l2 vector norm in C'
    cmd_line_name = 'l2vecnorm'
    problem_size  = 1000000
    command_line  = "./" + cmd_line_name + " " + str(problem_size)

    # call the external program; it is assumed that the external program
    # outputs only the timing in its first line of console output
    retvalue = os.popen(command_line).readlines()
    timing   = float(retvalue[0].strip())

    cur = conn.cursor()  # database table cursor

    # insert external program into programs table
    cur.execute("INSERT OR IGNORE INTO programs (program_name, description, cmd_line_name) VALUES (?, ?, ?)",
                (program_name, description, cmd_line_name) )
    print('Inserted program into programs table')

    # insert timing into timings table
    cur.execute("INSERT OR IGNORE INTO timings (problem_size, timing, program_name) VALUES (?, ?, ?)",
                (problem_size, timing, program_name) )
    print('Inserted timing into timings table')

    conn.commit()

