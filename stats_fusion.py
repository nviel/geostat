#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from collections import defaultdict


outFileName = sys.argv[1]
fileNameList = sys.argv[2:]

stats = defaultdict(int)

for fileName in fileNameList:
  inFile = open(fileName,'r')
  for line in inFile:
    (k,sv) = line.rsplit(' ',1)
    v=int(sv)
    stats[k] += v
  inFile.close()

    
outFile = open(outFileName,'w')
for k in stats:
  outFile.write(k + " " + str(stats[k]) + "\n")
