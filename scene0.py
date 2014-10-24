
import math
import vec3
import primitives as prims


def deg2rad(d):
	return math.pi * d / 180.0



class Poster : 
	def __init__(self,unAnnuaire,\
                          largeur=0.85,hauteur=1.417,epaisseur=0.1,\
                          nomPoster="chene", nomCadre="chene"):
		self.boite = prims.Boite(unAnnuaire,largeur=largeur,hauteur=hauteur,profondeur=epaisseur)
                unPoster.ajouterUneFace("avant",nomPoster)
		unPoster.ajouterUneFace("haut","chene")
		unPoster.ajouterUneFace("bas","chene")
		unPoster.ajouterUneFace("gauche","chene")
		unPoster.ajouterUneFace("droite","chene")
		self.unGroupe = prims.Groupe()
		tx, ty, tz = position
		self.unGroupe.transformer(-largeur/2.0,0.0,epaisseur)                      

	def draw(self):
		self.unGroupe.draw()

class PosterPlace : 
	def __init__(self,position=(0.0,0.0,0.0),angle=0.0, poster=None):
		if poster == None :
			self.poster = None
		else:
			self.poster = prims.Groupe()
			self.poster.addChild(poster)
			self.poster.transformer(translation=position, rotation=(angle,0.0,1.0,0.0))

	def draw(self):
		if self.poster != None :
			self.poster.draw()
		
		
		
		




 
def alignementPosters(annuaire,listeNomsPosters, dx = 1.5, translation=(0.0,0.0,0.0), angleRotation=0.0):
	i = 0
	alignement = prims.Groupe()
	for nomPoster in listeNomsPosters:
		unPoster = prims.Boite(annuaire,largeur=0.85, hauteur=1.417, profondeur=0.05)
		unPoster.ajouterUneFace("avant",nomPoster)
		unPoster.ajouterUneFace("haut","chene")
		unPoster.ajouterUneFace("bas","chene")
		unPoster.ajouterUneFace("gauche","chene")
		unPoster.ajouterUneFace("droite","chene")
		unGroupe = prims.Groupe()
		unGroupe.transformer(translation=(i*dx,0.8,0.0))
		i = i+1
		unGroupe.addChild(unPoster)
		alignement.addChild(unGroupe)	

	alignement.transformer(translation=translation,rotation=(angleRotation,0.0,1.0,0.0))

	return alignement

def chargerTexturesPosters(annuaire,exposition,suffixe,listeNoms):
	for nom in listeNoms : 
		uneTexture = prims.Texture(annuaire,nom,exposition+nom+suffixe)

