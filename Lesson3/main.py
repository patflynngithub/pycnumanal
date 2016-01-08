# main driver program in Python

import os

print os.getcwd()

retvalue = os.popen("./l2vecnorm 40000").readlines()

print retvalue

