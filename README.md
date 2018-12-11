Application: pycnumanal  (python/C numerical analysis)

A Python program that, choosing from a collection of C numerical routines (or algorithms), calls one of them with a user-specified problem size (n). The C code outputs the time required to run with that problem size. The Python program stores these timings in a database, allowing it to later display graphical plots of the timings (seconds) vs. problem sizes (n). It supports displaying the timing curves of multiple programs on the same plot for comparison purposes.

See syllabus.doc for more details.

NOTE: while the code here contains much of my "good" programming habits and design philosophy, there are elements of the code that were designed to support the learning process for a less experienced programmer. For example, while I do not comment code lightly, there is more commenting in this code than I would normally do. Also, some of the structural decisions/implementations were done in away so as to make it easier for the learner to follow.

