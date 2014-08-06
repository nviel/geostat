#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from collections import defaultdict
import ForbRecord


outFileName = sys.argv[1]
fileNameList = sys.argv[2:]

report = defaultdict(ForbRecord.ForbRecord)

for fileName in fileNameList:
  inFile = open(fileName,'r')
  for line in inFile:
    r = ForbRecord.ForbRecord(line)
    report[r.key] = report[r.key] + r
  inFile.close()

l=[]
for k in report:
  l.append(report[k])

l.sort(reverse=1)
    
outFile = open(outFileName,'w')
for r in l:
  outFile.write(repr(r)+"\n")
  #print(r) 
