# coding: utf-8
from pyo import *
from os import path
import csv
import sys

# Takes a csv file as input,
# asks if you want to use a column as x; if so which, asks which column to use as y
# Asks what size to use (defaults to 8192)
# computes a waveform from the CSV data, mapping the values to the right scale and
# Saves a file with pyo table data in.

# Function def
def yn_bool(string):
    if string[0] == 'y' or string[0] == 't' or string[0] == '1':
	return True
    else:
	return False


# Try to open file
file = open(sys.argv[1], 'rt')

# Using header row?
header_row = yn_bool(raw_input('First row is header? y/n >'))

if header_row != False:
    # Output column list
    head = csv.DictReader(file)
    print "Available Columns:\n"
    for (i, col) in enumerate(head.fieldnames):
	print str(i) + ": " + str(col)

# Using a col for x?
if yn_bool(raw_input('Use a column for x? y/n >')) == True:
    # We're using a column for x (instead of the array index). Query:
    x_col_index = int(raw_input('Which column to use for x axis? >'))
else:
    x_col_index = False

# Which col to use for y?
y_col_index = int(raw_input('Which column to use for y axis? >'))

# What size?
size = str(raw_input('How many samples in the table? Defaults to 8192 >'))
size = int(size) if len(size) != 0 else 8192

# What base (zero or -1)?
base = int(raw_input('What base? 0/-1 >'))
if base != 0 and base != -1:
    print "Bad base value, defaulting to zero"
    base = 0 # default to zero

# convert base to float
base = float(base)

# # # # Finished querying user, process

# Prepare vars for filling and iterating
samples = [];
i = 0

# Iterate over csv file
print "Iterating over CSV file..."
try:
    reader = csv.reader(file)
    for i,row in enumerate(reader):
	samples.append((int(row[x_col_index] if x_col_index != False else i), float(row[y_col_index])))
	i = i + 1
finally:
    file.close()

# Boot pyo server
print "Starting pyo server..."
s = Server().boot()

# Now samples is a list of x,y tuples.
# We need to map values of x between 0 and 'size' - 1, and values of y between 'base' and 1
# Find input min, max for x and y
x_in_min = int(min(samples, key=lambda x: x[0])[0])
x_in_max = int(max(samples, key=lambda x: x[0])[0])

y_in_min = float(min(samples, key=lambda x: x[1])[1])
y_in_max = float(max(samples, key=lambda x: x[1])[1])

# DEBUG
print x_in_min, x_in_max, y_in_min, y_in_max

mapped_points = []

for x, y in samples:
    # For each tuple, create a mapped tuple equivalent in mapped_points
    mapped_points.append((
	int(round(rescale(x, x_in_min, x_in_max, 0, size-1))),
	float(rescale(y, y_in_min, y_in_max, base, 1.))))

# 'mapped_points' is now a list of x,y tuples, mapped to the correct values for the final table
# Create a pyo table with the data, filled in by curves
table = CurveTable(mapped_points, size=size)

# Process
print "Normalizing..."
table.normalize()
print "Removing DC..."
table.removeDC()

# Save the table
basename = os.path.basename(file.name)
basename = os.path.splitext(basename)[0] # remove ext
basename = os.path.expanduser('~/' + basename + '_table.txt')

print "Saving to: " + basename

table.write(basename)


