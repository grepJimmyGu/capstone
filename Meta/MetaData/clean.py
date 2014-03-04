#!/usr/bin/env python
import csv, sys, os
a = open('Name')
b = a.read()
c = b.split('\n')

for row in c:
    b = row + 'Clean' + '.csv'
    name = row + '.csv'
    print b
    ifile = open(name, "rb")
    reader = csv.reader(ifile)
    ofile = open(b, "wb")
    writer = csv.writer(ofile, delimiter="\t", quotechar='"', quoting = csv.QUOTE_MINIMAL)

    count =0
    for row in reader:
        data = row[0], row[3], row[4], row[5], row[6], row[7], row[8], row[10], row[14], row[18]
        writer.writerow(data)
    os.remove(name)
        #count +=1
        #if count >=2:
            #exit

