# ======================================================================================================================
# TITLE: 		RiddleCollection.py
# AUTHOR: 		Anika Seidel
# 				Cedric Rönnfeld
# 				Till Mack
# 				Florian Lehmann
# LAST EDIT: 	21.03.2021
# ======================================================================================================================


# ======================================================================================================================
# IMPORTING
# ======================================================================================================================

# using to get a random number in an interval
from random import randrange

# ======================================================================================================================
# CONSTANTS
# ======================================================================================================================

# number of all possible riddles
RIDDLE_COUNT = 17

# generating a list for checking the used riddles
riddlelist = list()

# ======================================================================================================================
# RIDDLE COLLECTION CLASS
# ======================================================================================================================

# defining the RiddleCollection Class, the main Object to load riddles
class RiddleCollection:

    # ==================================================================================================================
    # GETTING A RIDDLE
    # ==================================================================================================================

    def get_riddle(self, main, scene):
        # global the riddlelist to make it more accessible
        global riddlelist
        # choosing a random riddle

        # if the riddlelist reaches the maximum amount of riddles, the riddles start duplicating
        # and the riddlelist gets resettet
        if len(riddlelist) == RIDDLE_COUNT:
            riddlelist =[]

        riddle = "riddle" + str(randrange(0, RIDDLE_COUNT))

        # checking if random riddle is used already, if yes, generate a new one
        while riddle in riddlelist:
            riddle = "riddle" + str(randrange(0, RIDDLE_COUNT))

        # add riddle number to list for checking
        riddlelist.append(riddle)

        return getattr(self, riddle)

    # ==================================================================================================================
    # RIDDLE 0
    # ==================================================================================================================

    # Riddle number 0, (clock riddle)
    def riddle0(self, scene, main):
        # zooming the riddle image
        feid = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Uhr"].duplicate()
        )
        # zoom button with clock on it
        main.add_texture_button(
            texture_from_res=main.res["Uhrwand"].duplicate(),
            function_execution_id=feid,
            scene=scene,
            x=800,
            y=120
        )

    # ==================================================================================================================
    # RIDDLE 1
    # ==================================================================================================================

    # Riddle number 1, (sudoku riddle)
    def riddle1(self, scene, main):
        # zooming the riddle image
        feid = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Sudoku"].duplicate()
        )
        # zoom button with frame on it
        main.add_texture_button(
            texture_from_res=main.res["Bilderrahmena"].duplicate(),
            scene=scene,
            function_execution_id=feid,
            x=50,
            y=500
        )

    # ==================================================================================================================
    # RIDDLE 2
    # ==================================================================================================================

    # Riddle number 2, (edges riddle)
    def riddle2(self, scene, main):
        # image with the neon shapes on ground
        main.add_image(
            texture_from_res=main.res["Ecken"].duplicate(),
            scene=scene,
            x=960,
            y=545
        )

    # ==================================================================================================================
    # RIDDLE 3
    # ==================================================================================================================

    # Riddle number 3, (letter riddle)
    def riddle3(self, scene, main):
        # zooming the riddle image
        feid = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Vigenere"].duplicate()
        )

        # zoom button with letter on it
        main.add_texture_button(
            texture_from_res=main.res["Briefb"].duplicate(),
            scene=scene,
            function_execution_id=feid,
            x=265,
            y=560
        )
        # image with the graffiti spray
        main.add_image(
            texture_from_res=main.res["Graffity"].duplicate(),
            scene=scene,
            x=960,
            y=600
        )

    # ==================================================================================================================
    # RIDDLE 4
    # ==================================================================================================================

    # Riddle number 4, (lines riddle)
    def riddle4(self, scene, main):
        # image with the bed
        main.add_image(texture_from_res=main.res["Bett"].duplicate(), scene=scene)
        # image with the lines
        main.add_image(texture_from_res=main.res["Striche"].duplicate(), scene=scene)

    # ==================================================================================================================
    # RIDDLE 5
    # ==================================================================================================================

    # Riddle number 5, (envelop riddle)
    def riddle5(self, scene, main):
        # zooming the riddle images
        feida = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Umschlaga"].duplicate()
        )
        feidb = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Umschlagb"].duplicate()
        )
        feidc = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Umschlagc"].duplicate()
        )
        feidd = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Umschlagd"].duplicate()
        )
        feide = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Umschlage"].duplicate()
        )

        # image with the bed
        main.add_image(
            texture_from_res=main.res["Bett"].duplicate(),
            scene=scene
        )

        # zoom buttons with a letter on it
        main.add_texture_button(
            texture_from_res=main.res["Briefa"].duplicate(),
            scene=scene,
            function_execution_id=feida,
            x=0,
            y=900
        )
        main.add_texture_button(
            texture_from_res=main.res["Briefb"].duplicate(),
            scene=scene,
            function_execution_id=feidb,
            x=290,
            y=700
        )
        main.add_texture_button(
            texture_from_res=main.res["Briefc"].duplicate(),
            scene=scene,
            function_execution_id=feidc,
            x=1000,
            y=400
        )
        main.add_texture_button(
            texture_from_res=main.res["Briefd"].duplicate(),
            scene=scene,
            function_execution_id=feidd,
            x=1800,
            y=800
        )
        main.add_texture_button(
            texture_from_res=main.res["Briefe"].duplicate(),
            scene=scene,
            function_execution_id=feide,
            x=900,
            y=700
        )



    # ==================================================================================================================
    # RIDDLE 6
    # ==================================================================================================================

    # Riddle number 6, (frame riddle)
    def riddle6(self, scene, main):
        # zooming the riddle images
        feida = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Rahmena"].duplicate()
        )
        feidb = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Rahmenb"].duplicate()
        )
        feidc = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Rahmenc"].duplicate()
        )
        feidd = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Rahmend"].duplicate()
        )

        # zoom buttons with a frame on it
        main.add_texture_button(
            texture_from_res=main.res["Bilderrahmena"].duplicate(),
            scene=scene,
            function_execution_id=feida,
            x=50,
            y=500
        )
        main.add_texture_button(
            texture_from_res=main.res["Bilderrahmenb"].duplicate(),
            scene=scene,
            function_execution_id=feidb,
            x=600,
            y=300
        )
        main.add_texture_button(
            texture_from_res=main.res["Bilderrahmenc"].duplicate(),
            scene=scene,
            function_execution_id=feidc,
            x=1800,
            y=150
        )
        main.add_texture_button(
            texture_from_res=main.res["Bilderrahmend"].duplicate(),
            scene=scene,
            function_execution_id=feidd,
            x=1500,
            y=0
        )

    # ==================================================================================================================
    # RIDDLE 7
    # ==================================================================================================================

    # Riddle number 7, (me riddle)
    def riddle7(self, scene, main):
        # zooming the riddle image
        feid =main.Executor.add_execution(
            function=main.load_me,
            function_var=0)

        # zoom buttons with a person on it
        main.add_texture_button(
            texture_from_res=main.res["Mensch"].duplicate(),
            scene=scene,
            function_execution_id=feid,
            x=700,
            y=450
        )

    # ==================================================================================================================
    # RIDDLE 8
    # ==================================================================================================================

    # Riddle number 8, (sudoku riddle)
    def riddle8(self, scene, main):
        # zooming the riddle image
        feid = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Sudokub"].duplicate()
        )

        # image with the bed
        main.add_image(
            texture_from_res=main.res["Bett"].duplicate(),
            scene=scene
        )

        # zoom buttons with a frame on it
        main.add_texture_button(
            texture_from_res=main.res["Bilderrahmena"].duplicate(),
            scene=scene,
            function_execution_id=feid,
            x=1000,
            y=490
        )



    # ==================================================================================================================
    # RIDDLE 9
    # ==================================================================================================================

    # Riddle number 9, (music riddle)
    def riddle9(self, scene, main):
        main.add_image(
            texture_from_res=main.res["Musik"].duplicate(),
            scene=scene,
            x=950,
            y=300
        )

    # ==================================================================================================================
    # RIDDLE 10
    # ==================================================================================================================

    # Riddle number 10, (birthday riddle)
    def riddle10(self, scene, main):

        # loading dialog for riddle
        feid =main.Executor.add_execution(
            function=main.load_birthday,
            function_var=0)
        # image with the bed
        main.add_image(
            texture_from_res=main.res["Bett"].duplicate(),
            scene=scene
        )

        # zoom buttons with a frame on it
        main.add_texture_button(
            texture_from_res=main.res["Mensch"].duplicate(),
            scene=scene,
            function_execution_id=feid,
            x=900,
            y=600
        )



    # ==================================================================================================================
    # RIDDLE 11
    # ==================================================================================================================

    # Riddle number 11, (maths riddle)
    def riddle11(self, scene, main):
        main.add_image(
            texture_from_res=main.res["Mathe"].duplicate(),
            scene=scene,
            x=950,
            y=400
        )

    # ==================================================================================================================
    # RIDDLE 12
    # ==================================================================================================================

    # Riddle number 12, (pages riddle)
    def riddle12(self,scene,main):
        # zooming the riddle image
        feid = main.Executor.add_execution(
            function= main.add_priority_image,
            function_var= main.res["Buch"].duplicate()
        )
        # image with the bed
        main.add_image(
            texture_from_res=main.res["Bett"].duplicate(),
            scene=scene
        )

        # zoom buttons with a frame on it
        main.add_texture_button(
            texture_from_res=main.res["Buch1"].duplicate(),
            scene=scene,
            function_execution_id=feid,
            x=251,
            y=725
        )



    # ==================================================================================================================
    # RIDDLE 13
    # ==================================================================================================================

    # Riddle number 13, (chemics riddle)
    def riddle13(self,scene,main):
        # zooming the riddle image
        feid = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Chemie"].duplicate()
        )

        # image with the bed
        main.add_image(
            texture_from_res=main.res["Bett"].duplicate(),
            scene=scene
        )

        # zoom button with a frame on it
        main.add_texture_button(
            texture_from_res=main.res["Erlenmeyerkolben"].duplicate(),
            scene=scene,
            function_execution_id=feid,
            x=250,
            y=575
        )


    # ==================================================================================================================
    # RIDDLE 14
    # ==================================================================================================================

    # Riddle number 14, (objects riddle)
    def riddle14(self,scene,main):
        # zooming the riddle images
        feida = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Karton1"].duplicate()
        )
        feidb = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Karton2"].duplicate()
        )
        feidc = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Karton3"].duplicate()
        )
        # image with the bed
        main.add_image(
            texture_from_res=main.res["Bett"].duplicate(),
            scene=scene
        )

        # zoom buttons with a frame on it
        main.add_texture_button(
            texture_from_res=main.res["Box1"].duplicate(),
            scene=scene,
            function_execution_id=feida,
            x=868,
            y=545
        )
        main.add_texture_button(
            texture_from_res=main.res["Box3"].duplicate(),
            scene=scene,
            function_execution_id=feidb,
            x=840,
            y=666
        )
        main.add_texture_button(
            texture_from_res=main.res["Box2"].duplicate(),
            scene=scene,
            function_execution_id=feidc,
            x=910,
            y=687
        )



    # ==================================================================================================================
    # RIDDLE 15
    # ==================================================================================================================

    # Riddle number 15, (light riddle)
    def riddle15(self,scene,main):
        # zooming the riddle image
        feid= main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Leuchten"].duplicate()
        )
        # image that creates light
        main.add_image(
            texture_from_res=main.res["Licht"].duplicate(),
            scene=scene
        )

        # zoom button with a frame on it
        main.add_texture_button(
            texture_from_res=main.res["Schalter"].duplicate(),
            scene= scene,
            function_execution_id=feid,
            x=614,
            y=430
        )



    # ==================================================================================================================
    # RIDDLE 16
    # ==================================================================================================================

    # Riddle number 16, (numbers riddle)
    def riddle16(self,scene,main):
        # zooming the riddle image
        feid = main.Executor.add_execution(
            function=main.add_priority_image,
            function_var=main.res["Zahlen"].duplicate()
        )

        # zoom button with a frame on it
        main.add_texture_button(
            texture_from_res=main.res["xy"].duplicate(),
            scene=scene,
            function_execution_id=feid,
            x=50,
            y=650
        )
