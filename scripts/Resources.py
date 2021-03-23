# ======================================================================================================================
# TITLE: 		Executor.py
# AUTHOR: 		Anika Seidel
# 				Cedric Rönnfeld
# 				Till Mack
# 				Florian Lehmann
# LAST EDIT: 	21.03.2021
# ======================================================================================================================


# ======================================================================================================================
# IMPORTING
# ======================================================================================================================

from godot import ResourceLoader, Sprite
from .RiddleCollection import RiddleCollection
import os
import json

# ======================================================================================================================
# LOADING ALL RESOURCES
# ======================================================================================================================

def load():
    # ==================================================================================================================
    # CREATING BACKGROUND SPRITES
    # ==================================================================================================================

    # BACKGROUNDS #
    # extracting Images as Sprite-Objects
    bg = Sprite.new()
    # bg.position = DEFAULT_RESOLUTION / 2

    Title = Sprite.new()

    MainMenuBG = bg.duplicate()
    CanteensBG = bg.duplicate()
    CellsBG = bg.duplicate()
    HallsBG = bg.duplicate()
    CornersBG = bg.duplicate()
    DialogBG = bg.duplicate()
    Graffity = bg.duplicate()
    Ecken = bg.duplicate()
    Sudoku = bg.duplicate()
    Striche = bg.duplicate()
    Umschlaga = bg.duplicate()
    Umschlagb = bg.duplicate()
    Umschlagc = bg.duplicate()
    Umschlagd = bg.duplicate()
    Umschlage = bg.duplicate()
    Uhr = bg.duplicate()
    Rahmena = bg.duplicate()
    Rahmenb = bg.duplicate()
    Rahmenc = bg.duplicate()
    Rahmend = bg.duplicate()
    Vigenere = bg.duplicate()
    Bett = bg.duplicate()
    Sudokub = bg.duplicate()
    Musik = bg.duplicate()
    Mathe = bg.duplicate()
    Buch = bg.duplicate()
    Zahlen = bg.duplicate()
    Licht = bg.duplicate()
    Leuchten = bg.duplicate()
    Chemie = bg.duplicate()
    Karton1 = bg.duplicate()
    Karton2 = bg.duplicate()
    Karton3 = bg.duplicate()
    TowersBG = bg.duplicate()
    Waerter = bg.duplicate()

    # ==================================================================================================================
    # CREATING OBJECT SPRITES
    # ==================================================================================================================

    # Images
    Briefa = Sprite.new()
    Briefb = Sprite.new()
    Briefc = Sprite.new()
    Briefd = Sprite.new()
    Briefe = Sprite.new()
    Uhrwand = Sprite.new()
    Bilderrahmena = Sprite.new()
    Bilderrahmenb = Sprite.new()
    Bilderrahmenc = Sprite.new()
    Bilderrahmend = Sprite.new()
    Mensch = Sprite.new()
    Schalter = Sprite.new()
    Erlenmeyerkolben = Sprite.new()
    Buch1 = Sprite.new()
    xy = Sprite.new()
    zigarette = Sprite.new()
    Box1 = Sprite.new()
    Box2 = Sprite.new()
    Box3 = Sprite.new()
    Mensch2 = Sprite.new()

    TP = Sprite.new()
    Help = Sprite.new()
    Heart = Sprite.new()
    Cig_Box = Sprite.new()
    SoundIcon = Sprite.new()
    MapBG = bg.duplicate()
    MapCell = Sprite.new()
    MapCellClosed = Sprite.new()
    MapCorner = Sprite.new()
    MapCornerClosed = Sprite.new()
    RedDot = Sprite.new()
    Compass = Sprite.new()

    # Arrows

    DownArrow = Sprite.new()
    LeftArrow = Sprite.new()
    LeftCornerArrow = Sprite.new()
    RightArrow = Sprite.new()
    CellArrow = Sprite.new()
    CanteenArrow = Sprite.new()

    # Doors

    CornerDoor = Sprite.new()
    HallDoor = Sprite.new()
    TowerDoor = bg.duplicate()

    # Numbers

    Hall0 = Sprite.new()
    Hall1 = Sprite.new()
    Hall2 = Sprite.new()
    Hall3 = Sprite.new()
    Hall4 = Sprite.new()
    Hall5 = Sprite.new()
    Hall6 = Sprite.new()
    Hall7 = Sprite.new()
    Hall8 = Sprite.new()
    Hall9 = Sprite.new()
    Corner0 = Sprite.new()
    Corner1 = Sprite.new()
    Corner2 = Sprite.new()
    Corner3 = Sprite.new()
    Corner4 = Sprite.new()
    Corner5 = Sprite.new()
    Corner6 = Sprite.new()
    Corner7 = Sprite.new()
    Corner8 = Sprite.new()
    Corner9 = Sprite.new()

    # Number Cig
    NumRahmen0 = Sprite.new()
    NumRahmen1 = Sprite.new()
    NumRahmen2 = Sprite.new()
    NumRahmen3 = Sprite.new()
    NumRahmen4 = Sprite.new()

    # Backgrounds
    # ==================================================================================================================
    # LOAD SPRITES
    # ==================================================================================================================

    Title.texture = ResourceLoader.load("res://resources/Images/Title.png")

    MainMenuBG.texture = ResourceLoader.load("res://resources/Images/MainMenu.png")
    CanteensBG.texture = ResourceLoader.load("res://resources/Images/Canteen.png")
    CellsBG.texture = ResourceLoader.load("res://resources/Images/Zelle.png")
    HallsBG.texture = ResourceLoader.load("res://resources/Images/Hall.png")
    CornersBG.texture = ResourceLoader.load("res://resources/Images/Corner.png")
    DialogBG.texture = ResourceLoader.load("res://resources/Images/Dialog_bg.png")

    # Riddle images
    Uhr.texture = ResourceLoader.load("res://resources/Images/Uhr.png")
    Uhrwand.texture = ResourceLoader.load("res://resources/Images/Uhrwand.png")
    Graffity.texture = ResourceLoader.load("res://resources/Images/Graffity.png")
    Vigenere.texture = ResourceLoader.load("res://resources/Images/Vigenere.jpg")
    Ecken.texture = ResourceLoader.load("res://resources/Images/Eckenrätsel.png")
    Sudoku.texture = ResourceLoader.load("res://resources/Images/Sudoku.jpg")
    Striche.texture = ResourceLoader.load("res://resources/Images/Striche.png")
    Umschlaga.texture = ResourceLoader.load("res://resources/Images/Umschlag1.jpg")
    Umschlagb.texture = ResourceLoader.load("res://resources/Images/Umschlag2.jpg")
    Umschlagc.texture = ResourceLoader.load("res://resources/Images/Umschlag3.jpg")
    Umschlagd.texture = ResourceLoader.load("res://resources/Images/Umschlag4.jpg")
    Umschlage.texture = ResourceLoader.load("res://resources/Images/Umschlag5.jpg")
    Rahmena.texture = ResourceLoader.load("res://resources/Images/Rahmen1.png")
    Rahmenb.texture = ResourceLoader.load("res://resources/Images/Rahmen2.png")
    Rahmenc.texture = ResourceLoader.load("res://resources/Images/Rahmen3.png")
    Rahmend.texture = ResourceLoader.load("res://resources/Images/Rahmen4.png")
    Bilderrahmena.texture = ResourceLoader.load("res://resources/Images/Bilderrahmen1.png")
    Bilderrahmenb.texture = ResourceLoader.load("res://resources/Images/Bilderrahmen2.png")
    Bilderrahmenc.texture = ResourceLoader.load("res://resources/Images/Bilderrahmen3.png")
    Bilderrahmend.texture = ResourceLoader.load("res://resources/Images/Bilderrahmen4.png")
    Briefa.texture = ResourceLoader.load("res://resources/Images/Brief1.png")
    Briefb.texture = ResourceLoader.load("res://resources/Images/Brief2.png")
    Briefc.texture = ResourceLoader.load("res://resources/Images/Brief3.png")
    Briefd.texture = ResourceLoader.load("res://resources/Images/Brief4.png")
    Briefe.texture = ResourceLoader.load("res://resources/Images/Brief5.png")
    Bett.texture = ResourceLoader.load("res://resources/Images/Bett.png")
    Mensch.texture = ResourceLoader.load("res://resources/Images/Mensch.png")
    Sudokub.texture = ResourceLoader.load("res://resources/Images/Sudoku2.png")
    Musik.texture = ResourceLoader.load("res://resources/Images/Musik.png")
    Mathe.texture = ResourceLoader.load("res://resources/Images/Mathe.png")
    Buch.texture = ResourceLoader.load("res://resources/Images/Buch.png")
    Zahlen.texture = ResourceLoader.load("res://resources/Images/Zahlen.png")
    Licht.texture = ResourceLoader.load("res://resources/Images/Licht.png")
    Leuchten.texture = ResourceLoader.load("res://resources/Images/Leuchten.png")
    Schalter.texture = ResourceLoader.load("res://resources/Images/Schalter.png")
    Chemie.texture = ResourceLoader.load("res://resources/Images/Chemie.png")
    Erlenmeyerkolben.texture = ResourceLoader.load("res://resources/Images/Erlenmeyerkolben.png")
    Buch1.texture = ResourceLoader.load("res://resources/Images/Buch1.png")
    xy.texture = ResourceLoader.load("res://resources/Images/xy.png")
    zigarette.texture = ResourceLoader.load("res://resources/Images/zigarette.png")
    Box1.texture = ResourceLoader.load("res://resources/Images/Box1.png")
    Box2.texture = ResourceLoader.load("res://resources/Images/Box2.png")
    Box3.texture = ResourceLoader.load("res://resources/Images/Box3.png")
    Karton1.texture = ResourceLoader.load("res://resources/Images/Karton1.png")
    Karton2.texture = ResourceLoader.load("res://resources/Images/Karton2.png")
    Karton3.texture = ResourceLoader.load("res://resources/Images/Karton3.png")
    Mensch2.texture = ResourceLoader.load("res://resources/Images/Mensch2.png")
    Waerter.texture = ResourceLoader.load("res://resources/Images/Wärter.png")

    # Icons
    Help.texture = ResourceLoader.load("res://resources/Images/Help.png")
    Heart.texture = ResourceLoader.load("res://resources/Images/Heart.png")
    Cig_Box.texture = ResourceLoader.load("res://resources/Images/Cigarette_Box.png")
    SoundIcon.texture = ResourceLoader.load("res://resources/Images/sound.png")
    MapBG.texture = ResourceLoader.load("res://resources/Images/MapBG.png")
    MapCell.texture = ResourceLoader.load("res://resources/Images/MapCell.png")
    MapCellClosed.texture = ResourceLoader.load("res://resources/Images/MapCellClosed.png")
    MapCorner.texture = ResourceLoader.load("res://resources/Images/MapCorner.png")
    MapCornerClosed.texture = ResourceLoader.load("res://resources/Images/MapCornerClosed.png")
    RedDot.texture = ResourceLoader.load("res://resources/Images/RedDot.png")
    Compass.texture = ResourceLoader.load("res://resources/Images/Compass.png")

    # Tower backgrounds
    TP.texture = ResourceLoader.load("res://resources/Images/TP.png")
    TowersBG.texture = ResourceLoader.load("res://resources/Images/Turm.png")

    # Arrows
    DownArrow.texture = ResourceLoader.load("res://resources/Images/Down.png")
    LeftCornerArrow.texture = ResourceLoader.load("res://resources/Images/Left_Corner.png")
    LeftArrow.texture = ResourceLoader.load("res://resources/Images/Left.png")
    RightArrow.texture = ResourceLoader.load("res://resources/Images/Right.png")
    CellArrow.texture = ResourceLoader.load("res://resources/Images/Pfeil_Zelle.png")
    CanteenArrow.texture = ResourceLoader.load("res://resources/Images/Pfeil_Canteen.png")

    # Doors
    HallDoor.texture = ResourceLoader.load("res://resources/Images/HallDoor.png")
    CornerDoor.texture = ResourceLoader.load("res://resources/Images/EckeDoor.png")
    TowerDoor.texture = ResourceLoader.load("res://resources/Images/TurmDoor.png")

    # Hall numbers
    Hall0.texture = ResourceLoader.load("res://resources/Images/Hall0.png")
    Hall1.texture = ResourceLoader.load("res://resources/Images/Hall1.png")
    Hall2.texture = ResourceLoader.load("res://resources/Images/Hall2.png")
    Hall3.texture = ResourceLoader.load("res://resources/Images/Hall3.png")
    Hall4.texture = ResourceLoader.load("res://resources/Images/Hall4.png")
    Hall5.texture = ResourceLoader.load("res://resources/Images/Hall5.png")
    Hall6.texture = ResourceLoader.load("res://resources/Images/Hall6.png")
    Hall7.texture = ResourceLoader.load("res://resources/Images/Hall7.png")
    Hall8.texture = ResourceLoader.load("res://resources/Images/Hall8.png")
    Hall9.texture = ResourceLoader.load("res://resources/Images/Hall9.png")

    # Corner numbers
    Corner0.texture = ResourceLoader.load("res://resources/Images/Corner0.png")
    Corner1.texture = ResourceLoader.load("res://resources/Images/Corner1.png")
    Corner2.texture = ResourceLoader.load("res://resources/Images/Corner2.png")
    Corner3.texture = ResourceLoader.load("res://resources/Images/Corner3.png")
    Corner4.texture = ResourceLoader.load("res://resources/Images/Corner4.png")
    Corner5.texture = ResourceLoader.load("res://resources/Images/Corner5.png")
    Corner6.texture = ResourceLoader.load("res://resources/Images/Corner6.png")
    Corner7.texture = ResourceLoader.load("res://resources/Images/Corner7.png")
    Corner8.texture = ResourceLoader.load("res://resources/Images/Corner8.png")
    Corner9.texture = ResourceLoader.load("res://resources/Images/Corner9.png")

    # AUDIO #

    MainAudio = ResourceLoader.load("res://resources/Sounds/Main.wav")
    StartAudio = ResourceLoader.load("res://resources/Sounds/Start.wav")
    StopAudio = ResourceLoader.load("res://resources/Sounds/Ende.wav")

    # SCENES #
    # extracting predefined Scene-Data
    Player = ResourceLoader.load("res://scenes/Player.tscn")

    NumRahmen0.texture = ResourceLoader.load("res://resources/Images/NumRahmen0.png")
    NumRahmen1.texture = ResourceLoader.load("res://resources/Images/NumRahmen1.png")
    NumRahmen2.texture = ResourceLoader.load("res://resources/Images/NumRahmen2.png")
    NumRahmen3.texture = ResourceLoader.load("res://resources/Images/NumRahmen3.png")
    NumRahmen4.texture = ResourceLoader.load("res://resources/Images/NumRahmen4.png")

    # DIALOGS #
    # extracting dialog data from json files
    Dialogs = dict()
    DIA_rest_list = ["intro", "riddle_solved", "riddle_failed", "help","guard","end_win","door", "birthday","me"]
    DIA_riddle_list = [
        "uhr",
        "sudoku",
        "ecken",
        "vigenere",
        "striche",
        "umschlag",
        "rahmen",
        "player",
        "sudokub",
        "musik",
        "geburtstag",
        "mathe",
        "gruenBett",
        "schalter",
        "gruenZahlen",
        "chemie",
        "objekte"
    ]
    pathes = [{"category": "rest", "name": i} for i in DIA_rest_list]
    pathes += [{"category": "riddle", "name": i} for i in DIA_riddle_list]
    for i in pathes:
        with open(
                os.path.join(os.path.dirname(__file__),
                             "../resources/Dialogs/" + i["category"] + "/DIA_" + i["name"] + ".json"),
                encoding="utf-8"
        ) as jfile:
            Dialogs[i["name"]] = json.load(jfile)

    # THEME #
    # extracting predefined Theme
    theme = ResourceLoader.load("res://resources/theme.tres")

    # RIDDLES #
    Riddles = RiddleCollection()

    # ==================================================================================================================
    # RETURN DICT
    # ==================================================================================================================

    return {
        "Title": Title,
        "MainMenuBG": MainMenuBG,
        "Player": Player,
        "Dialogs": Dialogs,
        "RiddleCollection": Riddles,
        "Theme": theme,

        # Audio
        "MainAudio": MainAudio,
        "StartAudio": StartAudio,
        "StopAudio": StopAudio,
        "SoundIcon": SoundIcon,

        # Map
        "MapBG": MapBG,
        "MapCell": MapCell,
        "MapCellClosed": MapCellClosed,
        "MapCorner": MapCorner,
        "MapCornerClosed": MapCornerClosed,
        "RedDot": RedDot,
        "Compass": Compass,

        # Backgrounds
        "CanteensBG": CanteensBG,
        "CellsBG": CellsBG,
        "HallsBG": HallsBG,
        "CornersBG": CornersBG,
        "DialogBG": DialogBG,
        "DownArrow": DownArrow,
        "LeftArrow": LeftArrow,
        "LeftCornerArrow": LeftCornerArrow,
        "RightArrow": RightArrow,
        "CellArrow": CellArrow,
        "CanteenArrow": CanteenArrow,
        "HallDoor": HallDoor,
        "CornerDoor": CornerDoor,
        "TowerDoor": TowerDoor,
        "TowersBG": TowersBG,
        "TP": TP,

        # Numbers
        "Hall0": Hall0,
        "Hall1": Hall1,
        "Hall2": Hall2,
        "Hall3": Hall3,
        "Hall4": Hall4,
        "Hall5": Hall5,
        "Hall6": Hall6,
        "Hall7": Hall7,
        "Hall8": Hall8,
        "Hall9": Hall9,
        "Corner0": Corner0,
        "Corner1": Corner1,
        "Corner2": Corner2,
        "Corner3": Corner3,
        "Corner4": Corner4,
        "Corner5": Corner5,
        "Corner6": Corner6,
        "Corner7": Corner7,
        "Corner8": Corner8,
        "Corner9": Corner9,

        # Riddle images
        "Graffity": Graffity,
        "Ecken": Ecken,
        "Sudoku": Sudoku,
        "Sudokub": Sudokub,
        "Striche": Striche,
        "Umschlaga": Umschlaga,
        "Umschlagb": Umschlagb,
        "Umschlagc": Umschlagc,
        "Umschlagd": Umschlagd,
        "Umschlage": Umschlage,
        "Uhr": Uhr,
        "Uhrwand": Uhrwand,
        "Rahmena": Rahmena,
        "Rahmenb": Rahmenb,
        "Rahmenc": Rahmenc,
        "Rahmend": Rahmend,
        "Bilderrahmena": Bilderrahmena,
        "Bilderrahmenb": Bilderrahmenb,
        "Bilderrahmenc": Bilderrahmenc,
        "Bilderrahmend": Bilderrahmend,
        "Briefa": Briefa,
        "Briefb": Briefb,
        "Briefc": Briefc,
        "Briefd": Briefd,
        "Briefe": Briefe,
        "Vigenere": Vigenere,
        "Bett": Bett,
        "Mensch": Mensch,
        "Musik": Musik,
        "Mathe": Mathe,
        "Buch": Buch,
        "Zahlen": Zahlen,
        "Licht": Licht,
        "Leuchten": Leuchten,
        "Schalter": Schalter,
        "Erlenmeyerkolben": Erlenmeyerkolben,
        "Chemie": Chemie,
        "Buch1": Buch1,
        "xy": xy,
        "zigarette": zigarette,
        "Box1": Box1,
        "Box2": Box2,
        "Box3": Box3,
        "Karton1": Karton1,
        "Karton2": Karton2,
        "Karton3": Karton3,
        "Mensch2": Mensch2,
        "Help": Help,
        "Cig_Box": Cig_Box,
        "Heart": Heart,
        "Wärter": Waerter,

        "NumRahmen0": NumRahmen0,
        "NumRahmen1": NumRahmen1,
        "NumRahmen2": NumRahmen2,
        "NumRahmen3": NumRahmen3,
        "NumRahmen4": NumRahmen4,
    }