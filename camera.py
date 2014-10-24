# -*- coding: utf-8 -*-

import pyglet
from pyglet.gl import *

import math
import vec3



def deg2rad(d):
	return math.pi*d/180.0

class Camera : 

	sub = False

	def __init__(self):
		self.positionOeil = -15.0,1.6,-15.0
		self.directionVisee = 0.0
		self.hauteurVisee = 0.0
		self.pointVisee = 5.0, 1.6, 0.0
		self.vitesseOeil = 0.0
		self.sensDeplacement = 1.0
		self.vitesseMax=10.0
	
	## switch vue subjective
	def positionSubjective(self):
		if (self.sub == False) :
			self.hauteurVisee = -3.0
			self.positionOeil = 10.0,35,10.0
			self.sub = True
		else :
			self.positionOeil = 5.0,1.6,5.0
			self.hauteurVisee = 0.0
			self.sub=False

		

	def parametresCamera(self):
		ex, ey,ez = self.positionOeil
		dx, dy, dz = math.cos(self.directionVisee), self.hauteurVisee, math.sin(self.directionVisee)
	
		self.pointVise = ex + dx, ey+dy, ez+dz

		

	def placer(self):
		ex, ey,ez = self.positionOeil
		dx, dy, dz = math.cos(self.directionVisee), self.hauteurVisee, math.sin(self.directionVisee)
	
		self.pointVise = ex + dx, ey+dy, ez+dz

		glLoadIdentity()
		gluLookAt(ex,ey,ez, ex+dx,ey+dy,ez+dz, 0.0,1.0,0.0)


	def rotationCamera(self,angleDegre):
		angleRadian = deg2rad(angleDegre)
		self.directionVisee += angleRadian

	def rotationCameraY(self,angleDegre):
		angleRadian = deg2rad(angleDegre)
		self.hauteurVisee+=angleRadian

	def accelerer(self,pas):
		self.vitesseOeil = min(self.vitesseOeil + pas, self.vitesseMax)

	def deccelerer(self,pas):
		self.vitesseOeil = max(self.vitesseOeil - pas, 0.0)

	def pilerSurPlace(self):
		global vitesseOeil
		self.vitesseOeil = 0.0

	def enAvant(self):
		self.sensDeplacement = 1.0

	def enArriere(self):
		self.sensDeplacement = -1.0

	def update(self,dt):
		ex, ey, ez = self.positionOeil
		r = self.sensDeplacement*self.vitesseOeil*dt
		dx, dy, dz = r*math.cos(self.directionVisee), 0.0, r*math.sin(self.directionVisee)
		self.positionOeil = ex + dx, ey + dy, ez + dz
