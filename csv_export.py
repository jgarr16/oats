# Public Contract: given the name of a CSV file as an argument, this module will read the CSV and return its contents as settings.reader


import csv
import settings


def read(file):
    fname = file
    f = open(fname, 'r', encoding='latin-1')
    next(f, None)  # skip the header row
    settings.reader = csv.reader(f)
