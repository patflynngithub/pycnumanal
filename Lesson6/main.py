# main driver program in Python

import os
import sqlite3

print os.getcwd()

db_filename = 'timings.db'
schema_filename = 'schema.sql'

db_is_new = not os.path.exists(db_filename)

with sqlite3.connect(db_filename) as conn:
    if db_is_new:
        print 'Creating schema'
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)

    else:
        print 'Database exists, assume schema does, too.'


    retvalue = os.popen("./l2vecnorm 40000").readlines()
    timing = float(retvalue[0].strip())

    conn.execute("""
            insert into algorithm (name, description, command_line)
            values ('l2 vector norm', 'l2 vector norm in C', 'l2vecnorm')
            """)

    conn.execute("""
            insert into timings (problem_size, time, algorithm)
            values (40000, 0.000451, 'l2 vector norm' )
            """)

    conn.commit()

