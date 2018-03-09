"""
The simplest random dataset generating script.

Author: Elvira Mingazova
Date: 8.03.18
Copyright: GeneWerk GmbH
"""

# Imports are used in order to make the script compatible with python 2.7
from __future__ import division
from __future__ import print_function
from builtins import zip
from builtins import str
from builtins import range

# Imports used in the main() function
import random
import numpy
import pandas as pd

def parseArgs():
    """This function parses arguments from the command line to the
    actual script"""

    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.prog = 'progName.py'
    parser.description = 'You can provide the program with three parameters through the terminal'
    parser.add_argument("-n", type=int, help='Number of integration regions generated')
    parser.add_argument("-r", type=int, help='Range-value: defines an interval where the IR is\
                        located')
    parser.add_argument("-d", type=int, help='Delta-value: expands the range with the value\
                        provided by user')
    # add new input argument
    parser.add_argument("-i", help='Input-file .txt with names of chromosomes and their lengths\
                        in bp organized into two columns and separated by \t')
    parser.add_argument("-o", help='Output-file where the random integration sites will be saved')
    namespace = parser.parse_args((sys.argv[1:]))
    return namespace


def checkFormatting():
    """Proves whether the input file contains  two columns."""

    dimension_file = read_file()
    check=True
    # go through all of the lines and check whether exactly two columns are present
    for line in dimension_file:
        result = line.split()
        if len(result) == 2:
            continue
        else:
            print('Checking format: the text file has to contain two columns')
            check = False
            break
    if check == True:
        print("Checking format: the file is well formatted")
    return check


def checkColumn1():
    """Checks whether the first column of the input file has duplications"""

    dimension_file = read_file()
    check = True
    column1 = []
    for line in dimension_file:
        if line.split()[0].strip() not in column1:
            column1.append(line.split()[0].strip())
        else:
            print("Checking the first column: one of the chromosome names is duplicated")
            check = False
            break
    if check == True:
        print("Checking the first column: the names of chromosomes are correct")
    return check


def checkColumn2():
    """Proves whether the second column contains a positive integer."""

    dimension_file = read_file()
    check = True
    column2 = []
    for line in dimension_file:
        try:
            # extract the second column to a list and try to convert each element into an integer
            column2.append(int(line.split()[1].strip()))
        # catch a ValueError: invalid literal for int()
        except ValueError:
            check = False
            print("Checking the second column: could not convert {} to an integer"\
            .format(line.split()[1].strip()))
    if check == True:
        for length in column2:
            if length < 0:
                print("Checking the second column: you provided a negative chromosome length: {}"\
                .format(length))
                check = False
    if check == True:
        print("Checking the second column: the lengths of chromosomes are correct")
    return check


def getDimensionDict(filename):
    """Processes the given text file and returns {"chr name": chr length} pairs
    inside of a dictionary."""

    d={}
    with open(filename) as dimension_file:
        for line in dimension_file:
            key, value = line.split()
            d[key.strip()]=int(value.strip())
        dimension_file.close()
    return d

def read_file():
    """Reads in the inputfile with chromosome sizes and returns it to the program"""

    namespace = parseArgs()
    f = open(namespace.i,"r")
    dimension_file = f.readlines()
    f.close()
    return dimension_file

def write_file(integr_sites, outputf):
    """Writes the integration sites into a file with the chosen path"""
    with open(outputf,'w') as outfile:
        integr_sites.to_string(outfile)



def main():
    """"""
    #check the input file
    namespace = parseArgs()
    dimension_file = read_file()
    check = checkFormatting()
    if check == True:
        check = checkColumn1()
        if check == True:
            check = checkColumn2()
            if check == True:
                dimension_dict = getDimensionDict(namespace.i)
                integr_sites = pd.DataFrame(columns = ("Chromosome", "Start", "End", "Match",\
                 "Rnd Model", "Assembly"))
                integr_sites[['Start', 'End']] = integr_sites[['Start', 'End']].astype(int)
                #loop on n random IR
                count = 1
                #weighted chromosome choice
                weights = {k:v/sum(dimension_dict.values()) for k,v in
                dimension_dict.items()}
                chroms, probs = list(zip(*iter(weights.items())))
                for i in range(namespace.n):
                    #select a chromosome
                    chrom = numpy.random.choice(chroms, 1, p=probs)
                    #select a site on that chromosome
                    start = random.randint(1,dimension_dict[chrom[0]])
                    #select a random region
                    end = start + random.randint(0,namespace.r) + namespace.d
                    integr_sites.loc[count] = chrom[0], start, end, "unmatched", "RM0", namespace.i
                    count += 1
                print(integr_sites)
                write_file(integr_sites, namespace.o)

if __name__ == "__main__":
    main()
