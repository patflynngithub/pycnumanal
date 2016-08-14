# Plot timings in Python

import sys
import os
import sqlite3
import matplotlib.pyplot as plt

print os.getcwd()  # current working directory

db_filename     = 'timings.db'

# does database file exist?
db_exists = os.path.exists(db_filename)
if not db_exists:
    print "Timings database (" + db_filename + ") not found"
    exit()

with sqlite3.connect(db_filename) as conn:

    # setup for querying timings database for desired timings
    alg_name         = 'l2 vector norm'
    description  = 'l2 vector norm in C'
    command      = 'l2vecnorm'
    cur = conn.cursor()  # database table cursor

    # extract desired timings from timings table
    cur.execute("SELECT problem_size, time FROM timings " +
                "INNER JOIN algorithms ON algorithms.name = timings.algorithm WHERE algorithms.name = ? " + 
                "ORDER BY problem_size ASC", (alg_name,))
    timings_info = cur.fetchall() 

    print timings_info

    # organize timings info for plotting
    sizes   = [timing[0] for timing in timings_info]
    timings = [timing[1] for timing in timings_info]

    print sizes
    print timings

    # plot the timings
    fig = plt.figure()
    fig.canvas.set_window_title('Timing vs Problem size') 
    plt.plot(sizes, timings)
    plt.xlabel('problem size')
    plt.ylabel('seconds')
    plt.title("Timings for " + description)
    plt.figtext(0.99, 0.01, command, horizontalalignment='right')
    plt.show()
