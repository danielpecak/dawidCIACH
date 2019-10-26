##!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Pęcak <daniel.pecak@gmail.com>

import sys
from operator import itemgetter

if len(sys.argv)>1: 
    inputfile=sys.argv[1]
else:
    sys.exit("Nie podano pliku wejściowego.")

if len(sys.argv)>2: 
    outputfile=sys.argv[2]
else:
    outputfile='output.txt'    


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
        cpinput.append((map(int,line)))
    if len(line)==3:
        count3 += 1
        L=int(line[0])
        N=int(line[1])
        dl=int(line[2])
    if len(line)>3: sys.exit("Zły format pliku wejściowego: za dużo argumentów w linii.")


if(count3!=1):     sys.exit("Pierwsza linia pliku jest nieprawidłowa. \n Format: długość sztabki [mm] liczba sztabek | szerokość spawu [mm] ")

sumA=L*N
sumN=0.0
items=0
for i in cpinput:
    sumN += i[0]*i[1]
    items += i[1]

if(sumA<sumN): sys.exit("SPAWN MORE pretów! Wincyj prętów!")

cpaval=[L]*N*2 # TODO maybe change items to items?

print "\n###### Informacje ###### "
print "### Długość sztabki:",L,"mm \n### liczba sztabek:",N,"\n### Szerokość spawu:",dl,"mm\n "

print "Sortowanie od największego kawałka [długość, #sztuk]:"
cpinput=sorted(cpinput,key=itemgetter(0),reverse=True)
for i in xrange(len(cpinput)):
    print "Item"+str(i+1)+":", cpinput[i]


out=[[] for _ in xrange(items)]

# Greedy algorithm:
# loop through the working list subtracting numbers
scraps = 0.0
for it in xrange(items):
    iwanttobreakfree=False
    for i in xrange(len(cpinput)):
        if iwanttobreakfree: continue
        if(cpinput[i][1]>0):
            for y in xrange(items):
                if iwanttobreakfree: continue
                if(cpaval[y]>=cpinput[i][0]):
                    cpinput[i][1] = cpinput[i][1] - 1
                    cpaval[y] = cpaval[y] - cpinput[i][0]
                    out[y].append(cpinput[i][0])
                    iwanttobreakfree=True
                    if(cpaval[y]>=dl):
                        cpaval[y] = cpaval[y] - dl
                        scraps += dl

# print " "
# for ii in xrange(len(cpinput)):
#     print "Item"+str(ii+1)+":", cpinput[ii]
# print " "
# for i in xrange(len(cpaval)):
#     print cpaval[i]

# print out
# for i in xrange(items):
#     print out[i]
print "\nŚcinki:", scraps, "mm"
scraps = -scraps    
rods=0
f = open(outputfile,'w')
for o in out:
    if len(o)>0:
        txt = " | ".join(list(map(str,o)))
        print txt
        f.write(txt+'\n')
        scraps += L-sum(o)
        rods+=1
f.close()
print "\nResztki:",scraps, "mm"
print "\nSztabek trzeba:",rods
print "\nWydajność:",(rods*L-scraps)/(rods*L),"%"


# output format:
# how many bars needed, how many scaps, efficiency
# bar1 length1 | length2 | .... | lengthN1 
# bar2 length1 | length2 | .... | lengthN2
# .......
# barM length1 | length2 | .... | lengthNM


# TODO test examples