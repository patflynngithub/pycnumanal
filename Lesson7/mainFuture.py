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

    c = conn.cursor()

    name = 'l2 vector norm'
    description = 'l2 vector norm in C'
    command = 'l2vecnorm'

    problem_size = 40000

    retvalue = os.popen("./l2vecnorm 40000").readlines()
    timing = float(retvalue[0].strip())

# c.execute("INSERT OR IGNORE INTO {tn} ({idf}, {cn}) VALUES (123456, 'test')".\
#        format(tn=table_name, idf=id_column, cn=column_name))

    alg_table = 'algorithms'

#c.execute("SELECT * FROM {tn} WHERE {idf}=?".\
#        format(tn=table_name, cn=column_2, idf=id_column), (123456,))

    c.execute("INSERT OR IGNORE INTO {at} (name, description, command_line) VALUES (?, ?, ?)".\
        format(at=alg_table), ( name, description, command,) )

#    c.execute("INSERT OR IGNORE INTO algorithms (name, description, command_line) VALUES (?, ?, ?)",
#              (name, description, command) )

    c.execute("INSERT OR IGNORE INTO timings (problem_size, time, algorithm) VALUES (?, ?, ?)",
              (problem_size, timing, name) )

#    conn.execute("""
#            insert into algorithms (name, description, command_line)
#            values ('l2 vector norm', 'l2 vector norm in C', 'l2vecnorm')
#            """)

#    conn.execute("""
#            insert into timings (problem_size, time, algorithm)
#            values (40000, 0.000451, 'l2 vector norm' )
#            """)

    conn.commit()

