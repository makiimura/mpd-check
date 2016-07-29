# import argparse

import argparse

#
#   Howto run test program
#
#   python arg_test.py --in something --out something



# Create parser object for parsing incoming arguments

parser = argparse.ArgumentParser()

# Add arguments that we want to parse
parser.add_argument('--in', action="store", dest='inputFileName')
parser.add_argument('--out', action='store', dest='outputFileName')

# We add 2 arguments --in and --out
# action=store means, we want to store the values to somewhere to use later
# dest=variable_name means, we want to store any value that follow --in (or --out) to this variable


# parsing argument, the values will be store inside 'arguments' variable
arguments = parser.parse_args()


# print 'inputFileName' that we defined and store from above
print arguments.inputFileName

# print 'outputFileName' that we defined and store from above
print arguments.outputFileName

