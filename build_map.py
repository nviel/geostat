#!/usr/bin/python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# TODO: o ajouter l'échelle
#       o utiliser une échelle fixe pour toutes les dates (avec seuil max)
#       o ajouter des éléments géographiques (frontières, villes)
#       o ajouter un géoréférencement pour importer dans QGIS...
#------------------------------------------------------------------------------
import os
import sys
import Carte
from PIL import Image
from PIL.ImageChops import multiply

def pond(v,dl):
  return v << dl

carte= Carte.Carte(sys.argv[1])

carte_matrix= [ [ 0 for i in range(carte.terr.dy) ] for j in range(carte.terr.dx) ]
maxval = 0



level_min = 99
level_max = 0
for fileName in carte.sources:
  if int(carte.sources[fileName]) > level_max:
    level_max = int(carte.sources[fileName])
  if int(carte.sources[fileName]) < level_min:
    level_min = int(carte.sources[fileName])




for fileName in carte.sources:
  fileLevel = int(carte.sources[fileName])

  inFile=open(fileName.upper(), 'r')

  for line in inFile:
    (i,j,v)=map(int,line.split())
    #print(i,j,v)
    dl = fileLevel - carte.terr.pix_level     # difference de niveau par rapport a celui de la carte.
    delta_file_level = fileLevel - level_min  # difference de niveau par rapport au niveau mini des stats utilisees 
                                              # (sert a ponderer la representation)

    # FIXME: j'ai le sentiment qu'on est pas oblige de faire 2 cas. Une formule generique devrait faire l'affaire (mais est-ce souhaitable pour la lisibilite?
    if dl >= 0:
      x = (i>>dl) - carte.terr.xo
      y = (j>>dl) - carte.terr.yo
      if x>=0 and x<carte.terr.dx and y>=0 and y<carte.terr.dy: 
        carte_matrix[x][y] += pond(v, delta_file_level)
        #print(carte_matrix[x][y])
        if carte_matrix[x][y] > maxval:
          maxval = carte_matrix[x][y]
    else:
      xmin = max(0, (i << -dl) -carte.terr.xo)
      xmax = min(carte.terr.dx-1,((i+1) << -dl) -1-carte.terr.xo)
    
      ymin = max(0,(j << -dl) -carte.terr.yo)
      ymax = min(carte.terr.dy-1,((j+1) << -dl) -1-carte.terr.yo)
      
      #print (xmin,xmax,ymin,ymax)
      if xmin > xmax or ymin > ymax:
        continue  
 
      for x in range (xmin,xmax + 1):
        for y in range (ymin, ymax + 1):
          carte_matrix[x][y] += pond(v, delta_file_level)
          if carte_matrix[x][y] > maxval:
            maxval = carte_matrix[x][y]

# il est possible d'utiliser un image en palette de couleur, mais je me suis trouve confronte a un 
# probleme quand j'ai voulu ajouter les limites des continents en noir. Du coup je reste en RVB pour
# pouvoir faire un multiply.

im = Image.new('RGB',(carte.terr.dx,carte.terr.dy)) #FIXME: image en gray ou palette de couleur.
print (maxval)
dyn = 255.0 / float(maxval)

for i in range(carte.terr.dx):
  for j in range (carte.terr.dy):
    v = int (carte_matrix[i][j] * dyn) # FIXME: un grand coup de map() devrait etre plus efficace.
    # FIXME: le remplissage pixel par pixel n'est peut etre pas le plus performant. 
    #        Ceci dit l'enregistrement de l'image n'est pas non plus excessivement long.
    im.putpixel((i,j),carte.palette[v])  

# FIXME: reactiver la superposition du contour
#imContour = Image.open(carte.terr.contour)
#imResult = multiply(im, imContour)
#imResult.save(carte.name)

im.save(carte.name)
