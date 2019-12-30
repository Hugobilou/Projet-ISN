from tkinter import*
from PIL import Image
from scipy import *

def fonction_déplacement(event): ## fonction de déplacement
    global coords,variable_saut, Image_hero_, sens_hero,sur_platform,en_saut
    touche = event.keysym ## traduit la touche presser en chaine de caractère

    if coords[1]==620: ## débloque le saut si on est au sol
        en_saut=0
    if touche == "z" and en_saut==0 : ## on détecte si on appuie sur la touche "z"
        variable_saut=0
        sur_platform=1
        en_saut=1
        saut2()
    elif touche == "d" and coords[0]<(coords_rectangle[2]-75): ## on détecte si on appuie sur la touche "d"
        coords = (coords[0] + 15, coords[1]) ## on modifie les coordonnées du perso
        if HeroMort==0:
            canvas.delete(Image_hero_)
            Image_hero_ = canvas.create_image(coords[0],coords[1], anchor=NW,image=Image_hero_droite)
            sens_hero=1
        if coords[0]>coords_rectangle[2]-75: ## on vérifie si on est en dehors de la fenêtre
            coords = coords_rectangle[2]-75,coords[1] ## on modifie les coordonnées du perso
    elif touche == "q" and coords[0]>coords_rectangle[0]: ## on détecte si on appuie sur la touche "q"
        coords = (coords[0] -15, coords[1]) ## on modifie les coordonnées du perso
        if HeroMort==0:
            canvas.delete(Image_hero_)
            Image_hero_ = canvas.create_image(coords[0],coords[1], anchor=NW,image=Image_hero_gauche)
            sens_hero=0
        if coords[0]<coords_rectangle[1]: ## on vérifie si on est en dehors de la fenêtre
            coords = coords_rectangle[1], coords[1] ## on modifie les coordonnées du perso
    elif touche== 's' and sur_platform==0: ## on détecte si on appuie sur la touche "s"
         coords=(coords[0],coords[1]+10) ## on modifie les coordonnées du perso
         canvas.coords(Image_hero_,coords[0],coords[1])

    canvas.coords(Image_hero_, coords[0], coords[1])
    if sur_platform==0:
        for i in range (0,len(tableau)): ##on vérifie si on sort de la plateforme
            if (tableau[i][0]<coords[0]<tableau[i][1])==False:
                variable_saut=15
                sur_platform=1
                saut2()


def saut2():
    global coords,sur_platform,variable_saut
    if variable_saut<15 : ## On fais monter le perso
        coords=(coords[0],coords[1]-10)
        canvas.coords(Image_hero_,coords[0],coords[1])
        fenetre.after(15,saut2)
        variable_saut=variable_saut+1

    elif coords[1]<620 and variable_saut==15 and sur_platform==1 : ## On descend le perso
        fenetre.after(0,platform()) ## On vérifie si le perso est sur une plateforme
        coords=(coords[0],coords[1]+10)
        canvas.coords(Image_hero_,coords[0],coords[1])
        fenetre.after(30,saut2)






def platform():
    global coords,sur_platform,en_saut
    for i in range (0,len(tableau)): ## On vérifie si le perso est sur une plateforme
        if (tableau[i][0]<coords[0]+25<tableau[i][1] or tableau[i][0]<coords[0]+45<tableau[i][1]) and coords[1]+120==tableau[i][2]:
            en_saut=0
            sur_platform=0
            coords=(coords[0],(tableau[i][2])-130)
            canvas.coords(Image_hero_,coords[0],coords[1])












def attaque (event):
    global coords,epee,en_attaque, HeroMort, sens_hero
    if en_attaque==0 and HeroMort == 0 and sens_hero == 1: ## On affiche l'épée a droite si on appuie sur f
        epee = canvas.create_image(coords[0]+50, coords[1]+60, anchor=NW, image=ImageEpee)
        en_attaque=1
        fenetre.after(200,attaque2) ## On supprime le l'épée au bout de 200 ms
        fenetre.after(0,mort_du_mechant)
    if en_attaque ==0 and HeroMort == 0 and sens_hero == 0 : ## On affiche l'épée a gauche si on appuie sur f
        epee = canvas.create_image(coords[0]-60, coords[1]+60, anchor=NW, image=ImageEpee2)
        en_attaque=1
        fenetre.after(200,attaque2) ## On supprime le l'épée au bout de 200 ms
        fenetre.after(0,mort_du_mechant)

def attaque2 ():
    global epee,en_attaque
    canvas.delete(epee)
    en_attaque=0





def deplacement_mechants (): ## Déplacement du méchant
    global coords_Mechant1,sens_mechant,ImageMechant1_,MechantMort
    if sens_mechant==0 and MechantMort==0: ## Boucle qui fais se déplacer le méchant vers la droite
        coords_Mechant1=(coords_Mechant1[0]-15, coords_Mechant1[1])
        if coords_Mechant1[0]== 300:
            sens_mechant=1
            canvas.delete(ImageMechant1_)
            ImageMechant1_ = canvas.create_image(coords_Mechant1[0],coords_Mechant1[1], anchor=NW,image=ImageMechant1v2)

    if sens_mechant==1 and MechantMort==0: ## Boucle qui fais se déplacer le méchant vers la gauche
        coords_Mechant1=(coords_Mechant1[0]+15, coords_Mechant1[1])
        if coords_Mechant1[0]== 1200:
            sens_mechant=0
            canvas.delete(ImageMechant1_)
            ImageMechant1_ = canvas.create_image(coords_Mechant1[0],coords_Mechant1[1], anchor=NW,image=ImageMechant1)

    fenetre.after(100,deplacement_mechants) ## On le déplace toute les 100 ms
    canvas.coords(ImageMechant1_,coords_Mechant1[0],coords_Mechant1[1])
    fenetre.after(0,dégat_héro_subis())



