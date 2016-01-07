# main driver program in Python
# will call l2vecnorm.c

import os

print os.getcwd()

retvalue = os.popen("./l2vecnorm 40000").readlines()

print retvalue

