#! /usr/bin/python

import pyglet
from pyglet.gl import *

import math


import primitives as prims
import vec3
import camera
import parse
import wavefront
import acteur 


# Variables globales
#  -----------------

try:
	config = Config(sample_buffer=1, samples=4, \
          depth_size=16, double_buffer=True)
	window = pyglet.window.Window(resizable=True, config=config)
except:
	window = pyglet.window.Window(resizable=True)


horloge=0.0
scene = []
textures={}
laCamera = None
# pingouin = wavefront.WavefrontModel()
# pingouin.LoadFile('pingouin/p.obj', 1)
ex = acteur.ActorSteering(-15.0,-15.0,'pingouin/p.obj')
ex.arriveOn()

def setup():

	
	global textures
	global scene
	global laCamera
	
	glEnable(GL_DEPTH_TEST)

	glEnable(GL_TEXTURE_2D)
	glAlphaFunc(GL_GREATER,0.4)
	glEnable(GL_ALPHA_TEST)

	
	laCamera = camera.Camera()
	scene = parse.parser('scene.xml')



@window.event
def on_resize(width, height):
    # Override the default on_resize handler to create a 3D projection
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, width / float(height), .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED


@window.event
def on_draw():
	global scene

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	# Placement de la camera
	
	#glLoadIdentity()
	#gluLookAt( 0.0, 1.6, 8.0, 0.0, 1.6, 0.0, 0.0,1.0,0.0)
	laCamera.placer()
	ex.update(0.1)
	# glPushMatrix()
	# glRotatef(90.0,-1.0,0.0,0.0)
	# glTranslatef(-15.0, 15.0,0.0)
	# pingouin.Draw()
	# glPopMatrix()
	for obj in scene() :
		obj.draw()


@window.event
def on_key_press(symbol,modifiers):
	if symbol == pyglet.window.key.Q:
		pass
	elif symbol == pyglet.window.key.LEFT : # Fleche gauche 
		laCamera.enArriere()
	elif symbol == pyglet.window.key.RIGHT : # Fleche droite 
		laCamera.enAvant()
	elif symbol == pyglet.window.key.UP : # Fleche haut
		laCamera.accelerer(0.5)
	elif symbol == pyglet.window.key.DOWN : # fleche bas
		laCamera.deccelerer(0.5)
	elif symbol == pyglet.window.key.SPACE :
		laCamera.pilerSurPlace()

	elif symbol == pyglet.window.key.A : 
		laCamera.positionSubjective()


@window.event
def on_mouse_press(x,y,bouton,modifiers):
	pass


@window.event
def on_mouse_drag(x,y,dx,dy,boutons,modifiers):
	laCamera.rotationCamera(dx)
	# laCamera.rotationCameraY(dy)


def update(dt):
	global horloge

	horloge = horloge + dt

	laCamera.update(dt)
	





	
	

if __name__ == "__main__":
	
	print "Hello World"
	setup()

	# La fonction update sera appelee toutes les 30eme de seconde
        pyglet.clock.schedule_interval(update, 1.0/30.0)

	pyglet.app.run()
