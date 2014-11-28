# -*- coding: utf-8 -*-
import math

import pyglet
from pyglet.gl import *

import geo

import visu.wavefront

def vec(*args):
	return (GLfloat * len(args))(*args)

class TextureCatalog(object):
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(TextureCatalog, cls).__new__(
					cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		self.catalog = {}

	def loadTexture(self,nom):

		if self.catalog.has_key(nom):
			return self.catalog[nom]
		else:
			image = pyglet.image.load(nom)
			texture = image.get_texture()
			glBindTexture(GL_TEXTURE_2D,texture.id)
			glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
			glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
			self.catalog[nom] = texture
			return texture



class Materiau : 

	def __init__(self):
		self.kd_rouge = 0.0
		self.kd_vert  = 0.0
		self.kd_bleu  = 0.0
		self.kd_alpha = 0.0
		self.ka_rouge = 0.0
		self.ka_vert  = 0.0
		self.ka_bleu  = 0.0
		self.ka_alpha = 0.0
		
	def appliques(self):
		glMaterialf(GL_FRONT,GL_DIFFUSE,self.kd_rouge, self.kd_vert, self.kd_bleu, self.kd_alpha)
		
	def fixes_diffus(self,rouge,vert,bleu,alpha):
		self.kd_rouge = rouge
		self.kd_vert  = vert
		self.kd_bleu  = bleu
		self.kf_alpha = alpha

class Noeud :

	def __init__(self):
		self.perceptible = True
		self.translation = geo.vec3.zero()
		self.cap         = 0.0 # cap donne en degres
		
	def fixes_translation(self,tx,ty,tz):
		self.translation.setCoordonnees(x=tx,y=ty,z=tz)
		
	def fixes_position(self,p):
		self.translation.copier(p) 
		
	def fixes_cap(self,angle_en_radians):
		self.cap = angle_en_radians * 180.0 / math.pi
		
		
	def appliques_transfo(self):
		glTranslatef(self.translation.x, self.translation.y, self.translation.z)
		glRotatef(self.cap,0.0,0.0,1.0)
		
		

class Groupe(Noeud):

	def __init__(self):
		Noeud.__init__(self)
		self.fils = []
		
	def dessines_toi(self):
		self.appliques_transfo()
		for x in self.fils :
			glPushMatrix()
			x.dessines_toi()
			glPopMatrix()
			
	def enregistres(self,n):
		self.fils.append(n)
		

class ObjetDecore(Noeud):

	def __init__(self):
		Noeud.__init__(self)
		self.kd_rouge = 0.0
		self.kd_vert  = 0.0
		self.kd_bleu  = 0.0
		self.kd_alpha = 0.0
		self.ka_rouge = 0.0
		self.ka_vert  = 0.0
		self.ka_bleu  = 0.0
		self.ka_alpha = 0.0
		
	
	def dessines_toi(self):
		self.appliques_materiau()
		self.dessines_forme()
			
	def appliques_materiau(self):
		glMaterialfv(GL_FRONT,GL_DIFFUSE,vec(self.kd_rouge, self.kd_vert, self.kd_bleu, self.kd_alpha))
		
	def fixes_diffus(self,rouge,vert,bleu,alpha):
		self.kd_rouge = rouge
		self.kd_vert  = vert
		self.kd_bleu  = bleu
		self.kf_alpha = alpha
		
		
class Sphere(ObjetDecore):

	def __init__(self):
		ObjetDecore.__init__(self)
		self.q = gluNewQuadric()
		gluQuadricDrawStyle(self.q,GLU_FILL)
		
	def dessines_forme(self):
		gluSphere(self.q,1.0,16,16)
		

class Tableau(Noeud) : 
	def __init__(self,**attributs):
		Noeud.__init__(self)
		self.visible = True
		recto = attributs.get('recto',"../data/textures/dante.jpg")
		self.recto = TextureCatalog().loadTexture(recto)
		verso = attributs.get('verso',"../data/textures/dante.jpg")
		self.verso = TextureCatalog().loadTexture(verso)
		self.largeur = attributs.get('largeur',1.0)
		self.hauteur = attributs.get('hauteur',1.0)
		self.epaisseur = attributs.get('epaisseur',0.01)

	def dessines_toi(self):
		if self.perceptible:
		
			self.appliques_transfo()
		
			glPushMatrix()
			glScalef(self.epaisseur,self.largeur/2.0,self.hauteur/2.0)

			glBindTexture(GL_TEXTURE_2D,self.recto.id)
			glBegin(GL_QUADS)
			glTexCoord2f(0.0, 0.0)
			glVertex3f(1.0, -1.0, -1.0)
			glTexCoord2f(1.0, 0.0)
			glVertex3f(1.0, 1.0, -1.0)
			glTexCoord2f(1.0, 1.0)
			glVertex3f(1.0, 1.0, 1.0)
			glTexCoord2f(0.0, 1.0)
			glVertex3f(1.0, -1.0, 1.0)
			glEnd()



			glPopMatrix()


class TableauFond(Noeud) : 
	def __init__(self,**attributs):
		Noeud.__init__(self)
		self.visible = True
		recto = attributs.get('recto',"../data/textures/dante.jpg")
		self.recto = TextureCatalog().loadTexture(recto)
		verso = attributs.get('verso',"../data/textures/dante.jpg")
		self.verso = TextureCatalog().loadTexture(verso)
		self.largeur = attributs.get('largeur',1.0)
		self.hauteur = attributs.get('hauteur',1.0)
		self.epaisseur = attributs.get('epaisseur',0.01)

	def dessines_toi(self):
		if self.perceptible:
		
			self.appliques_transfo()
		
			glPushMatrix()
			glScalef(self.epaisseur,self.largeur/2.0,self.hauteur/2.0)

			glBindTexture(GL_TEXTURE_2D,self.recto.id)
			glBegin(GL_QUADS)
			glTexCoord2f(0.0, 0.0)
			glVertex3f(1.0, -1.0, -1.0)
			glTexCoord2f(1.0, 0.0)
			glVertex3f(1.0, 1.0, -1.0)
			glTexCoord2f(1.0, 1.0)
			glVertex3f(1.0, 1.0, 1.0)
			glTexCoord2f(0.0, 1.0)
			glVertex3f(1.0, -1.0, 1.0)
			glEnd()

			glBindTexture(GL_TEXTURE_2D,self.verso.id)

			glBegin(GL_QUADS)
			glTexCoord2f(0.0, 0.0)
			glVertex3f(0.0, 1.0, -1.0)
			glTexCoord2f(1.0, 0.0)
			glVertex3f(0.0, -1.0, -1.0)
			glTexCoord2f(1.0, 1.0)
			glVertex3f(0.0, -1.0, 1.0)
			glTexCoord2f(0.0, 1.0)
			glVertex3f(0.0, 1.0, 1.0)
			glEnd()

			glPopMatrix()



		
class Obj(Noeud):
	def __init__(self,**attributs):
		Noeud.__init__(self)
		self.url = attributs.get("url","../data/obj/pingouin/p.obj")
		self.model = visu.wavefront.WavefrontModel()
		self.model.LoadFile(self.url)

	def dessines_toi(self):
		if self.perceptible:
			self.appliques_transfo()
			self.model.Draw()


class ObjY(Noeud):
	def __init__(self,**attributs):
		Noeud.__init__(self)
		self.url = attributs.get("url","../data/obj/pingouin/p.obj")
		self.model = visu.wavefront.WavefrontModel()
		self.model.LoadFile(self.url)

	def dessines_toi(self):
		if self.perceptible:
			self.appliques_transfo()
			glPushMatrix()
			glRotatef(90.0,1.0,0.0,0.0)
			self.model.Draw()
			glPopMatrix()
		
		
class Sol(Noeud) : 
	def __init__(self,**attributs):
		Noeud.__init__(self)
		self.size   = attributs.get('size',500)
		textureName = attributs.get('texture','../data/textures/moquette.jpg')
		self.texture = TextureCatalog().loadTexture(textureName)
		# self.facteurTexture = getVal(attr,float,"facteurTexture",1.0)
	
	def dessines_toi(self):

		#size = self.size
		if self.perceptible:
		
			self.appliques_transfo()
			size=100
			fz = 1.0
		
			glBindTexture(GL_TEXTURE_2D,self.texture.id)
			glBegin(GL_QUADS)
			glTexCoord2f(0.0,0.0)
			glVertex3f(-size,-size,0.0)
			glTexCoord2f(size,0.0)
			glVertex3f(size,-size,0.0)
			glTexCoord2f(size,size)
			glVertex3f(size,size,0.0)
			glTexCoord2f(0.0,size)
			glVertex3f(-size,size,0.0)
			glEnd()
			
class Ciel(Noeud):
		def __init__(self,**attributs):
			Noeud.__init__(self)
			self.size = attributs.get('size',500.0)
	
			textureName = attributs.get('texture','../data/skyboxes/ciel.jpg')
			image = pyglet.image.load(textureName)
			imageSeq = pyglet.image.ImageGrid(image, 3, 4)
			self.textureUP = imageSeq[9].get_texture()
			self.textureDN = imageSeq[1].get_texture()
			self.textureLT = imageSeq[4].get_texture()
			self.textureFT = imageSeq[5].get_texture()
			self.textureRT = imageSeq[6].get_texture()
			self.textureBK = imageSeq[7].get_texture()
			self.textureFactor = 1.0	
	
		def dessines_toi(self):
				if self.perceptible :
				
					self.appliques_transfo()
					
					size = self.size
					halfsize = (size/2)
					halfsizec = halfsize*1.01 #halfsize corrected
					tf = self.textureFactor
		
					glPushMatrix()
					glRotatef(90.0,1.0,0.0,0.0)

					# Up
					glBindTexture(GL_TEXTURE_2D,self.textureUP.id)
					glBegin(GL_QUADS)
					glTexCoord2f(0.0,0.0)
					glVertex3f(-halfsizec,halfsize,-halfsizec)
					glTexCoord2f(1.0,0.0)
					glVertex3f(halfsizec,halfsize,-halfsizec)
					glTexCoord2f(1.0,1.0)
					glVertex3f(halfsizec,halfsize,halfsizec)
					glTexCoord2f(0.0,1.0)
					glVertex3f(-halfsizec,halfsize,halfsizec)
					glEnd()
					# Down
					glBindTexture(GL_TEXTURE_2D,self.textureDN.id)
					glBegin(GL_QUADS)
					glTexCoord2f(0.0,0.0)
					glVertex3f(-halfsizec,-halfsize,halfsizec)
					glTexCoord2f(1.0,0.0)
					glVertex3f(halfsizec,-halfsize,halfsizec)
					glTexCoord2f(1.0,1.0)
					glVertex3f(halfsizec,-halfsize,-halfsizec)
					glTexCoord2f(0.0,1.0)
					glVertex3f(-halfsizec,-halfsize,-halfsizec)
					glEnd()
					# Left
					glBindTexture(GL_TEXTURE_2D,self.textureLT.id)
					glBegin(GL_QUADS)
					glTexCoord2f(0.0,0.0)
					glVertex3f(-halfsize,-halfsizec,halfsizec)
					glTexCoord2f(1.0,0.0)
					glVertex3f(-halfsize,-halfsizec,-halfsizec)
					glTexCoord2f(1.0,1.0)
					glVertex3f(-halfsize,halfsizec,-halfsizec)
					glTexCoord2f(0.0,1.0)
					glVertex3f(-halfsize,halfsizec,halfsizec)
					glEnd()
					# Front
					glBindTexture(GL_TEXTURE_2D,self.textureFT.id)
					glBegin(GL_QUADS)
					glTexCoord2f(0.0,0.0)
					glVertex3f(-halfsizec,-halfsizec,-halfsize)
					glTexCoord2f(1.0,0.0)
					glVertex3f(halfsizec,-halfsizec,-halfsize)
					glTexCoord2f(1.0,1.0)
					glVertex3f(halfsizec,halfsizec,-halfsize)
					glTexCoord2f(0.0,1.0)
					glVertex3f(-halfsizec,halfsizec,-halfsize)
					glEnd()
					# Right
					glBindTexture(GL_TEXTURE_2D,self.textureRT.id)
					glBegin(GL_QUADS)
					glTexCoord2f(0.0,0.0)
					glVertex3f(halfsize,-halfsizec,-halfsizec)
					glTexCoord2f(1.0,0.0)
					glVertex3f(halfsize,-halfsizec,halfsizec)
					glTexCoord2f(1.0,1.0)
					glVertex3f(halfsize,halfsizec,halfsizec)
					glTexCoord2f(0.0,1.0)
					glVertex3f(halfsize,halfsizec,-halfsizec)
					glEnd()
					# Back
					glBindTexture(GL_TEXTURE_2D,self.textureBK.id)
					glBegin(GL_QUADS)
					glTexCoord2f(0.0,0.0)
					glVertex3f(halfsizec,-halfsizec,halfsize)
					glTexCoord2f(1.0,0.0)
					glVertex3f(-halfsizec,-halfsizec,halfsize)
					glTexCoord2f(1.0,1.0)
					glVertex3f(-halfsizec,halfsizec,halfsize)
					glTexCoord2f(0.0,1.0)
					glVertex3f(halfsizec,halfsizec,halfsize)
					glEnd()

					glPopMatrix()
		

