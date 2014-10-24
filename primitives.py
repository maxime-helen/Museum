# -*- coding: utf-8 -*-

import pyglet
from pyglet.gl import *

def id(x):
	return x

def triplet(chaine):
	coords = chaine.split()
	return (float(coords[0]), float(coords[1]), float(coords[2])) 

def quadruplet(chaine):
	coords = chaine.split()
	return (float(coords[0]), float(coords[1]), float(coords[2]), float(coords[3])) 

def getVal(attrs,fconv, nom,defaut):
	if attrs.has_key(nom):
		return fconv(attrs[nom])
	else:
		return defaut


class CatalogueTextures : 

	def __init__(self):
		self.catalogue = {}

	def chargerTexture(self,nom):

		if self.catalogue.has_key(nom):
			return self.catalogue[nom]
		else:
			image = pyglet.image.load(nom)
			print ">>>>> TEXTURE ", nom, " CHARGEE"
			texture = image.get_texture()
			glBindTexture(GL_TEXTURE_2D,texture.id)
			glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
			glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
			self.catalogue[nom] = texture
			return texture

catalogueTextures = CatalogueTextures()


class Scene : 

	def __init__(self,fils):
		self.lesFils = fils

	def __call__(self):
		return self.lesFils

	def draw(self):
		for fils in self.lesFils : 
			fils.draw()

class Transform : 

	def __init__(self,fils,attr):
		self.lesFils = fils
		self.translation = getVal(attr,triplet,'translation',(0.0,0.0,0.0))
		self.rotation = getVal(attr,quadruplet,'rotation',(0.0,0.0,1.0,0.0))

	def draw(self):
		tx, ty, tz = self.translation
		angle, ax, ay, az = self.rotation
		glPushMatrix()
		glTranslatef(tx, ty, tz)
		glRotatef(angle, ax, ay, az)

		for f in self.lesFils : 
			f.draw()

		glPopMatrix()


class Rectangle : 

	def __init__(self,attr):
		self.largeur = getVal(attr,float,"largeur",1.0)
		self.hauteur = getVal(attr,float,"hauteur",2.5)

	def __repr__(self):
		return "<Rectangle :: larg = %f - haut = %f>" % (self.largeur, self.hauteur)


	def draw(self):
		glBegin(GL_QUADS)
		glVertex3f(0.0, 0.0, 0.0)
		glVertex3f(self.largeur, 0.0, 0.0)
		glVertex3f(self.largeur, self.hauteur, 0.0)
		glVertex3f(0.0, self.hauteur, 0.0)
		glEnd()


class Tableau : 
	def __init__(self,attr):
		self.largeur = getVal(attr,float,"largeur",1.0)
		self.hauteur = getVal(attr,float,"hauteur",2.5)
		nomTexture = getVal(attr,id,'texture','tableaux/guernica.jpg')
		self.texture = catalogueTextures.chargerTexture(nomTexture)
		
	def draw(self):
	
		glPushMatrix()
	
		glScalef(self.largeur/2.0, self.hauteur, 1.0)

		#glDisable(GL_TEXTURE_2D)

		glBindTexture(GL_TEXTURE_2D,self.texture.id)
		glBegin(GL_QUADS)

		# Affichage du recto

	
		glTexCoord2f(0.0, 0.0)
		glVertex3f(-0.5, 0.0, 0.0)
		glTexCoord2f(1.0, 0.0)
		glVertex3f( 0.5, 0.0, 0.0)
		glTexCoord2f(1.0,1.0)
		glVertex3f( 0.5, 1.0, 0.0)
		glTexCoord2f(0.0,1.0)
		glVertex3f(-0.5, 1.0, 0.0)

		glEnd()

	

		glDisable(GL_TEXTURE_2D)	

		glBegin(GL_QUADS)
		
		# Affichage du verso

		glColor3f(1.0,0.0,0.0)
		glVertex3f(-0.5, 0.0, -0.02)
		glVertex3f(-0.5, 1.0, -0.02)
		glVertex3f( 0.5, 1.0, -0.02)
		glVertex3f( 0.5, 0.0, -0.02)

		glColor3f(1.0,1.0,1.0)

		# Cote droit
		glVertex3f(0.5,0.0,0.0)
		glVertex3f(0.5,0.0,-0.02)
		glVertex3f(0.5,1.0,-0.02)
		glVertex3f(0.5,1.0,0.0)

		# Cote gauche
		glVertex3f(-0.5,0.0,0.0)
		glVertex3f(-0.5,1.0,0.0)
		glVertex3f(-0.5,1.0,-0.02)
		glVertex3f(-0.5,0.0,-0.02)

		# Cote haut
		glVertex3f(-0.5, 1.0, 0.0)
		glVertex3f( 0.5, 1.0, 0.0)
		glVertex3f( 0.5, 1.0,-0.02)
		glVertex3f(-0.5, 1.0,-0.02)

		# Cote bas
		glVertex3f(-0.5, 0.0, 0.0) 
		glVertex3f(-0.5, 0.0,-0.02)
		glVertex3f( 0.5, 0.0,-0.02)
		glVertex3f( 0.5, 0.0, 0.0)

		glEnd()

		glEnable(GL_TEXTURE_2D)
		glPopMatrix()







