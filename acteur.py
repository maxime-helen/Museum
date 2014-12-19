import vec3
import wavefront
import graphe
import __builtin__
import random
from pyglet.gl import *

class Actor(object) :

	def __init__(self,x,y,url):
		self.null = vec3.Vec3()
		self.currentPosition = vec3.Vec3(0.0,0.0,0.0)
		self.originPosition = vec3.Vec3(x,y,0.0)
		self.url = url
		self.model = wavefront.WavefrontModel()
		self.model.LoadFile(url, 1)
		self.currentPosition.vers(self.null,self.originPosition)

	def update(self):
		return 0

	def draw(self):
		self.model.Draw()

class ActorSteering(Actor) :

	def __init__(self,x,y,url):
		self.STEERING = False
		self.ARRIVE = False
		self.position = vec3.Vec3()
		self.graph = graphe.Dijkstra(graphe.lireGrapheNavigation("graphe.nav"))
		self.indexArrive = 1
		self.indexSteering = 1
		self.angle = 0.0
		Actor.__init__(self,x,y,url)
		self.road = self.graph.trouverChemin(de=self.graph.getNameByPosition(vec3.Vec3(x,y,0.0)),a="p33")

	def getRandomRoom(self):
		return "p"+str(random.randint(0, 3))+str(random.randint(0, 3))

	def getRotation(self,index):
		tmp = 1
		if self.currentPosition.x<self.road[index].x and self.currentPosition.x==self.road[index].x:
			tmp = 0.0
		if self.currentPosition.x>self.road[index].x and self.currentPosition.x==self.road[index].x:
			tmp = 180.0
		if self.currentPosition.y<self.road[index].y and self.currentPosition.x==self.road[index].x:
			tmp = 270.0
		if self.currentPosition.y>self.road[index].y and self.currentPosition.x==self.road[index].x:
			tmp = 90.0
		if self.currentPosition.y>self.road[index].y and self.currentPosition.x>self.road[index].x:
			tmp = 125.0
		if self.currentPosition.y<self.road[index].y and self.currentPosition.x<self.road[index].x:
			tmp = 315.0
		if self.currentPosition.y>self.road[index].y and self.currentPosition.x<self.road[index].x:
			tmp = 225.0
		if self.currentPosition.y<self.road[index].y and self.currentPosition.x>self.road[index].x:
			tmp = 45.0
		return tmp

	def update(self,dt):
		glPushMatrix()
		glRotatef(90.0,-1.0,0.0,0.0)
		glTranslatef(self.currentPosition.x,-self.currentPosition.y,0.0)
		if self.STEERING and self.indexSteering<len(self.road):
			self.currentPosition.goto(0.1,self.road[self.indexSteering])
			glRotatef(self.getRotation(self.indexSteering),0.0,0.0,1.0)
			if self.currentPosition.compare(self.road[self.indexSteering],0.1) : 
				self.currentPosition = self.road[self.indexSteering].round()
				self.indexSteering += 1
		elif self.ARRIVE and self.indexArrive<len(self.road):
			self.currentPosition.goto(0.1,self.road[self.indexArrive])
			glRotatef(self.getRotation(self.indexArrive),0.0,0.0,1.0)
			if self.currentPosition.compare(self.road[self.indexArrive],0.1) :
				self.currentPosition = self.road[self.indexArrive].round()
				self.indexArrive+=1
				self.arriveOff()
				self.seekOn()
		else :
			self.seekOff()
			self.arriveOff()
			self.arriveOn()
		super(ActorSteering,self).draw()
		glPopMatrix()

	def seekOn(self) :
		self.road = __builtin__.buffer_salle[self.graph.getNameByPosition(self.currentPosition.round())];
		self.indexArrive = 1
		self.indexSteering = 1
		self.ARRIVE = False
		self.STEERING = True

	def seekOff(self) :
		self.road = None
		self.indexArrive = 1
		self.indexSteering = 1
		self.STEERING = False

	def arriveOn(self) :
		self.road = self.graph.trouverChemin(de=self.graph.getNameByPosition(self.currentPosition.round()),a="p33")
		self.indexArrive = 1
		self.indexSteering = 1
		self.STEERING = False
		self.ARRIVE = True

	def arriveOff(self) :
		self.indexArrive = 1
		self.indexSteering = 1
		self.road = None
		self.STEERING = False
		self.ARRIVE = False