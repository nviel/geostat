#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser

def build_LUT(lutConfFileName):
  pal=[(0,0,0) for i in range(256)]
  lutFile=open(lutConfFileName,'r')
  (nd,rd,vd,bd) = map(int,lutFile.readline().split())
  (nf,rf,vf,bf) = (0,0,0,0)
  for line in lutFile:
    (nf,rf,vf,bf)=map(int,line.split())
    dn = nf - nd
    (dr,dv,db)=(float(rf-rd)/dn,float(vf-vd)/dn,float(bf-bd)/dn)
    for i in range(dn):
      pal[nd+i]=(int(rd+dr*i),int(vd+dv*i),int(bd+db*i))
    (nd,rd,vd,bd)=(nf,rf,vf,bf)
  pal[nf] = (rf,vf,bf)
  return pal



class Territoire:
  def __init__(self, configFileName):
    self.configFileName = configFileName
    config = ConfigParser.ConfigParser()
    config.read(configFileName)
    self.xo = config.getint('territoire','xo')
    self.yo = config.getint('territoire','yo')
    self.dx = config.getint('territoire','dx')
    self.dy = config.getint('territoire','dy')
    self.pix_level = config.getint('territoire','pix_level')
    self.contour   = config.get ('territoire','contour') 
    
  def __repr__(self):
    return "Fichier:" + self.configFileName + "\nxo=" + str(self.xo) + " yo=" + str(self.yo) + "\ndx=" + str(self.dx) + " dy=" + str(self.dy)

class Carte:
  def __init__(self, configFileName):
    self.configFileName = configFileName
    config = ConfigParser.ConfigParser()
    config.read(configFileName)
    self.name     = config.get('carte','name')
    self.terr     = Territoire(config.get('carte','territoire'))
    self.palette  = build_LUT(config.get('carte','palette'))
    self.sources  = dict(config.items('sources'))
  
  def __repr__(self):
    desc =  "Fichier:"    + self.configFileName + "\n"
    desc += "name:"       + self.name +"\n"
    desc += "territoire:" + str(self.terr) +"\n"
    desc += "palette:"    + str(self.palette) +"\n"
    desc += "SOURCES:\n"
    for source in self.sources:
      desc += source + ":" + self.sources[source] + "\n"
    return desc


if __name__ == '__main__':
  c = Carte('/home/nico/Applications/tools/geostats/ressouces/cartes/WLD_ORTHOIMAGERY.ORTHOPHOTOS_1-10.map')
  print(c)
#  t = Territoire("/home/nico/Applications/tools/geostats/ressouces/territoires/monde_10.ter")
#  print(t)


