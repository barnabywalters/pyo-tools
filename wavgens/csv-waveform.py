# coding: utf-8
from pyo import *
from os import path
import csv
import sys

# Takes a csv file as input,
# asks which columns to use as x and y,
# computes a waveform from the CSV data,
# Saves a file with pyo table data in.

# Try to open file
file = open(sys.argv[1], 'rt')

# Check for header row
header_row = bool(raw_input('First row is header? 0/1 >'))

if header_row != False:
    # Output column list
    head = csv.DictReader(file)
    print "Available Columns:\n"
    for (i, col) in enumerate(head.fieldnames):
	print str(i) + ": " + str(col)

# Which col to use?
col_index = int(raw_input('Which column to use for y axis? >'))

# Prepare vars for filling and iterating
samples = [];

# Iterate over csv file
print "Iterating over CSV file..."
try:
    reader = csv.reader(file)
    for row in reader:
	samples.append(float(row[col_index]))
finally:
    file.close()

# Boot pyo server
print "Starting pyo server..."
s = Server().boot()

# Create an empty pyo table to put the data in
table = DataTable(float(len(samples)), chnls=1, init=samples);
#table.view()

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
