import vec3
import wavefront
import graphe
from pyglet.gl import *

class Actor(object) :
	def __init__(self,x,y,url):
		self.null = vec3.Vec3()
		self.currentPosition = vec3.Vec3(0.0,0.0,0.0)
		self.originPosition = vec3.Vec3(x,y,0.0)
		self.url = url
		self.model = wavefront.WavefrontModel()
		self.model.LoadFile('pingouin/p.obj', 1)
		self.currentPosition.vers(self.null,self.originPosition)

	def update(self):
		print 'wew'
		# glPushMatrix()
		# glRotatef(90.0,-1.0,0.0,0.0)
		# glTranslatef(self.currentPosition.x,-self.currentPosition.y,0.0)
		# self.draw()
		# glPopMatrix()

	def draw(self):
		self.model.Draw()

class ActorSteering(Actor) :
	def __init__(self,x,y,url):
		self.STEERING = False
		self.ARRIVE = False
		self.position = vec3.Vec3()
		self.graph = graphe.Dijkstra(graphe.lireGrapheNavigation("graphe.nav"))
		self.road = self.graph.trouverChemin(de="p00",a="p33")
		self.index = 1
		Actor.__init__(self,x,y,url)
	def update(self,dt):
		# super(ActorSteering,self).update()
		glPushMatrix()
		glRotatef(90.0,-1.0,0.0,0.0)
		glTranslatef(self.currentPosition.x,-self.currentPosition.y,0.0)
		if self.STEERING :
			print "STEERING"
		elif self.ARRIVE and self.index!=len(self.road):
			self.currentPosition.goto(0.1,self.road[self.index])
			print self.currentPosition,self.road[self.index], self.currentPosition.compare(self.road[self.index],0.1)
			if self.currentPosition.compare(self.road[self.index],0.1) : self.index+=1
		super(ActorSteering,self).draw()
		glPopMatrix()
	def setTarget(self,vec):
		self.target = vec
	def seekOn(self) :
		self.STEERING = True
	def seekOff(self) :
		self.STEERING = False
	def arriveOn(self) :
		self.ARRIVE = True
		self.road = self.graph.trouverChemin(self.graph.getNameByPosition(self.currentPosition),"p33")
	def arriveOff(self) :
		self.ARRIVE = False
		road = None