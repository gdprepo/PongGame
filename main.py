# Importation des librairies
from tkinter import *
import math

# Déclaration des variables globales
menuview = None
settingview = None
playview = None
sz_arena = 0
winpoints = 0
# # Définition des variables pour déplacer la balle et des raquettes
h_speed_ball = 1
v_speed_ball = 1
speed_racket = 30


def open_setting():
    global menuview, playview, settingview, sz_arena
    # Fermeture du Menu principal
    menuview.destroy()

    # Définition des dimensions de la fenêtre "settingview"
    setting_width = 350
    half_setting_width = setting_width / 2
    setting_height = 100
    half_setting_height = setting_height / 2

    # Construction de la fenêtre principale "settingview"
    settingview = Tk()
    settingview.title("Configuration")
    settingicon = PhotoImage(file=".icones/settingicon.png")
    settingview.call("wm", "iconphoto", settingview._w, settingicon)
    # Empêchement de la redimensionner
    settingview.resizable(width=False, height=False)
    # Création du canvas "fen_menu"
    fen_setting = Canvas(settingview, width=setting_width, height=setting_height, bd=-1)

    # Création de la rubrique "Arène"
    # Création du label "Arène"
    lbl_arena = Label(settingview, text="Arène", font=("Roboto", "11"))
    # Création du bonton de menu "Taille de l'Arène"
    mnb_sz_arena = Menubutton(
        settingview,
        activebackground="#464856",
        activeforeground="white",
        text="Taille de l'Arène",
        font=("Roboto", "10"),
        relief="raised",
    )
    # Création de la liste déroulante avec les trois configurations possibles
    mnb_sz_arena.mnu_arena = Menu(
        mnb_sz_arena,
        activebackground="#464856",
        activeforeground="white",
        font=("Roboto", "9"),
        tearoff=0,
    )
    mnb_sz_arena["menu"] = mnb_sz_arena.mnu_arena
    sz_arena = IntVar()
    mnb_sz_arena.mnu_arena.add_radiobutton(
        label="Entraînement", variable=sz_arena, value=1
    )
    mnb_sz_arena.mnu_arena.add_radiobutton(label="Basique", variable=sz_arena, value=0)
    mnb_sz_arena.mnu_arena.add_radiobutton(label="Tournoi", variable=sz_arena, value=2)

    # Création du label "Nombre de points gagnants"
    lbl_winpoints = Label(
        settingview, text="Nombre de points gagnants", font=("Roboto", "10")
    )
    # Création du champ de texte pour le Nombre de points gagnants
    winpoints = StringVar()
    cds_winpoints = Entry(
        settingview,
        textvariable=winpoints,
        font=("Staatliches", "12"),
        justify="center",
        selectborderwidth="3",
    ).grid(row=5, column=2)

    # Création du bouton "Valider"
    Button(
        settingview,
        text="Valider",
        foreground="#464856",
        activebackground="#CCFFCC",
        activeforeground="#11692A",
        font=("Roboto", "11"),
        borderwidth=2,
        command=open_play,
    ).grid(row=6, column=4)

    # Placement des widgets
    fen_setting.grid(row=16, column=5)
    lbl_arena.grid(row=1, column=2)
    mnb_sz_arena.grid(row=3, column=0)
    lbl_winpoints.grid(row=5, column=0)


