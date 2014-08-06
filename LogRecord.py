#!/usr/bin/python
# -*- coding: utf-8 -*-


def analyse_params(paramString):
  signature=''
  params = dict()
  paramList = paramString.split('&')
  for p in paramList:
    t = p.split('=')
    if len(t)!=2:
      continue
    signature += t[0]
    params[t[0].upper()] = t[1]
  return (params,signature)


class LogRecord:

  def __init__(self, line):
    self.status      = 'ok'
    self.ip          = ''
    self.date        = ''
    self.method      = ''
    self.key         = ''
    self.urlservice  = ''
    self.params  = {}
    self.signature   = ''
    self.return_code = ''
    self.referer     = ''
 
    pip = line.find(' ',7,16)
    if pip==-1:
      self.status = 'impossible de trouver le premier blanc'
      return
    self.ip = line[0:pip]

    self.date = line[pip+6:pip+32]

    pmethod = line.find(' ',pip+37,pip+40)
    if pmethod==-1:
      self.status = 'impossible de trouver le blanc apres la methode http'
      return
    self.method = line[pip+35:pmethod]

    if self.method !='GET':
      self.status = 'not GET'
      return

    pkey = line.find('/', pmethod+3, pmethod+40)
    if pkey==-1:
      self.status = 'impossible de trouver le / apres la clef'
      return
    self.key = line[pmethod+2:pkey]

    pinter = line.find('?', pkey)
    if pinter==-1:
      self.status = 'impossible de trouver le ?'
      return
    pserv  = line[:pinter-1].rfind('/')
    self.urlservice = line[pserv+1:pinter]
    if self.urlservice == 'wmts/':
      self.urlservice = 'wmts'
    elif self.urlservice != 'wmts':
      self.status = 'not wmts'
      return
    
    pparams=line.find(' ',pinter)
    (self.params,self.signature) = analyse_params(line[pinter+1:pparams])

    self.return_code = line[pparams+11 : pparams+14]
#    self.size       =
    pbreferer = line.find('"', pparams+14)+1
    pereferer = line.find('"', pbreferer)
    self.referer    = line[pbreferer:pereferer]

  def __repr__(self):
#    if self.status != 'ok':
#      return self.status

    rep = "status:[" + str(self.status) + "]\n"
    rep+= "ip:["     + self.ip     + "]\n"
    rep+= "date:["   + self.date   + "]\n"
    rep+= "method:[" + self.method + "]\n"
    rep+= "key:["    + self.key    + "]\n"
    rep+= "urlservice:["  + self.urlservice     + "]\n"
    rep+= "params:["  + str(self.params)+ "]\n"
    rep+= "signature:["   + self.signature      + "]\n"
    rep+= "return_code:[" + self.return_code    + "]\n"
    rep+= "referer:["     + self.referer        + "]\n"

    return rep


if __name__ == '__main__':
  r = LogRecord('80.215.0.94 - - [06/Jun/2013:01:49:19 +0200] "GET /1s5mos64sdq602d1ngvktqmw/geoportail/wmts?LAYER=GEOGRAPHICALGRIDSYSTEMS.MAPS&EXCEPTIONS=text/xml&FORMAT=image/jpeg&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&&TILEMATRIX=13&TILECOL=4212&TILEROW=2996 HTTP/1.1" 200 2414 "http://la-trace.com/itineraires/vtt/1334/parc-de-figuerolles" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) Version/5.0.6 Safari/533.22.3" "-" "0.001" "563" - 1s5mos64sdq602d1ngvktqmw - GEOGRAPHICALGRIDSYSTEMS.MAPS - WMTS_EXT_GEOPORTAIL - - - - - -')
  print(r)

