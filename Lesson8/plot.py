# Plot timings in Python

import sys
import os
import sqlite3
import matplotlib.pyplot as plt

print os.getcwd()

db_filename     = 'timings.db'

# does database file exist?
db_exists = os.path.exists(db_filename)
if not db_exists:
    print "Timings database (" + db_filename + ") not found"
    exit()

with sqlite3.connect(db_filename) as conn:

    # setup for querying timings database for desired timings
    name         = 'l2 vector norm'

    cur = conn.cursor()  # database table cursor

#	select * from timings inner join algorithms on algorithms.name = timings.algorithm
#	where algorithms.name = 'l2 vector norm';

    # insert timing into timings table
    cur.execute("select problem_size, time from timings inner join algorithms on algorithms.name = timings.algorithm where algorithms.name = 'l2 vector norm'");

#    c.execute("SELECT * FROM {tn} WHERE {idf}={my_id}".\
#            format(tn=table_name, cn=column_2, idf=id_column, my_id=some_id))
    timings_info = cur.fetchall()
    print timings_info

    sizes   = [size[0]   for size   in timings_info]
    timings = [timing[1] for timing in timings_info]

    print sizes
    print timings

    plt.plot(sizes, timings)
    plt.xlabel('problem size')
    plt.ylabel('seconds')
    plt.show()

