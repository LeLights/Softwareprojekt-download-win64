# ======================================================================================================================
# TITLE: 		Constructor.py
# AUTHOR: 		Anika Seidel
# 				Cedric Rönnfeld
# 				Till Mack
# 				Florian Lehmann
# LAST EDIT: 	21.03.2021
# ======================================================================================================================


# ======================================================================================================================
# IMPORTING
# ======================================================================================================================

# using the Node Feature from godot to create scenes
from godot import Node2D

# getting a random float between 0 and 1 for probabilities
from random import uniform

# ======================================================================================================================
# CONSTRUCTOR CLASS
# ======================================================================================================================

# defining the Constructor Class, the main Object to handling the Creation of Rooms
# and to construct the inventory of a scene


class Constructor:

    # setting the size of prison, defined by the room count
    SIZE = 16
    # constant for the amount of cigarettes placed around the prison
    CIG_AMOUNT = 4

    def __init__(self, main):

        # setting the Size of the prison by converting the size to a multiple of four
        self.SIZE = round(abs(self.SIZE) / 4) * 4
        # lists were the state of Halls, Cells, Open and the Canteen, Tower is stored
        self.Halls = [None] * self.SIZE
        self.Cells = [None] * self.SIZE
        self.Open = [None] * self.SIZE
        self.Canteen = [None]
        self.Tower = [None]


        # Setting a empty key list with space for each room
        self.Keys = list(range(0, self.SIZE))

        # adapting the main class from main.py
        self.main = main

        # store the amount of loaded cells and placed cigarettes
        self.loaded_cells_count = 0
        self.placed_cig_count = 0

        # saving the widgits, which should be loaded repeatedly
        self.heart_images = [None] * 3
        self.cig_count_image = None
        self.cig_counter = None

    # ==================================================================================================================
    # GETTING ALL ROOMS
    # ==================================================================================================================

    # get the combination of all possible rooms
    def get_all_rooms(self):
        return self.Halls + self.Cells + self.Canteen + self.Tower

    # ==================================================================================================================
    # CALLING A ROOM UPDATE
    # ==================================================================================================================

    # updating a room, with current means the position of the player and SceneState is the Scene which should load
    def call_update_room(self, current, SceneState):

        # check if the current is smaller than the size of the prison. If so, then its in the corridor
        if current < self.SIZE:
            # if its a multiple of 4, then its in the corner of the corridor, else its a default hallway
            if current % (self.SIZE / 4) == 0:
                Type = "Corner"
            else:
                Type = "Hall"

            # set the state of the hall where the player is in
            self.Halls[current] = {
                "RoomInstance": SceneState,
                "Type": Type
            }

        # check if the current is smaller than twice the size. If so, its a cell
        elif current < self.SIZE * 2:
            Type = "Cell"
            # set the state of the cell where the player is in
            self.Cells[current - self.SIZE] = {
                "RoomInstance": SceneState,
                "Type": Type
            }

        # check if the current is equal than twice the size. If so, its the canteen
        elif current == self.SIZE * 2:
            Type = "Canteen"
            # set the state of the canteen where the player is in
            self.Canteen[0] = {
                "RoomInstance": SceneState,
                "Type": Type
            }

        # check if the current is equal than twice the size plus one. If so, its the tower
        elif current == self.SIZE * 2 + 1:
            Type = "Tower"
            # set the state of the tower where the player is in
            self.Tower[0] = {
                "RoomInstance": SceneState,
                "Type": Type
            }

        # if nothing got triggered, the index isn't declared and a error should be raised
        else:
            return False

        # returning the current room type
        return Type

    # ==================================================================================================================
    # ADDING A NEW ROOM
    # ==================================================================================================================

    # Adding a new room and return its data
    def add_room(self):
        # create the scene as a godot node
        room_scene = Node2D.new()
        # getting the type of the room by updating it
        Type = self.call_update_room(
            current=self.main.Player.get_current(),
            SceneState=room_scene
        )
        # initialize and load the scene
        self.room_init(
            scene=room_scene,
            main=self.main,
            Type=Type
        )
        # return the data of the current room
        return {
            "RoomInstance": room_scene,
            "Type": Type
        }

    # ==================================================================================================================
    # CREATING A CELL NUMBER SIGN
    # ==================================================================================================================

    # Creating the sign for the cell number
    def create_sign(self, current, Type):
        # creating the sign as a new node
        sign = Node2D.new()
        # enumerate over the room indices to create multiple sign images if the room number is a multi-digit integer
        for i, num in enumerate(str(current)):
            # moving the image 100 each digit
            pos = 100 * i
            # creating a duplication of the number image with the corresponding digit and depending of the type
            number = self.main.res[Type + num].duplicate()
            # set its position relative
            number.position += self.main.convert_pos(pos, 0)
            # place it as a sign child
            sign.add_child(number)

        # returning the node
        return sign

    # ==================================================================================================================
    # INITIALIZE A ROOM
    # ==================================================================================================================

    # initialize the room
    def room_init(self, scene, main, Type):
        # loading resource
        res = main.res

        # creating used Execution IDs
        back = main.Executor.add_execution(
            function=main.call_switch,
            function_var=-4
        )
        enter = main.Executor.add_execution(
            function=main.call_switch,
            function_var=-3
        )
        solve_riddle_dialog = main.Executor.add_execution(
            function=main.solve_riddle_dialog,
            function_var=0
        )

        load_help = main.Executor.add_execution(
            function=main.load_help,
            function_var=0
        )

        load_map = main.Executor.add_execution(
            function=main.add_map,
            function_var=self.main.Player.get_current()
        )

        # add the background image
        main.add_image(
            scene=scene,
            texture_from_res=res[Type + "sBG"].duplicate()
        )

        # creating a Help Button, for showing Help Dialog
        main.add_texture_button(
            texture_from_res=main.res["Help"].duplicate(),
            scene=scene,
            function_execution_id=load_help,
            x=1870,
            y=0
        )

        # creating a Map Button, for showing a Map
        main.add_texture_button(
            texture_from_res=main.res["Compass"].duplicate(),
            scene=scene,
            function_execution_id=load_map,
            x=1815,
            y=0
        )

        # if positioned on a corridor
        if Type == "Hall" or Type == "Corner":
            # create executables for moving
            left = main.Executor.add_execution(
                function=main.call_switch,
                function_var=-2
            )
            right = main.Executor.add_execution(
                function=main.call_switch,
                function_var=-1
            )

            # different operations for a hall and for a cell
            if Type == "Hall":
                # create executable for going into canteen
                canteen = main.Executor.add_execution(
                    function=main.call_switch,
                    function_var=main.Constructor.SIZE * 2
                )
                # adding the buttons for moving
                main.add_texture_button(
                    scene=scene,
                    texture_from_res=res["DownArrow"],
                    x=812,
                    y=875,
                    function_execution_id=canteen
                )
                main.add_texture_button(
                    scene=scene,
                    texture_from_res=res["LeftArrow"],
                    x=194,
                    y=350,
                    function_execution_id=left
                )
                main.add_texture_button(
                    scene=scene,
                    texture_from_res=res["RightArrow"],
                    x=1319,
                    y=357,
                    function_execution_id=right
                )
                main.add_texture_button(
                    scene=scene,
                    texture_from_res=res["HallDoor"],
                    x=741,
                    y=281,
                    function_execution_id=enter
                )
                # placing the sign
                main.add_image(
                    scene=scene,
                    texture_from_res=self.create_sign(
                        current=self.main.Player.get_current(),
                        Type=Type
                    ),
                    x=573,
                    y=321
                )

            elif Type == "Corner":
                # adding the buttons for moving
                main.add_texture_button(
                    scene=scene,
                    texture_from_res=res["LeftCornerArrow"],
                    x=33,
                    y=421,
                    function_execution_id=left
                )
                main.add_texture_button(
                    scene=scene,
                    texture_from_res=res["RightArrow"],
                    x=1319,
                    y=357,
                    function_execution_id=right
                )
                main.add_texture_button(
                    scene=scene,
                    texture_from_res=res["CornerDoor"],
                    x=524,
                    y=166,
                    function_execution_id=enter
                )
                # placing the sign
                main.add_image(
                    scene=scene,
                    texture_from_res=self.create_sign(
                        current=self.main.Player.get_current(),
                        Type=Type
                    )
                )

        # if positioned in a cell
        elif Type == "Cell":
            # add a arrow for leaving the cell
            main.add_texture_button(
                scene=scene,
                texture_from_res=res["CellArrow"],
                x=450,
                y=970,
                function_execution_id=enter
            )
            # creating a new riddle if its not existing
            main.res["RiddleCollection"].get_riddle(scene=scene, main=main)(scene=scene, main=main)

            # placing cigarettes with a laplace distribution and a uniform to check the random placement: the
            # favorable are the amount of not placed cigarettes and the possible cases are the amount of unloaded cells
            if uniform(0, 1) < (self.CIG_AMOUNT - self.placed_cig_count) / (self.SIZE - self.loaded_cells_count):
                # increase the amount of placed cigarettes
                self.placed_cig_count += 1
                # executable for adding a new item to the inventory
                add_execution = main.Executor.add_execution(
                    function=self.add_cigarette_item,
                    function_var=[main, "Zigaretten"]
                )
                # executable for closing the button of cigarette
                close_execution = main.Executor.add_execution(
                    function=main.close_and_execute,
                    function_var=None
                )

                # place the four cigarettes on predefined positions
                if self.placed_cig_count == 1:
                    button = main.add_texture_button(
                        texture_from_res=main.res["zigarette"].duplicate(),
                        function_execution_id=close_execution,
                        scene=scene,
                        x=550,
                        y=750
                    )
                elif self.placed_cig_count == 2:
                    button = main.add_texture_button(
                        texture_from_res=main.res["zigarette"].duplicate(),
                        function_execution_id=close_execution,
                        scene=scene,
                        x=1780,
                        y=880
                    )
                elif self.placed_cig_count == 3:
                    button = main.add_texture_button(
                        texture_from_res=main.res["zigarette"].duplicate(),
                        function_execution_id=close_execution,
                        scene=scene,
                        x=230,
                        y=510
                    )
                else:
                    button = main.add_texture_button(
                        texture_from_res=main.res["zigarette"].duplicate(),
                        function_execution_id=close_execution,
                        scene=scene,
                        x=1710,
                        y=740
                    )

                # Change Var in Executor Buffer
                main.Executor.Buffer[close_execution][1] = {
                    "scene": button,
                    "id": add_execution
                }

            # increase the loaded cell count after loading the whole cell
            self.loaded_cells_count += 1

        # if positioned in the canteen
        elif Type == "Canteen":

            # adding buttons for leaving the canteen and talking to Mr. James
            main.add_texture_button(
                scene=scene,
                texture_from_res=res["CanteenArrow"],
                x=850,
                y=967,
                function_execution_id=back
            )
            main.add_texture_button(
                scene=scene,
                texture_from_res=res["Mensch2"],
                x=400,
                y=800,
                function_execution_id=solve_riddle_dialog
            )
            # creating and adding a button with executable for entering the escape tower
            tower = main.Executor.add_execution(
                function=self.tower,
                function_var=[main, scene]
            )
            main.add_texture_button(
                scene=scene,
                texture_from_res=res["TowerDoor"].duplicate(),
                x=900,
                y=804,
                function_execution_id=tower
            )

            main.add_texture_button(
                scene=scene,
                texture_from_res = res["Wärter"].duplicate(),
                x = 930,
                y=830,
                function_execution_id=tower
            )



        # if positioned in the tower
        elif Type == "Tower":
            # create a teleport / escape button
            score_menu = main.Executor.add_execution(
                function=self.main.call_end_win,
                function_var=None
            )
            main.add_texture_button(
                scene=scene,
                texture_from_res=res["TP"].duplicate(),
                x=805,
                y=200,
                function_execution_id=score_menu
            )

        # iterate threw all heart_images and close them if possible
        for i in range(3):
            try:
                main.close(self.heart_images[i])
            except:
                pass

        # loop as often as lifes are left and add a new image of a life
        life = main.Player.get_life()
        for i in range(life):
            self.heart_images[i] = main.add_image(
                scene=scene,
                texture_from_res=res["Heart"].duplicate(),
                x=75 + i*100,
                y=75
            )

        # load a image of a cigarette box
        self.cig_count_image = main.add_image(
            scene=scene,
            texture_from_res=res["Cig_Box"].duplicate(),
            x=1800,
            y=1030
        )

        # load a image of the cigarette count by using the numbers inside a frame
        self.cig_counter = main.add_image(
            scene=scene,
            texture_from_res=res["NumRahmen" + str(main.Player.get_cigs())].duplicate(),
            x=1860,
            y=1030
        )

    # ==================================================================================================================
    # OTHER FUNCTIONS
    # ==================================================================================================================

    # create the function for the tower to check if all cigarettes are collected
    def tower(self, var):
        if var[0].Player.get_cigs() == 4:
            var[0].call_switch(2*self.SIZE+1)
        else:
            var[0].add_dialog("guard","Mr. Guardian")

    # create the funktion for the cigarette adding, where the item gets added and the counter gets updated
    def add_cigarette_item(self, var):
        var[0].Player.add_item(var[1])
        var[0].update_cigs()