def creer() : 
	unAnnuaire = prims.creerAnnuaire()

	laScene = prims.Scene()

	uneTexture = prims.Texture(unAnnuaire,"romantisme","data/tableaux/romantisme.jpg")
	uneTexture = prims.Texture(unAnnuaire,"panneau1","data/textures/cloisons/japan_012-1024x854.jpg")
	uneTexture = prims.Texture(unAnnuaire,"dante","data/textures/murs/dante-475x709.jpg")
	uneTexture = prims.Texture(unAnnuaire,"plancher","data/textures/bois/wood-1280x1024.jpg")
	uneTexture = prims.Texture(unAnnuaire,"acajou","data/textures/bois/acajou.png")
	uneTexture = prims.Texture(unAnnuaire,"chene", "data/textures/bois/015chenef.jpg")
	unAnnuaire.ajouter("rouge",prims.Rvb(1.0,0.0,0.0))

	exposition = "data/expositions/laser/"
	jpg = ".jpg"
	listeNoms = ["appli0","appli1","appli2","appli3","titre0","titre1","histo0"]
	listeNoms = listeNoms + ["laser0", "laser1", "laser2", "laser3", "laser4"]
	listeNoms = listeNoms + ["lum0","lum1","lum2","lum3"]
	chargerTexturesPosters(unAnnuaire,exposition,jpg,listeNoms)

	
	posters1 = alignementPosters(unAnnuaire,["titre1","titre0"],translation=(2.5,0.0,2.55), dx = 1.3)
	laScene.addChild(posters1)

	posters2 = alignementPosters(unAnnuaire,["histo0"], translation=(-1.5,0.0,2.55), dx = 1.3)
	laScene.addChild(posters2)

	posters3 = alignementPosters(unAnnuaire,["laser1","laser0"], translation=(-2.3,0.0,-2.4), dx = 1.3)
	laScene.addChild(posters3)

	posters4 = alignementPosters(unAnnuaire,["laser4","laser3","laser2"], translation=(-2.3,0.0,2.0),angleRotation=90.0)
	laScene.addChild(posters4)
	
	posters5 = alignementPosters(unAnnuaire,["lum3","lum2","lum1","lum0"],translation=(2.4,0.0,-4.8),angleRotation=-90.0,dx=1.3)
	laScene.addChild(posters5)

	posters6 = alignementPosters(unAnnuaire,["appli0","appli1","appli2","appli3"],translation=(-2.6,0.0,-2.3),angleRotation=-90.0,dx=1.3)
	laScene.addChild(posters6)

	# laScene.addChild(AlignementDePosters(unAnnuaire,listeNomsPosters=["appli0","appli1","appli2","appli3"], angle=-90.0))
	


	leSol = prims.Boite(unAnnuaire,largeur=10.0, hauteur=0.1,profondeur=10.0)
	leSol.ajouterUneFace("haut","plancher")
	unGroupe = prims.Groupe()
	unGroupe.addChild(leSol)
	unGroupe.transformer(translation=(-4.9,-0.1,5.0))
	laScene.addChild(unGroupe)

	lePlafond = prims.Boite(unAnnuaire,largeur=10.0, hauteur=0.1,profondeur=10.0)
	lePlafond.ajouterUneFace("bas","acajou")
	unGroupe = prims.Groupe()
	unGroupe.addChild(lePlafond)
	unGroupe.transformer(translation=(-4.9,5.0,5.0))
	laScene.addChild(unGroupe)

	murOuest = prims.Boite(unAnnuaire,largeur=0.1, hauteur=5.0,profondeur=10.0)
	murOuest.ajouterUneFace("droite","panneau1")
	unGroupe = prims.Groupe()
	unGroupe.addChild(murOuest)
	unGroupe.transformer(translation=(-5.0,0.0,5.0))
	laScene.addChild(unGroupe)

	
	murEst = prims.Boite(unAnnuaire,largeur=0.1, hauteur=5.0,profondeur=10.0)
	murEst.ajouterUneFace("gauche","dante")
	unGroupe = prims.Groupe()
	unGroupe.addChild(murEst)
	unGroupe.transformer(translation=(5.0,0.0,5.0))
	laScene.addChild(unGroupe)

	murNord = prims.Boite(unAnnuaire,largeur=10.1, hauteur=5.0,profondeur=0.1)
	murNord.ajouterUneFace("avant","panneau1")
	unGroupe = prims.Groupe()
	unGroupe.addChild(murNord)
	unGroupe.transformer(translation=(-5.0,0.0,-5.0))
	laScene.addChild(unGroupe)

	murSud = prims.Boite(unAnnuaire,largeur=10.1,hauteur=5.0,profondeur=0.1)
	murSud.ajouterUneFace("arriere","dante")
	unGroupe = prims.Groupe()
	unGroupe.addChild(murSud)
	unGroupe.transformer(translation=(-5.0,0.0,5.1))
	laScene.addChild(unGroupe)

	cloison1 = prims.Boite(unAnnuaire,largeur=2.5, hauteur= 5.0, profondeur=0.1)
	cloison1.ajouterUneFace("avant","dante")
	cloison1.ajouterUneFace("arriere","dante")
	cloison1.ajouterUneFace("gauche","dante")
	cloison1.ajouterUneFace("droite","dante")
	groupe1 = prims.Groupe()
	groupe1.transformer(translation=(-2.5,0.0,2.5))
	groupe1.addChild(cloison1)
	laScene.addChild(groupe1)

	cloison2 = prims.Boite(unAnnuaire,largeur=0.1, hauteur=5.0, profondeur=4.9)
	cloison2.ajouterUneFace("gauche","acajou")
	cloison2.ajouterUneFace("droite","acajou")
	groupe2 = prims.Groupe()
	groupe2.transformer(translation=(-2.5,0.0,2.4))
	groupe2.addChild(cloison2)
	laScene.addChild(groupe2)

	cloison3 = prims.Boite(unAnnuaire,largeur=0.1, hauteur=5.0, profondeur=2.4)
	cloison3.ajouterUneFace("gauche","acajou")
	cloison3.ajouterUneFace("droite","acajou")
	cloison3.ajouterUneFace("arriere","acajou")
	groupe3 = prims.Groupe()
	groupe3.transformer(translation=(-0.1,0.0,2.4))
	groupe3.addChild(cloison3)
	laScene.addChild(groupe3)

	cloison4 = prims.Boite(unAnnuaire,largeur=2.5, hauteur= 5.0, profondeur=0.1)
	cloison4.ajouterUneFace("avant","dante")
	cloison4.ajouterUneFace("arriere","dante")
	cloison4.ajouterUneFace("gauche","dante")
	cloison4.ajouterUneFace("droite","dante")
	groupe4 = prims.Groupe()
	groupe4.transformer(translation=(-2.5,0.0,-2.5))
	groupe4.addChild(cloison4)
	laScene.addChild(groupe4)

	cloison6 = prims.Boite(unAnnuaire,largeur=2.5, hauteur= 2.5, profondeur=0.1)
	cloison6.ajouterUneFace("avant","dante")
	cloison6.ajouterUneFace("arriere","dante")
	cloison6.ajouterUneFace("gauche","dante")
	cloison6.ajouterUneFace("droite","dante")
	groupe6 = prims.Groupe()
	groupe6.transformer(translation=(2.5,0.0,2.5))
	groupe6.addChild(cloison6)
	laScene.addChild(groupe6)


	cloison7 = prims.Boite(unAnnuaire,largeur=0.1,hauteur=2.5,profondeur=5.0)
	cloison7.ajouterUneFace("gauche","acajou")
	cloison7.ajouterUneFace("droite","acajou")
	cloison7.ajouterUneFace("avant","acajou")
	groupe7 = prims.Groupe()
	groupe7.addChild(cloison7)
	groupe7.transformer(translation=(2.5,0.0,0.0))
	laScene.addChild(groupe7)

	mezzanine1 = prims.Boite(unAnnuaire,largeur=2.5, hauteur = 0.1, profondeur = 7.5)
	mezzanine1.ajouterUneFace("bas","plancher")
	mezzanine1.ajouterUneFace("gauche","plancher")
	mezzanine1.ajouterUneFace("avant","dante")
	mezzanine1.ajouterUneFace("haut","plancher")
	groupeMezzanine1 = prims.Groupe()
	groupeMezzanine1.addChild(mezzanine1)
	groupeMezzanine1.transformer(translation=(2.5,2.5,2.5))
	laScene.addChild(groupeMezzanine1)

	

	return laScene