def mort_du_mechant ():
    global coords_Mechant1, vie_Mechant1, MechantMort, sens_hero
    if sens_hero == 1:
        for o in range (coords[0]+80,coords[0]+80+80+1) : ## On détecte si l'épée touche le méchant
            if (coords_Mechant1[0]<= o <=coords_Mechant1[0]+65) and (coords_Mechant1[1]<=  coords[1]+60  or coords[1]+60+30 >=coords_Mechant1[1]+120)  :
                canvas.delete(ImageMechant1_)
                MechantMort=1
    if sens_hero == 0:
        for o in range (coords[0]-60,coords[0]+20+1): ## On détecte si l'épée touche le méchant
            if (coords_Mechant1[0]+65>= o >=coords_Mechant1[0]) and (coords_Mechant1[1]<=  coords[1]+60  or coords[1]+60+30 >=coords_Mechant1[1]+120)  :
                canvas.delete(ImageMechant1_)
                MechantMort=1




def dégat_héro_subis ():
    global coords, coords_Mechant1, MéchantMort,HeroMort,frame_invincibilite,hp
    if frame_invincibilite==0:
        if MechantMort == 0:
            for o in range (coords[0], coords[0]+65): ## On détecte si le méchant touche le joueur
                if frame_invincibilite==0:
                    if (coords_Mechant1[0]<= o <= coords_Mechant1[0]+65) and (coords_Mechant1[1]<= coords[1]):
                        frame_invincibilite=1
                        hp=hp-1
                        if hp==0:
                            canvas.delete(Image_hero_)
                            canvas.create_image(-20,-100, anchor=NW,image=perdu)
                            HeroMort=1
                            frame_invincibilite=1
                        else:
                            fenetre.after(1000,dégat)
                break

    if hp == 2 : ## Décomte des points de vie
        canvas.delete(ImageCoeur3_)
    elif hp == 1 :
        canvas.delete(ImageCoeur2_)
    elif hp == 0 :
        canvas.delete(ImageCoeur1_)


def dégat():
    global frame_invincibilite
    frame_invincibilite=0


tableau=array([[300,500,630],[350,450,530],[600,700,600]])

## Innitialisation de toutes les variables
sens_hero = 1
sur_platform=1
en_saut=0
en_attaque=0
sens_mechant=0
MechantMort = 0
MechantMort = 0
hp=3
frame_invincibilite=0
HeroMort = 0


fenetre = Tk() ## Boucle de la fênetre graphique

coords = (700, 620)
photo = PhotoImage(file='1er fond.png') ## Création du fond

## Création de l'image du perso
Image_hero_gauche = PhotoImage(file='perso_0_gauche.png')
Image_hero_droite = PhotoImage(file='perso_sans_bords_5.png')
canvas = Canvas(fenetre,width=1500, height=800)
canvas.create_image(0, 0, anchor=NW, image=photo)
Image_hero_ = canvas.create_image(700,620, anchor=NW,image=Image_hero_droite)

## Création de l'image de l'épée
ImageEpee = PhotoImage(file='epee.png')
ImageEpee2 = PhotoImage(file='epee2.png')
perdu = PhotoImage(file="perdu.png")

## Création des plateformes
platform_=PhotoImage(file='plateforme.png')

platform_1_1=canvas.create_image(300,630,anchor=NW,image=platform_)
platform_1_2=canvas.create_image(400,630,anchor=NW,image=platform_)

platform_2=canvas.create_image(350,530,anchor=NW,image=platform_)

platform_3=canvas.create_image(600,600,anchor=NW,image=platform_)

## Création du Méchant
ImageMechant1 = PhotoImage(file='ennemi_1.png')
ImageMechant1_ = canvas.create_image(1200,620, anchor=NW,image=ImageMechant1)
ImageMechant1v2=PhotoImage(file='ennemi_2.png')
coords_Mechant1 = (1200, 620)

## Créaion de l'hitbox de la fênetre graphique
rectangle_fenetre=canvas.create_rectangle(0,0,1500,740,width=0)
coords_rectangle = (0,0,1500,740)

## Création des images des coeurs
ImageCoeur3 = PhotoImage(file='coeur_vie_3.png')
ImageCoeur3_ = canvas.create_image(50,50, anchor=NW,image=ImageCoeur3)
ImageCoeur2 = PhotoImage(file='coeur_vie_2.png')
ImageCoeur2_ = canvas.create_image(50,50, anchor=NW,image=ImageCoeur2)
ImageCoeur1 = PhotoImage(file='coeur_vie_1.png')
ImageCoeur1_ = canvas.create_image(50,50, anchor=NW,image=ImageCoeur1)





rectangle_hitbox_hero = canvas.create_rectangle(coords[0],coords[1],coords[0]+75,coords[1]+120,width=0)

deplacement_mechants()
canvas.focus_set()

## Détection des touches présser
canvas.bind("<Key>", fonction_déplacement)
canvas.bind("<KeyPress-f>",attaque)


canvas.pack()
fenetre.mainloop()