class Sol : 
	def __init__(self,attr):
		self.taille = getVal(attr, float,"taille",10.0)
		nomTexture = getVal(attr,id,"texture","oups.jpg")
		self.texture = catalogueTextures.chargerTexture(nomTexture)
		self.facteurTexture = getVal(attr,float,"facteurTexture",1.0)
	
	def draw(self):

		taille = self.taille
		fz = 1.0
		
		glBindTexture(GL_TEXTURE_2D,self.texture.id)
		glBegin(GL_QUADS)
		glTexCoord2f(0.0,0.0)
		glVertex3f(-taille,0.0,taille)
		glTexCoord2f(taille,0.0)
		glVertex3f(taille,0.0, taille)
		glTexCoord2f(taille,taille)
		glVertex3f(taille,0.0,-taille)
		glTexCoord2f(0.0,taille)
		glVertex3f(-taille,0.0,-taille)
		glEnd()







class MurPlein : 

	def __init__(self,attr):
		self.facteurTexture = getVal(attr,float,"facteurTexture",1.0)
		self.largeur = getVal(attr,float,"largeur",1.0)
		self.hauteur = getVal(attr,float,"hauteur",1.0)
		nomText1 = getVal(attr,id,"recto",None)
		nomText2 = getVal(attr,id,"verso",None)
		self.textureRecto = catalogueTextures.chargerTexture(nomText1)
		if nomText2 == None : 
			self.textureVerso = self.textureRecto
		else:
			self.textureVerso = catalogueTextures.chargerTexture(nomText2)
		self.demiEpaisseur = 0.2/2.0


	def draw(self):	
		zft = self.facteurTexture

		# Affichage du recto

		glBindTexture(GL_TEXTURE_2D,self.textureRecto.id)

		glBegin(GL_QUADS)
		glTexCoord2f(0.0, 0.0)
		glVertex3f(0.0, 0.0, self.demiEpaisseur)
		glTexCoord2f(zft, 0.0)
		glVertex3f(self.largeur, 0.0, self.demiEpaisseur)
		glTexCoord2f(zft,zft)
		glVertex3f( self.largeur, self.hauteur, self.demiEpaisseur)
		glTexCoord2f(0.0,zft)
		glVertex3f(0.0, self.hauteur, self.demiEpaisseur)

		glEnd()

		# Affichage du verso

		glBindTexture(GL_TEXTURE_2D,self.textureVerso.id)

		glBegin(GL_QUADS)
		glTexCoord2f(0.0, 0.0)
		glVertex3f(0.0, 0.0, -self.demiEpaisseur)
		glTexCoord2f(0.0, zft)
		glVertex3f(0.0, self.hauteur, -self.demiEpaisseur)
		glTexCoord2f(zft, zft)
		glVertex3f( self.largeur, self.hauteur, -self.demiEpaisseur)
		glTexCoord2f(zft,0.0)
		glVertex3f(self.largeur, 0.0, -self.demiEpaisseur)

		glEnd()

		# Affichage des cotes

		glDisable(GL_TEXTURE_2D)

		glColor3f(0.0,0.0,0.0)

		glBegin(GL_QUADS)

		glVertex3f(0.0, 0.0, self.demiEpaisseur)
		glVertex3f(0.0, self.hauteur, self.demiEpaisseur)
		glVertex3f(0.0, self.hauteur, -self.demiEpaisseur)
		glVertex3f(0.0, 0.0, -self.demiEpaisseur)

		glVertex3f(self.largeur, 0.0, self.demiEpaisseur)
		glVertex3f(self.largeur, 0.0, -self.demiEpaisseur)
		glVertex3f(self.largeur, self.hauteur, -self.demiEpaisseur)
		glVertex3f(self.largeur, self.hauteur, self.demiEpaisseur)


		glEnd(GL_QUADS)



		glEnable(GL_TEXTURE_2D)

		


if __name__ == '__main__' : 
	r = Rectangle(hauteur=1.0)
	print r


		


	