def open_play():
    """
    Fonction gérant l'écran de jeu
    """
    global settingview, sz_arena
    # Fermeture de l'écran de configuration
    settingview.destroy()

    # Définition des dimensions de la fenêtre "playview"
    if sz_arena.get() == 0:
        play_width = 654
        play_height = 400
    elif sz_arena.get() == 1:
        play_width = 458
        play_height = 280
    elif sz_arena.get() == 2:
        play_width = 851
        play_height = 520
    half_play_width = play_width / 2
    half_play_height = play_height / 2
    # Définition des dimensions des Buts
    left_width_goal = play_width * 25 / 327
    right_width_goal = play_width - left_width_goal
    middle_play_width = (half_play_width - left_width_goal) / 2
    # Définition des variables de positionnement
    x0_ball = half_play_width - 6
    y0_ball = half_play_height - 6
    x1_ball = half_play_width + 6
    y1_ball = half_play_height + 6
    # Définition des variables des raquettes
    min_racket_height = half_play_height - 40
    max_racket_height = half_play_height + 40

    # Mise en mouvement de la balle

    def move_ball():
        """
        Fonction permettant à la balle de se déplacer
        """
        global h_speed_ball, v_speed_ball

        # Si la valeur en y0 est < à 0
        # OU la valeur en y1 est > à la play_height
        if fen_play.coords(ball)[1] < 6 or fen_play.coords(ball)[3] > play_height - 6:
            v_speed_ball *= -1

        # Collision de la balle avec les raquettes
        if (
            fen_play.coords(ball)[0] < fen_play.coords(left_racket)[2]
            and fen_play.coords(ball)[3] > fen_play.coords(left_racket)[1]
            and fen_play.coords(ball)[1] < fen_play.coords(left_racket)[3]
        ) or (
            fen_play.coords(ball)[2] > fen_play.coords(right_racket)[0]
            and fen_play.coords(ball)[3] > fen_play.coords(right_racket)[1]
            and fen_play.coords(ball)[1] < fen_play.coords(right_racket)[3]
        ):
            h_speed_ball *= -1

        fen_play.move(ball, h_speed_ball, v_speed_ball)

        # Traitement des victoires
        if fen_play.coords(ball)[0] < left_width_goal - 1:
            # Retour au Menu principal
            playview.destroy()
            open_menu()
        elif fen_play.coords(ball)[2] > right_width_goal + 1:
            # Retour au Menu principal
            playview.destroy()
            open_menu()
        fen_play.after(10, move_ball)

    def move_racket(event):
        """
        Fonction permettant de faire bouger les raquettes
        """
        global speed_racket
        # Déclaration de la variable "key"
        key = event.keysym

        # Déplacement de la raquette de gauche
        if fen_play.coords(left_racket)[1] <= 30:
            if key == "f":
                fen_play.move(left_racket, 0, speed_racket)
        elif fen_play.coords(left_racket)[3] >= play_height - 30:
            if key == "r":
                fen_play.move(left_racket, 0, -speed_racket)
        else:
            if key == "r":
                fen_play.move(left_racket, 0, -speed_racket)
            if key == "f":
                fen_play.move(left_racket, 0, speed_racket)

        # Déplacement de la raquette de droite
        if fen_play.coords(right_racket)[1] <= 30:
            if key == "Down":
                fen_play.move(right_racket, 0, speed_racket)
        elif fen_play.coords(right_racket)[3] >= play_height - 30:
            if key == "Up":
                fen_play.move(right_racket, 0, -speed_racket)
        else:
            if key == "Up":
                fen_play.move(right_racket, 0, -speed_racket)
            if key == "Down":
                fen_play.move(right_racket, 0, speed_racket)

    # Construction de la fenêtre principale "playview"
    playview = Tk()
    playview.title("Partie de jeu")
    playicon = PhotoImage(file=".icones/playicon.png")
    playview.call("wm", "iconphoto", playview._w, playicon)
    # Empêchement de la redimensionner
    playview.resizable(width=False, height=False)

    # Création du Canvas "fen_play"
    fen_play = Canvas(playview, width=play_width, height=play_height, bd=0, bg="black")
    fen_play.pack()

    # Création de la ligne du haut
    fen_play.create_line(0, 0, play_width + 1, 0, fill="white", width=10)
    # Création de la ligne du bas
    fen_play.create_line(
        0, play_height, play_width + 1, play_height, fill="white", width=10
    )

    # Séparation de la fenêtre en deux
    fen_play.create_line(
        half_play_width,
        10,
        half_play_width,
        play_height - 10,
        fill="white",
        dash=(20, 10),
        width=4,
    )
    # Démarcation des Zones de Buts
    left_goal = fen_play.create_line(
        left_width_goal,
        10,
        left_width_goal,
        play_height - 10,
        fill="white",
        dash=(6, 6),
        width=2,
    )
    right_goal = fen_play.create_line(
        right_width_goal,
        10,
        right_width_goal,
        play_height - 10,
        fill="white",
        dash=(6, 6),
        width=2,
    )
    # Création des raquettes
    left_racket = fen_play.create_line(
        left_width_goal,
        min_racket_height,
        left_width_goal,
        max_racket_height,
        fill="white",
        width=6,
    )
    right_racket = fen_play.create_line(
        right_width_goal,
        min_racket_height,
        right_width_goal,
        max_racket_height,
        fill="white",
        width=6,
    )
    # Création de la balle
    ball = fen_play.create_oval(x0_ball, y0_ball, x1_ball, y1_ball, fill="white")

    # Affichage des Scores
    # Définition des variables de score
    left_score = 0
    right_score = 0
    difference_score = math.fabs(left_score - right_score)

    fen_play.create_text(
        half_play_width - middle_play_width,
        half_play_height,
        text=left_score,
        font=("Staatliches", "46"),
        fill="white",
    )
    fen_play.create_text(
        half_play_width + middle_play_width,
        half_play_height,
        text=right_score,
        font=("Staatliches", "46"),
        fill="white",
    )

    playview.bind("<Key>", move_racket)

    move_ball()

    # Lancement de la "boucle principale"
    playview.mainloop()


def open_menu():
    global menuview

    # Définition des dimensions de la fenêtre "menuview"
    menu_width = 250
    half_menu_width = menu_width / 2
    menu_height = 100

    # Construction de la fenêtre principale "menuview"
    menuview = Tk()
    menuview.title("Menu principal")
    menuicon = PhotoImage(file=".icones/menuicon.png")
    menuview.call("wm", "iconphoto", menuview._w, menuicon)
    # Empêchement de la redimensionner
    menuview.resizable(width=False, height=False)
    # Création du canvas "fen_menu"
    fen_menu = Canvas(menuview, width=menu_width, height=menu_height, bd=-1)

    # Création du bouton "Faire une partie"
    btn_play = Button(
        menuview,
        text="Faire une partie",
        foreground="#464856",
        activebackground="#99CCFF",
        activeforeground="#22427C",
        font=("Roboto", "11"),
        borderwidth=2,
        command=open_setting,
    )
    # Création du bouton "Quitter"
    btn_exit = Button(
        menuview,
        text="Quitter",
        foreground="#464856",
        activebackground="#FFCCCC",
        activeforeground="#800000",
        font=("Roboto", "11"),
        borderwidth=2,
        command=menuview.destroy,
    )
    # Création du label "Y. LE COZ  2018 - 2019"
    fen_menu.create_text(
        half_menu_width,
        menu_height - 5,
        text="Y. LE COZ  2018 - 2019",
        font=("DINOT", "9"),
        fill="#464856",
    )

    # Placement des widgets
    fen_menu.grid(row=0, column=2, columnspan=2, padx=10, pady=5)
    btn_play.grid(row=0, column=2)
    btn_exit.grid(row=0, column=3)

    # Lancement de la "boucle principale"
    menuview.mainloop()


open_menu()
