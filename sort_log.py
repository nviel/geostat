#!/usr/bin/python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------
# TODO: 
#  o stats separees par clef
#  o controle de la signature des flux 3D ?
#  o mode stats 404 : ne fait pas de rapport, seulement les stats en acceptant les 404 pour faire des cartes des tuiles non trouvées.
#  
#------------------------------------------------------------------------------------
import os
import sys
from collections import defaultdict
import LogRecord
import ForbRecord


def findSep( s, equal):
  i = equal + 1
  imax = i + 100
  while s[i]!='&' and s[i]!=' ':
    i = i+1
    if i >= imax: #or i=len(s) pour etre tout a fait rigoureux
      return 0,1
  if s[i]==' ':
    return i,1
  while s[i+1]=='&':
    i+=1
  return i,0


# -------- main -----------

logFileName = sys.argv[1]

logFile = open(logFileName, 'r')
stats = defaultdict(defaultdict)
statsForbidden = defaultdict(ForbRecord.ForbRecord)
lineNumber = 0
delta = 100000
mark = delta

badReqFile = open('bad_request.txt', 'w')
badsignFile_2D = open('bad_signature_2D.txt', 'w')
badsignFile_3D = open('bad_signature_3D.txt', 'w')
badsignFile_M = open('bad_signature_m.txt', 'w')
#notFoundFile = open('404.txt', 'w')  # FIXME utile pour faire des cartes de 404.
#forbiddenFile = open('403.txt', 'w') # FIXME utile pour faire des cartes de 403 ??
echecFile = open('echec.txt', 'w')

countNF=0  # comptage des 404
countALL=0 # comptage du total des requêtes WMTS
countOK=0
countFORB=0 # comptage des requetes interdites
countECH=0 # comptage des echecs (autres codes)
count2D=0  # comptage des requetes geoportail 2D
count3D=0  # comptage des requetes geoportail 3D
countM=0   # comptage des requetes geoportail mobile
countBad2D=0
countBad3D=0
countBadM=0



for line in logFile:
  #sys.stderr.write(line+'\n')
  lineNumber += 1
  r = LogRecord.LogRecord(line)
  if r.status != 'ok':
    if r.status == 'not GET' or r.status == 'not wmts' or r.status == 'impossible de trouver le ?':
      continue
    else:
      badReqFile.write(r.status+"\n")
      badReqFile.write(line+'\n')
      continue

  countALL+=1
  
  if r.return_code != '200' and r.return_code != '304':
    if r.return_code == '404': # pas trouve
      countNF+=1
      # FIXME reactiver l'enregistrement des 404 pour faire des cartes?
      continue
    if r.return_code == '403': # manque de droits
      countFORB+=1
      #forbiddenFile.write(line+'\n') # commenté parce que ca prend plein de place et que le rapport est plus consis
                                      # A réactiver si on veut en faire une carte, mais je ne vois pas l'intérêt
      statsForbidden[r.key] = statsForbidden[r.key] + ForbRecord.ForbRecord(key=r.key,ref=r.referer)
      continue
    if r.return_code == '499': # le client est parti avant d'avoir sa reponse.
      continue
    countECH+=1
    echecFile.write(line+'\n')
    continue

  countOK+=1

  #controle clef du geoportail
  if r.key == 'tyujsdxmzox31ituc2uw0qwl':
    count2D+=1
    if r.signature[:74] != 'SERVICEVERSIONREQUESTLAYERSTYLEFORMATTILEMATRIXSETTILEMATRIXTILEROWTILECOL':
      countBad2D+=1
      badsignFile_2D.write(line+'\n')
  #controle clef du geoportail mobile
  elif r.key == '6usqvehthxi0ck95g2s9sc36':
    countM+=1
    if r.signature != 'SERVICEREQUESTVERSIONLAYERSTYLETILEMATRIXSETTILEMATRIXTILEROWTILECOLFORMAT':
      countBadM+=1
      badsignFile_M.write(line+'\n')
  #controle clef du geoportail 3D
#  if r.key = '???' and r.signature[:66] != '???':
#    badsignFile_3D.write(line)

