# Python user-defined database exceptions
# 
# Intended to be database exceptions that are independent
# of the specific database being used. I call them "agnostic"
# database exceptions. When a SQL command generates an exception
# proprietary to the underlying databse being used, one of the
# "agnostic" exceptions is substituted for the particular
# database's exception.
#
# For example, when SQLite is being used and SQL commands
# are only executed in a special database module (e.g., database.py),
# if Python SQLite generates an exception, one of the below
# "agnostic" exceptions, would be substitued for it
# and passed on.
# This would allow another database to be more easily
# substituted for SQLite. One would only need to make
# changes to the SQLite exceptions in the special database
# module (e.g., database.py) and no changes would need to be
# made to the to the "agnostic" database exceptions used in
# other modules of the application.
#
# --------------------------------------------------------
#
# Change log:
#
#
#    12/22/2018 (pf)   - created for handling database exceptions in
#                        the pycnumanal application
#
# (pf) Patrick Flynn
#
# ---------------------------------------------------------

class DB_Error(Exception):
   """Base class for "agnostic" database exceptions"""
   pass
