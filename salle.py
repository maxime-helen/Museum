# -*- coding: utf-8 -*-
import primitives as prims
import random

def getVal(attrs,nom,defaut):
  if attrs.has_key(nom):
    return attrs[nom]
  else:
    return defaut

class Signaletique:
  def __init__(self):
    self.buffer = {}
    self.count = 0
    self.buffer_siblings = []

  def count_salle(self):
    self.count = self.count+1

  def get_size_signaletique(self):
    return [4.048,1.6]

  def draw_signaletique(self,path,translation_x,translation_z,rotation) :
    lesFils = [1]
    signaletique = prims.Tableau({'largeur':float((self.get_size_signaletique()[0])),'hauteur':float((self.get_size_signaletique()[1])),'texture':str(path)})
    lesFils[0]=signaletique
    prims.Transform(lesFils,{"translation":str(translation_x)+" "+str(0.0)+" "+str(translation_z),"rotation":rotation}).draw()

  def add_salle(self,salle):
    self.buffer[str(unicode(salle.x))+" "+str(unicode(salle.y))]= salle

  def sort_buffer_siblings(self):
    def get_key_x(item):
      return item.x
    def get_key_y(item):
      return item.y
    self.buffer_siblings = [i for i in sorted(self.buffer_siblings,key=get_key_x)]
    self.buffer_siblings = [i for i in sorted(self.buffer_siblings,key=get_key_y)]

  def set_buffer_siblings(self,salle):
    if((str(salle.x+10.0)+" "+str(salle.y)) in self.buffer) :
      self.buffer_siblings.append(self.buffer[str(salle.x+10.0)+" "+str(unicode(salle.y))])
    if((str(salle.x-10.0)+" "+str(salle.y)) in self.buffer) :
      self.buffer_siblings.append(self.buffer[str(salle.x-10.0)+" "+str(unicode(salle.y))])
    if((str(salle.x)+" "+str(salle.y+10.0)) in self.buffer) :
      self.buffer_siblings.append(self.buffer[str(salle.x)+" "+str(unicode(salle.y+10.0))])
    if((str(salle.x)+" "+str(salle.y-10.0)) in self.buffer) :
      self.buffer_siblings.append(self.buffer[str(salle.x)+" "+str(unicode(salle.y-10.0))])

  def draw(self) :
    for element in self.buffer:
      self.set_buffer_siblings(self.buffer[element])
      self.sort_buffer_siblings()
      for subelement in self.buffer_siblings:
        offset_x = self.buffer[element].x-subelement.x
        offset_y = self.buffer[element].y-subelement.y
        if (offset_x==-10.0 and int(self.buffer[element].n)!=0): #N
          if(int(self.buffer[element].n)==2):
            self.draw_signaletique("signalisation/sens_visite_gauche.jpg",self.buffer[element].x+4.88,self.buffer[element].y+4.00,"-90.0 0.0 1.0 0.0")
          elif(int(self.buffer[element].n)!=0):
            if(subelement.style!='none'):
              self.draw_signaletique("signalisation/salle_"+subelement.style+"_gauche.jpg",self.buffer[element].x+4.88,self.buffer[element].y+2.00,"-90.0 0.0 1.0 0.0")
            else:
              self.draw_signaletique("signalisation/sens_visite_gauche.jpg",self.buffer[element].x+4.88,self.buffer[element].y+2.00,"-90.0 0.0 1.0 0.0")
        elif (offset_x==10.0 and int(self.buffer[element].s)!=0): #S
          if(int(self.buffer[element].s)==2):
            self.draw_signaletique("signalisation/sens_visite_droite.jpg",self.buffer[element].x-4.88,self.buffer[element].y+4.00,"90.0 0.0 1.0 0.0")
          elif(int(self.buffer[element].s)!=0):
            if(subelement.style!='none'):
              self.draw_signaletique("signalisation/salle_"+subelement.style+"_droite.jpg",self.buffer[element].x-4.88,self.buffer[element].y+2.00,"90.0 0.0 1.0 0.0")
            else :
              self.draw_signaletique("signalisation/sens_visite_droite.jpg",self.buffer[element].x-4.88,self.buffer[element].y+2.00,"90.0 0.0 1.0 0.0")
        if (offset_y==10.0 and int(self.buffer[element].w)!=0): #W
          if(int(self.buffer[element].w)==2):
            self.draw_signaletique("signalisation/sens_visite_droite.jpg",self.buffer[element].x-4.00,self.buffer[element].y-4.88,"0.0 0.0 1.0 0.0")
          elif(int(self.buffer[element].w)!=0): 
            if(subelement.style!='none'):
              self.draw_signaletique("signalisation/salle_"+subelement.style+"_gauche.jpg",self.buffer[element].x+2.00,self.buffer[element].y-4.88,"0.0 0.0 1.0 0.0")
            else :
              self.draw_signaletique("signalisation/sens_visite_gauche.jpg",self.buffer[element].x+2.00,self.buffer[element].y-4.88,"0.0 0.0 1.0 0.0")
        elif (offset_y==-10.0 and int(self.buffer[element].e)!=0): #E
          if(int(self.buffer[element].e)==2) :
            self.draw_signaletique("signalisation/sens_visite_droite.jpg",self.buffer[element].x+4.00,self.buffer[element].y+4.88,"180.0 0.0 1.0 0.0")
          elif(int(self.buffer[element].e)!=0):
            if(subelement.style!='none'):
              self.draw_signaletique("signalisation/salle_"+subelement.style+"_droite.jpg",self.buffer[element].x+2.00,self.buffer[element].y+4.88,"180.0 0.0 1.0 0.0")
            else :
              self.draw_signaletique("signalisation/sens_visite_droite.jpg",self.buffer[element].x+2.00,self.buffer[element].y+4.88,"180.0 0.0 1.0 0.0")
      self.buffer_siblings = []

