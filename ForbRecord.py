#!/usr/bin/python
# -*- coding: utf-8 -*-


class ForbRecord:
  def __init__(self,line='',hit=0, key='', ref=''):
    if line != '':
      (h,self.key,ref) = line.split('|',2)
      self.hit = int(h)
      self.ref = set(ref.split())
      return
    if key != '':
      self.key = key
      if ref != '':
        self.ref = set(ref.split())
        if hit == 0:
          self.hit = 1
        else:
          self.hit = hit
        return
      else:
        self.ref = set()
        self.hit = hit
        return
    self.key = ''
    self.hit = 0
    self.ref = set()    
        

  def __repr__(self):
    line=str(self.hit)+"|"+self.key+"|"
    if len(self.ref)>0:
      for ref in self.ref:
        line+= ref + " "
      return line[:-1]
    else:
      return line

  def __add__(self,other):
    result = ForbRecord()
    if self.key =='':
      if other.key =='':
        return result
    result.key = other.key

    if self.key != other.key:
      pass # fixme: grosse erreur, mais je ne sais pas la remonter... (il faudrait que j'apprenne le python un jour)

    result.hit = self.hit + other.hit
    result.ref = self.ref | other.ref
    #print(self)
    #print(other)
    #print(result)
    #print("--------")
    return result

  def __cmp__(self,other):
    return cmp(self.hit,other.hit)


if __name__ == '__main__':
  r1 = ForbRecord('173|laclef|nico fred')
  r2 = ForbRecord(key='laclef', ref='nico toto')
  
  print(r1)
  print(r2)
  print(r1+r2)

