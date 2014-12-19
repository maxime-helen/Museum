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

import __builtin__


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
__builtin__.buffer_salle = {}
laCamera = None
ex = acteur.ActorSteering(-15.0,-15.0,'pingouin/p.obj')
ex.arriveOn()
ex1 = acteur.ActorSteering(-15.0,5.0,'pingouin/p.obj')
ex1.arriveOn()
ex2 = acteur.ActorSteering(5.0,-15.0,'pingouin/p.obj')
ex2.arriveOn()
ex3 = acteur.ActorSteering(-5.0,15.0,'pingouin/p.obj')
ex3.arriveOn()
ex4 = acteur.ActorSteering(-15.0,-5.0,'pingouin/p.obj')
ex4.arriveOn()
ex5 = acteur.ActorSteering(5.0,5.0,'pingouin/p.obj')
ex5.arriveOn()
ex6 = acteur.ActorSteering(5.0,-5.0,'pingouin/p.obj')
ex6.arriveOn()


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
	laCamera.placer()
	ex.update(0.1)
	ex1.update(0.1)
	ex2.update(0.1)
	ex3.update(0.1)
	ex4.update(0.1)
	ex5.update(0.1)
	ex6.update(0.1)
	for obj in scene() :
		obj.draw()
	
	for key in __builtin__.buffer_salle :
		__builtin__.buffer_salle[key]=[]

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
	
	setup()

	# La fonction update sera appelee toutes les 30eme de seconde
        pyglet.clock.schedule_interval(update, 1.0/30.0)

    	print '*****************************************************README*************************************************************'
   	print 'SEVEN PINGOUIN ACTORS FIRE <ARRIVE> PROCEDURE FROM DIFFERENT POSITIONS'
	print 'ONCE THEY REACH A ROOM, <STEERING> PROCEDURE IS FIRED'
	print 'IF ANY ROOMS HAVE PAINTS, ACTOR WILL ADMIRE EVERY DRAWS OVER <STEERING> PROCEDURE AND WILL TAKE OVER <ARRIVE> AT THE END'
	print 'IF ANY ROOMS ARE HALLS, ACTOR WILL FIRE <ARRIVE> PROCEDURE AUTOMATICALLY ONCE THE HALL REACHED'
	print 'IMPORTANT: PRESS "A" FOR CHECKING OUT THOSE PINGUIN BEHAVIORS UNDER A GLOBAL VIEW'
	print 'IMPORTANT: PRESS "A" FOR CHECKING OUT THOSE PINGUIN BEHAVIORS UNDER A GLOBAL VIEW'
	print 'IMPORTANT: PRESS "A" FOR CHECKING OUT THOSE PINGUIN BEHAVIORS UNDER A GLOBAL VIEW'
	print 'ENJOY'
	print 'TEFA CP - ZeZen - Manchette - December 2014'
	print '************************************************************************************************************************'

	pyglet.app.run()

