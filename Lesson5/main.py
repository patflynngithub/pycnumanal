# main driver program in Python

import os

print os.getcwd()

external_command = "./l2vecnorm 40000"
ret_value = os.popen(external_command).readlines()

print ret_value
