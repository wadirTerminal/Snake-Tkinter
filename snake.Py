import tkinter as tk
import random
import sys


# Sans ça, Windows affiche la fenêtre floue sur les écrans HD (mise à l'échelle)
if sys.platform == "win32":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

TAILLE = 20  #taille d'une case en pixels
LARGEUR = 20 # nombre de case horizontale
HAUTEUR = 20  #nombre de case verticale

VERT = "#3ddc97"
FOND = "#0d1117"
TERRAIN = "#010409"
GRILLE = "#161b22"

fenetre = tk.Tk()
fenetre.title("Snake")
fenetre.resizable(False, False)
fenetre.configure(bg=FOND)


# pouvoir refaire des boutons du meme style sans re-coder
def creer_bouton(parent, texte, commande, largeur=12):
    bouton = tk.Label(parent, text=texte, width=largeur, font=("Arial", 13, "bold"),fg=VERT, bg=FOND, cursor="hand2", pady=6, highlightthickness=2, highlightbackground=VERT)
    bouton.bind("<Button-1>", lambda event: commande())
    bouton.bind("<Enter>", lambda event: bouton.config(bg=VERT, fg=FOND))
    bouton.bind("<Leave>", lambda event: bouton.config(bg=FOND, fg=VERT))
    return bouton



# ====  cadre du menu  =======
menu = tk.Frame(fenetre, bg=FOND, width=LARGEUR * TAILLE + 40, height=HAUTEUR * TAILLE + 80)
menu.pack_propagate(False)

tk.Label(menu, text="SNAKE", fg=VERT, bg=FOND, font=("Arial", 38, "bold")).pack(pady=(80, 30))
creer_bouton(menu, "Jouer", lambda: lancer_partie()).pack(pady=6)
creer_bouton(menu, "Quitter", fenetre.destroy).pack(pady=6)

# ==== cadre du jeu  =====
jeu = tk.Frame(fenetre, bg=FOND)

canvas = tk.Canvas(jeu, width=LARGEUR * TAILLE, height=HAUTEUR * TAILLE, bg=TERRAIN, highlightthickness=3, highlightbackground=VERT)
canvas.pack(padx=20, pady=(20, 10))

barre = tk.Frame(jeu, bg=FOND)
barre.pack(fill="x", padx=20, pady=(0, 15))
creer_bouton(barre, "Restart", lambda: lancer_partie(), largeur=9).pack(side="left")
creer_bouton(barre, "Menu", lambda: afficher_menu(), largeur=9).pack(side="right")

#  ===== fonction et methode du jeu ========
serpent = []
direction = (1, 0)
prochaine_direction = (1, 0)
pomme = (5, 5)
score = 0
boucle = None  # id du after() actuel


def nouvelle_pomme():
    libres = [(x, y) 
            for x in range(LARGEUR) 
            for y in range(HAUTEUR)
            if (x, y) not in serpent]
    return random.choice(libres)


def dessiner():
    canvas.delete("all")
    x, y = pomme
    canvas.create_rectangle(x * TAILLE, y * TAILLE, (x + 1) * TAILLE, (y + 1) * TAILLE, fill="red")
    for x, y in serpent:
        canvas.create_rectangle(x * TAILLE, y * TAILLE, (x + 1) * TAILLE, (y + 1) * TAILLE, fill="green")

def afficher_score():
    fenetre.title(f"Snake  score : {score}")

def avancer():
    global pomme, direction, boucle , score
    direction = prochaine_direction
    x, y = serpent[0]
    nouvelle_tete = (x + direction[0], y + direction[1])

    if not ((0 <= nouvelle_tete[0] < LARGEUR ) and ( 0 <= nouvelle_tete[1] < HAUTEUR) ) or nouvelle_tete in serpent:
        canvas.create_text(LARGEUR * TAILLE // 2, HAUTEUR * TAILLE // 2, text="PERDU", fill="white", font=("Arial", 30))
        return

    serpent.insert(0, nouvelle_tete)
    if nouvelle_tete == pomme:
        pomme = nouvelle_pomme()
        score += 1
        afficher_score()
    else:
        serpent.pop()

    dessiner()
    boucle = fenetre.after(120, avancer)


def tourner(dx, dy):
    global prochaine_direction
    if (dx, dy) != (-direction[0], -direction[1]):
        prochaine_direction = (dx, dy)


# =====control ========
def arreter_boucle():
    global boucle
    if boucle:
        fenetre.after_cancel(boucle)
        boucle = None


def lancer_partie():
    global serpent, direction, prochaine_direction, pomme , score
    arreter_boucle()
    score = 0
    fenetre.title("Snake")
    serpent = [(10, 10)]
    direction = (1, 0)
    prochaine_direction = (1, 0)
    pomme = nouvelle_pomme()
    menu.pack_forget()
    jeu.pack(padx=6, pady=6)
    avancer()


def afficher_menu():
    arreter_boucle()
    jeu.pack_forget()
    menu.pack(padx=6, pady=6)
    fenetre.title("Snake")


fenetre.bind("<Up>", lambda event: tourner(0, -1))
fenetre.bind("<Down>", lambda event: tourner(0, 1))
fenetre.bind("<Left>", lambda event: tourner(-1, 0))
fenetre.bind("<Right>", lambda event: tourner(1, 0))

afficher_menu()
fenetre.mainloop()