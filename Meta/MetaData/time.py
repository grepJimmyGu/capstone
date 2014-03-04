#! /usr/bin/env python
import csv, sys, os, numpy
a = open('Name')
b = a.read()
name = b.split('\n')
for i in name:
    newname = name + 'Clean' + '.csv'
    input = open(newname, "rb")
    reader = csv.reader(input)
    output = 