class Salle:
  def __init__(self,attr):
    self.x = float(getVal(attr,"x",0.0))
    self.y = float(getVal(attr,"y",0.0))
    self.n = getVal(attr,"north",0) # 0 - sans ouverture; 1 - avec petite ouverture; 2 - avec grande ouverture; 3 - sans cloisons
    self.e = getVal(attr,"est",0) # 0 - sans ouverture; 1 - avec petite ouverture; 2 - avec grande ouverture; 3 - sans cloisons
    self.s = getVal(attr,"south",0) # 0 - sans ouverture; 1 - avec petite ouverture; 2 - avec grande ouverture; 3 - sans cloisons
    self.w = getVal(attr,"west",0) # 0 - sans ouverture; 1 - avec petite ouverture; 2 - avec grande ouverture; 3 - sans cloisons
    self.style = getVal(attr,"theme","none")
    self.buffer_wall=[self.n,self.s,self.e,self.w]
    self.buffer_tableau = "none"
    self.count_tableau = 1

  def cloison(self,translation_x,translation_z,rotation):
    lesFils=[5]
    mur = prims.MurPlein({"largeur":10.0, "hauteur":3.5, "recto":"textures/029frene.jpg", "facteurTexture":3.0})
    lesFils[0]=mur
    prims.Transform(lesFils,{"translation":str(translation_x)+" "+str(0.0)+" "+str(translation_z),"rotation":rotation}).draw()

  def cloison_ouverte(self,translation_x,translation_z,rotation,offset_x,offset_y):
    if(offset_x==6.0 or offset_y==6.0 or offset_y==-6.0 or offset_y==-6.0):
      largeur = 4.0
    else:
      largeur= 2.0
    lesFils=[5]
    mur = prims.MurPlein({"largeur":largeur, "hauteur":3.5, "recto":"textures/029frene.jpg", "facteurTexture":3.0})
    lesFils[0]=mur
    prims.Transform(lesFils,{"translation":str(translation_x)+" "+str(0.0)+" "+str(translation_z),"rotation":rotation}).draw()
    mur = prims.MurPlein({"largeur":largeur, "hauteur":3.5, "recto":"textures/029frene.jpg", "facteurTexture":3.0})
    lesFils[0]=mur
    prims.Transform(lesFils,{"translation":str(translation_x+offset_x)+" "+str(0.0)+" "+str(translation_z+offset_y),"rotation":rotation}).draw()

  def get_tableau_by_theme(self):
    if int(self.count_tableau) != 4: 
      if self.buffer_tableau in "pics/"+str(self.style)+"/"+str(self.count_tableau)+".jpg" :
        self.count_tableau = self.count_tableau+1
      self.buffer_tableau = "pics/"+str(self.style)+"/"+str(self.count_tableau)+".jpg"
      return self.buffer_tableau
    else : return 'A'

  def get_size_tableau(self):
    return [4.048,1.6]

  def draw_tableau(self,path,translation_x,translation_z,rotation):
    if path!='A' :
      lesFils=[5]
      tableau = prims.Tableau({'largeur':float((self.get_size_tableau()[0])),'hauteur':float((self.get_size_tableau()[1])),'texture':str(path)})
      lesFils[0]=tableau
      prims.Transform(lesFils,{"translation":str(translation_x)+" "+str(1.0)+" "+str(translation_z),"rotation":rotation}).draw()
  
  def tableaux(self,translation_x,translation_y,rotation):
    #Si la salle comporte une cloison_2, alors c'est un couloir donc pas de tableau
    flag = 0
    for element in self.buffer_wall:
      if int(element)==2 :
        flag=1
    if flag==0 :
      a = self.get_tableau_by_theme()
      self.draw_tableau(str(a),translation_x,translation_y,rotation)

  def random_offset(self):
      # offset = random.randint(0, 1)
      offset = 1
      if offset==0 :
        offset = 3
      else :
        offset = -3
      return offset

  def draw(self):
    lesFils=[5]
    if int(self.n) == 0:
      translation_x = float(self.x) + 5.0
      translation_z = float(self.y) + 5.0
      offset = 0
      self.cloison(translation_x, translation_z,"90.0 0.0 1.0 0.0")
    elif int(self.n) == 1:
      translation_x = float(self.x) + 5.0
      translation_z = float(self.y) + 5.0
      offset = self.random_offset()
      self.cloison_ouverte(translation_x, translation_z,"90.0 0.0 1.0 0.0",0.0,-6.0)
    elif int(self.n) == 2:
      translation_x = float(self.x) + 5.0
      translation_z = float(self.y) + 5.0
      offset = 0
      self.cloison_ouverte(translation_x, translation_z,"90.0 0.0 1.0 0.0",0.0,-8.00)
    translation_x = float(self.x) + 4.7
    translation_z = float(self.y) + offset
    self.tableaux(translation_x, translation_z,"-90.0 0.0 1.0 0.0")
    if int(self.s) == 0:
      translation_x = float(self.x) - 5.0
      translation_z = float(self.y) + 5.0
      offset = 0
      self.cloison(translation_x, translation_z,"90.0 0.0 1.0 0.0")
    elif int(self.s) == 1:
      translation_x = float(self.x) - 5.0
      translation_z = float(self.y) + 5.0
      offset = self.random_offset()
      self.cloison_ouverte(translation_x, translation_z,"90.0 0.0 1.0 0.0",0.0,-6.0)
    elif int(self.s) == 2:
      translation_x = float(self.x) - 5.0
      translation_z = float(self.y) + 5.0
      offset = 0
      self.cloison_ouverte(translation_x, translation_z,"90.0 0.0 1.0 0.0",0.0,-8.0)
    translation_x = float(self.x) - 4.7
    translation_z = float(self.y) + offset
    self.tableaux(translation_x, translation_z,"90.0 0.0 1.0 0.0")
    if int(self.e) == 0:
      translation_x = float(self.x) - 5.0
      translation_z = float(self.y) + 5.0
      offset = 0
      self.cloison(translation_x, translation_z,"0.0 0.0 1.0 0.0")
    elif int(self.e) == 1:
      translation_x = float(self.x) - 5.0
      translation_z = float(self.y) + 5.0
      offset = self.random_offset()
      self.cloison_ouverte(translation_x, translation_z,"0.0 0.0 0.0 0.0",6.0,0.0)
    elif int(self.e) == 2:
      translation_x = float(self.x) - 5.0
      translation_z = float(self.y) + 5.0
      offset = 0
      self.cloison_ouverte(translation_x, translation_z,"0.0 0.0 0.0 0.0",8.0,0.0)
    translation_x = float(self.x) + offset
    translation_z = float(self.y) + 4.7 
    self.tableaux(translation_x, translation_z,"180.0 0.0 1.0 0.0")
    if int(self.w) == 0:
      translation_x = float(self.x) - 5.0
      translation_z = float(self.y) - 5.0
      offset = 0
      self.cloison(translation_x, translation_z,"0.0 0.0 0.0 0.0")
    elif int(self.w) == 1:
      translation_x = float(self.x) - 5.0
      translation_z = float(self.y) - 5.0
      offset = self.random_offset()
      self.cloison_ouverte(translation_x, translation_z,"0.0 1.0 0.0 0.0",6.0,0.0)
    elif int(self.w) == 2:
      translation_x = float(self.x) - 5.0
      translation_z = float(self.y) - 5.0
      offset = 0
      self.cloison_ouverte(translation_x, translation_z,"0.0 1.0 0.0 0.0",8.0,0.0)
    translation_x = float(self.x) + offset
    translation_z = float(self.y) - 4.7 
    self.tableaux(translation_x, translation_z,"0.0 0.0 1.0 0.0")
    self.count_tableau=1
 
      

      
      
      


    
  
      