##!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Pęcak <daniel.pecak@gmail.com>

import sys

if len(sys.argv)>1: 
    inputfile=sys.argv[1]
else:
    sys.exit("Nie podano pliku wejściowego.")
    
# TODO Read File
# File format 
# === beginning
# default_length_of_bar how_many cut_length
# length1 how_many1
# length2 how_many2
# length3 how_many3
# ...
# === ending

with open(inputfile,'r') as fp:
    input=fp.readlines()

cpinput = []
count3=0
for i in input:
    line = i[:-1].split()
    if len(line)==2:
        cpinput.append(line)
    if len(line)==3:
        count3 += 1
        L=line[0]
        N=line[1]
        dl=line[2]
    if len(line)>3: sys.exit("Zły format pliku wejściowego: za dużo argumentów w linii.")

# cpinput = list(map(int,cpinput))
# print cpinput    

if(count3!=1):     sys.exit("Pierwsza linia pliku jest nieprawidłowa. \n Format: długość sztabki [mm] liczba sztabek | szerokość spawu [mm] ")

print "### Długość sztabki:",L,"liczba sztabek:",N,"Szerokość spawu",dl

cpinput = input[1:]

for i in cpinput:
    i=i[:-1]
    print i
    
print cpinput

# greedy algoruthm:
# sort the list by length
# make working copy of list
# loop through the working list subtracting numbers

# output format:
# how many bars needed, how many scaps, efficiency
# bar1 length1 | length2 | .... | lengthN1 
# bar2 length1 | length2 | .... | lengthN2
# .......
# barM length1 | length2 | .... | lengthNM


# TODO test examples