# facultatif parce qu'on a eu un 200
#  if 'REQUEST' not in r.params:
#    badReqFile.write(">>> pas de paramertre request\n")
#    badReqFile.write(line+'\n')
#    continue

  if r.params['REQUEST'].upper() != 'GETTILE':
    continue

# facultatif parce qu'on a eu un 200
#  if 'TILEMATRIXSET' not in r.params or 'TILEMATRIX' not in r.params or 'TILECOL' not in r.params or 'TILEROW' not in r.params or 'LAYER' not in r.params:
#    badReqFile.write(">>> il manque un parametre\n")
#    badReqFile.write(line+'\n')
#    continue


  if r.params['TILEMATRIXSET']!='PM':
    continue # on ne le met pas en erreur parce qu'on a les couches en WGS84G de la 3D

# facultatif parce qu'on a eu un 200
#  if not (r.params['TILEMATRIX'].isdigit():
#    badReqFile.write(">>> mauvais TM\n")
#    badReqFile.write(line+'\n')
#    continue


  if not r.params['TILECOL'].isdigit():
    if r.params['TILECOL'][0]=='-':
      continue
    v=''
    for c in r.params['TILECOL']:
      if not c.isdigit():
        break
      v+=c
    if len(v) != 0:
      r.params['TILECOL']=v
    else:
      badReqFile.write(">>> tilecol non numerique\n")
      badReqFile.write(line+'\n')
      continue

  if not r.params['TILEROW'].isdigit():
    if r.params['TILEROW'][0]=='-':
      continue
    v=''
    for c in r.params['TILEROW']:
      if not c.isdigit():
        break
      v+=c
    if len(v) != 0:
      r.params['TILEROW']=v
    else:
      badReqFile.write(">>> tilerow non numerique\n")
      badReqFile.write(line+'\n')
      continue

  layerVal = r.params['LAYER']
  tmVal = r.params['TILEMATRIX']
  colVal = r.params['TILECOL']
  rowVal = r.params['TILEROW']
  statName = layerVal+"."+tmVal
  coordVal = colVal+" "+rowVal

  if statName in stats.keys():
    tm = stats[statName]
  else:
    tm=defaultdict(int)
    stats[statName]=tm

  tm[coordVal] += 1



  if lineNumber >= mark:
    mark += delta
    print(str(lineNumber))

# generation des fichiers de stats pour les cartes
for statName in stats:
  statFile = open(statName, 'w')
  coords=stats[statName]
  for coord in coords:
    statFile.write(coord + " " + str(coords[coord])+"\n")
  statFile.close()
 
# generation des rapports de stats textuels
forbiddenReport = open('forbiddenReport.txt','w')
for key in statsForbidden:
  forbiddenReport.write(str(statsForbidden[key]) + "\n")
forbiddenReport.close()

report = open('report.txt','w')
report.write("Nombre total de requetes WMTS:                  "+str(countALL)+"\n")
report.write("Nombre de 404:                                  "+str(countNF)+"\n")
report.write("Nombre de 403:                                  "+str(countFORB)+"\n")
report.write("Nombre de clefs en 403:                         "+str(len(statsForbidden.keys()))+"\n")
report.write("Nombre de requetes ayant une reponse complete:  "+str(countOK)+"\n")
report.write("Nombre de requetes sur la clef geoportail 2D:             "+str(count2D)+"\n")
report.write("Nombre de requetes illegitimes sur la clef geoportail 2D: "+str(countBad2D)+" ("+str(countBad2D*100.0/count2D)+"%)\n")
#report.write("Nombre de requetes illegitimes sur la clef geoportail 2D: "+str(countBad2D)+"\n")
report.write("Nombre de requetes sur la clef geoportail M:              "+str(countM)+"\n")
report.write("Nombre de requetes illegitimes sur la clef geoportail M:  "+str(countBadM)+" ("+str(countBadM*100.0/countM)+"%)\n")
#report.write("Nombre de requetes illegitimes sur la clef geoportail M:  "+str(countBadM)+"\n")
