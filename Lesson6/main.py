# main driver program in Python

import os

print(os.getcwd())

external_command = "./l2vecnorm 40000"

# calls external program with program size and
# reads the returned timing value
ret_value = os.popen(external_command).readlines()

print(ret_value)

