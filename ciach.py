##!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Pęcak <daniel.pecak@gmail.com>

import sys
from operator import itemgetter

if len(sys.argv)>1: 
    inputfile=sys.argv[1]
else:
    sys.exit("Nie podano pliku wejsciowego.")

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
    if len(line)>3: sys.exit("Zly format pliku wejsciowego: za duzo argumentow w linii.")


if(count3!=1):     sys.exit("Pierwsza linia pliku jest nieprawidlowa. \n Format: dlugosc profilu [mm] liczba profili | szerokosc ciecia [mm] ")

sumA=L*N
sumN=0.0
items=0
for i in cpinput:
    sumN += i[0]*i[1]
    items += i[1]

if(sumA<sumN): sys.exit("SPAWN MORE pretow! Wincyj pretow!")

cpaval=[L]*N*2 # TODO maybe change items to items?
f = open(outputfile,'w')
f.write("###### Informacje ###### \n")
f.write("### Dlugosc profilu: {} mm \n### liczba profili: {} \n### Szerokosc ciecia: {} mm\n\n".format(L,N,dl))

f.write("### Sortowanie od najwiekszego kawalka [dlugosc, #sztuk]:\n")
cpinput=sorted(cpinput,key=itemgetter(0),reverse=True)
for i in xrange(len(cpinput)):
    f.write("Item{}: {}\n".format(str(i+1), cpinput[i]))
f.write("\n")

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
f.write("\nScinki (lacznie): {} mm\n".format(scraps))
scraps = -scraps    
rods=0


f.write("### Ciachaj kolejne profile w ten sposób: \n")

i = 0
for o in out:
    if len(o)>0:
        i+=1
        txt = "Profil nr {} ({}/{}): ".format(i,sum(o),L)
        txt += " | ".join(list(map(str,o)))
        # print txt
        f.write(txt+'\n')
        scraps += L-sum(o)
        rods+=1
f.write("\nResztki: {} mm".format(scraps))
f.write("\nPotrzebnych profili: {}".format(rods))
f.write("\nWydajnosc: {0:.2f} %\n".format(100.*(rods*L-scraps)/(rods*L)))
f.close()


# output format:
# how many bars needed, how many scaps, efficiency
# bar1 length1 | length2 | .... | lengthN1 
# bar2 length1 | length2 | .... | lengthN2
# .......
# barM length1 | length2 | .... | lengthNM


# TODO test examples