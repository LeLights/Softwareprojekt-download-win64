# ======================================================================================================================
# TITLE: 		Main.py
# AUTHOR: 		Anika Seidel
# 				Cedric Rönnfeld
# 				Till Mack
# 				Florian Lehmann
# LAST EDIT: 	21.03.2021
# ======================================================================================================================


# ======================================================================================================================
# IMPORTING
# ======================================================================================================================

from godot import *
from random import randrange, choice
from .Constructor import Constructor
from .Dialog import Dialog
from .Executor import Executor
from .RiddleCollection import RiddleCollection, riddlelist
from .Resources import load
from .Debugger import debug

import os
import json
import hashlib

DEFAULT_RESOLUTION = Vector2(1920, 1080)

# CHEATS AND DEBUGGING #
ALL_KEYS = False
DEBUGGING = False

num_to_text = {
	1: "First",
	2: "Second",
	3: "Third"
}

# ======================================================================================================================
# MAIN CLASS
# ======================================================================================================================

# Main handler, used by Godot on startup as the default

@exposed
class Main(Node2D):

	# ==================================================================================================================
	# CALLED ONCE
	# ==================================================================================================================

	def _ready(self):

		# ==============================================================================================================
		# DEFINING VARS
		# ==============================================================================================================

		self.res = load()								# Load resources
		self.freeze = True								# Freeze Boolean to disable some actions if needed
		self.scene = None								# Pointer to current Room
		self.ui = None									# Pointer to current UI-Element
		self.audio = AudioStreamPlayer.new()			# Pointer to the AudioManager
		self.call_volume(60.0)							# Adjust Volume to an None-Deaf percentage
		self.last_audio = None							# Pointer to the last played audio
		self.add_child(self.audio)						# Adding the AudioManager
		debug("con", "Added the audio node as a child of main node")
		self.priority_image = None						# Pointer to current Priority-Image

		# ==============================================================================================================
		# DEFINING OBJECTS
		# ==============================================================================================================

		self.Executor = Executor()						# Initiating Executor
		self.Constructor = Constructor(self)			# Initiating Constructor
		SIZE = self.Constructor.SIZE					# Getting Size of the Prison
		self.START = randrange(0, SIZE-1) + SIZE		# Chose random Starting-Position for the Player
		self.add_key(self.START - SIZE)					# Open Cell of random Starting-Position
		self.Player = self.res["Player"].instance()		# Defining the Player
		self.Player.init(self.START, SIZE)				# Initiating the Player

		# ==============================================================================================================
		# DEFINING CONNECTIONS
		# ==============================================================================================================

		self.on_resize()								# Calling a Initial-Resize
		self.update_audio()								# Calling a Initial-Audio-Start
		self.get_tree().get_root().connect("size_changed", self, "on_resize")  # Connecting Resize to on_resize()
		self.audio.connect("finished", self, "update_audio")				   # Connecting  Audio-Finish to add_audio()

		self.call_main_menu()							# Initiating MainMenu

	# ==================================================================================================================
	# CALLED EVERY FRAME
	# ==================================================================================================================

	def _process(self, delta):
		# Check for Freeze before checking for Keyboard-Inputs
		if not self.freeze:
			# Check if Priority Image should be closed
			if Input.is_action_just_pressed("ui_end"):
				debug("key", "Player pressed 'ui_close' key")
				if self.priority_image is not None:
					if DEBUGGING: print("Closing current priority Image")
					self.close(self.priority_image)
					self.scene.modulate = Color(1.0, 1.0, 1.0, 1.0)
					self.priority_image = None


			# Check for movement
			movement_bool = False
			# check for move left key
			if Input.is_action_just_pressed("ui_left"):
				movement_bool = True
				debug("key", "Player pressed 'move_left' key")

			# check for move right key
			if Input.is_action_just_pressed("ui_right"):
				movement_bool = True
				debug("key", "Player pressed 'move_right' key")

			# check for move up key
			if Input.is_action_just_pressed("ui_up"):
				movement_bool = True
				debug("key", "Player pressed 'move_up' key")

			# check for move down key
			if Input.is_action_just_pressed("ui_down"):
				movement_bool = True
				debug("key", "Player pressed 'move_down' key")

			# check if any move got executed
			if movement_bool:
				size = self.Constructor.SIZE
				current = self.Player.get_current()
				Type = None
				if current < size and current % (size / 4) == 0: Type = "Corner"
				elif current < size and not current % (size / 4) == 0: Type = "Hall"
				elif current < 2 * size: Type = "Cell"
				elif current == 2 * size: Type = "Canteen"
				elif current == 2 * size + 1: Type = "Tower"
				move = None
				move = -2 if Input.is_action_just_pressed("ui_left") and Type in ["Corner", "Hall"] else move
				move = -1 if Input.is_action_just_pressed("ui_right") and Type in ["Corner", "Hall"] else move
				move = -3 if Input.is_action_just_pressed("ui_up") and Type in ["Corner", "Hall"] else move
				move = 2 * size + 1 if Input.is_action_just_pressed("ui_up") and Type in ["Canteen"] and self.Player.get_cigs() == 4 else move
				move = -4 if Input.is_action_just_pressed("ui_down") and Type in ["Canteen"] else move
				move = -3 if Input.is_action_just_pressed("ui_down") and Type in ["Cell"] else move
				move = 2 * size if Input.is_action_just_pressed("ui_down") and Type in ["Hall"] else move
				try:
					self.execute(self.Executor.add_execution(self.call_switch, move))
				except:
					pass

			if Input.is_action_just_pressed("open_map"):
				debug("key", "Player pressed 'open_map' key")
				self.add_map(self.Player.get_current())

			if Input.is_action_just_released("open_map"):
				debug("key", "Player released 'open_map' key")
				self.close(self.ui)
				self.call_switch(self.Player.get_current())

			if Input.is_action_just_pressed("open_help"):
				debug("key", "Player pressed 'open_help' key")
				self.load_help(0)

		if Input.is_action_just_pressed("toggle_fullscreen"):
			debug("key", "Player pressed 'toggle_fullscreen' key")
			OS.set_window_fullscreen(not OS.window_fullscreen)

# ======================================================================================================================
# FUNCTION DEFINITIONS - MICRO SERVICE
# ======================================================================================================================

	# ==================================================================================================================
	# CALL EVENTS
	# ==================================================================================================================

	# Function to open the MainMenu
	def call_main_menu(self):
		MainMenu = Node2D.new()							# Creating Drawing-Canvas for MainMenu

		self.add_image(									# Adding MainMenu-Background
			scene=MainMenu, 							# to MainMenu-Canvas
			texture_from_res=self.res["MainMenuBG"]		# Getting Background Image from Res
		)

		self.add_image(									# Adding Title
			scene=MainMenu, 							# to MainMenu-Canvas
			texture_from_res=self.res["Title"], 		# Getting Background Image from Res
			x=300, 										# Setting X-Coordinate Position
			y=100										# Setting Y-Coordinate Position
		)

		id1 = self.Executor.add_execution(self.load_start, None)								 # Create_exe start
		id2 = self.Executor.add_execution(self.close_and_execute, {"scene": MainMenu, "id": id1})# Add_exe close & start

		self.add_label(									# Adding Credits
			scene=MainMenu,								# to MainMenu-Canvas
			text="Credits :\n"							# Setting Credits String				
				"   Anika S. \n"
				"   Florian L. \n"
				"   Cedric R. \n"
				"   Till M. \n",
			x=100,										# Setting X-Coordinate Position
			y=300										# Setting Y-Coordinate Position
		)

		START = self.create_text_button(				# Defining Start-Button
			text="Start",								# Setting Button String
			x=100,										# Setting X-Coordinate Position
			y=880,										# Setting Y-Coordinate Position
			function_execution_id=id2					# Setting Execution id of Function, which should be Executed
		)

		START.rect_size = Vector2(400, 100)				# Setting Size of Start-Button
		MainMenu.add_child(START)						# Adding Start-Button to MainMenu
		debug("con", "Added the start button node as a child of main menu node")

		self.add_slider_input(							# Adding volume-Slider
			scene=MainMenu,								# to MainMenu
			x=1560,										# Setting X-Coordinate Position
			y=1050										# Setting Y-Coordinate Position
		)

		self.add_image(									# Adding Sound-Icon
			scene=MainMenu,								# to MainMenu
			x=1870,										# Setting X-Coordinate Position
			y=1043,										# Setting Y-Coordinate Position
			texture_from_res=self.res["SoundIcon"]		# Getting Sound-Icon from Res
		)

		self.add_child(MainMenu)						# Open MainMenu
		debug("con", "Added the main menu node as a child of main node")

	# Function for the end dialog
	def call_end_win(self, a):
		for child in self.get_children():					# Get everything which is being displayed
			child.queue_free()								# Delete it
		self.add_main_dialog(								# Open End_Win Dialog
			"end_win", 										# Setting Dialog Identifier
			"Jason", 										# Setting Dialog-Partner
			y=-200											# Setting Y-Coordinate Position
		)

	# Function to open the GameOverMenu
	def call_end_menu(self):
		for child in self.get_children():							 # Get everything which is being displayed
			child.queue_free()										 # Delete it
		scene = Node2D.new()										 # Creating Drawing-Canvas for GameOverMenu
		id = self.Executor.add_execution(self.call_game_over, None)  # Add Execution for call_game_over

		self.add_label(												 # Add GameOver Title
			scene=scene, 											 # to GameOverMenu
			text="Game Over",										 # Setting Game Over String
			x=DEFAULT_RESOLUTION.x/2 - 75, 							 # Setting X-Coordinate Position from Mid-Point
			y=DEFAULT_RESOLUTION.y/2 - 300							 # Setting Y-Coordinate Position from Mid-Point
		)

		self.add_text_button(										 # Add Back to Start Button
			scene=scene, 											 # to GameOverMenu
			text="Zurück zum Start",  								 # Setting Back to Start String
			x=DEFAULT_RESOLUTION.x/2 - 112,							 # Setting X-Coordinate Position from Mid-Point
			y=700, 													 # Setting Y-Coordinate Position
			function_execution_id=id								 # Setting Execution id of Button
		)

		self.add_child(scene)												# Open GameOverMenu
		debug("con", "Added the end menu node as a child of main node")

	# Function to open the HighScore menu at the end of the end dialog
	def call_score_menu(self):
		for child in self.get_children():								  # Get everything which is being displayed
			child.queue_free()											  # Delete it
		scene = Node2D.new()											  # Creating Drawing-Canvas for ScoreMenu

		id = self.Executor.add_execution(self.call_game_over, None)		  # Adding Execution for call_game_over

		self.add_label(													  # Add Title
			scene=scene,  												  # to ScoreMenu
			text="Du hast es geschafft !!",								  # Setting Title String
			x=DEFAULT_RESOLUTION.x/2 - 150,								  # Setting X-Coordinate Position from Mid-Point
			y=DEFAULT_RESOLUTION.y/2 - 300								  # Setting Y-Coordinate Position from Mid-Point
		)

		self.add_label(														 # Add Score Display
			scene=scene,													 # to ScoreMenu
			text="Dein Score ist : " + str(round(self.Player.get_score())),  # Setting Score Text with Score from Player
			x=DEFAULT_RESOLUTION.x/2 - 135,								  # Setting X-Coordinate Position from Mid-Point
			y=DEFAULT_RESOLUTION.y/2 - 400								  # Setting Y-Coordinate Position from Mid-Point
		)

		self.add_text_button(											  # Add Back to Start Button
			scene=scene,												  # to ScoreMenu
			text="Zurück zum Start",									  # Setting Back to Start String
			x=DEFAULT_RESOLUTION.x/2 - 112,								  # Setting X-Coordinate Position from Mid-Point
			y=700, 														  # Setting Y-Coordinate Position
			function_execution_id=id								 	  # Setting Execution if of Button
		)

		self.add_child(scene)												# Open ScoreMenu
		debug("con", "Added the score menu node as a child of main node")

	# Function to check if an Password-Input is the right one
	def call_check(self, answer):
		self.scene.modulate = Color(1.0, 1.0, 1.0, 1.0)					  	# Darken the Scene
		riddle_str = self.Player.get_current_riddle()						# Getting current Riddle-String
		self.close(self.ui)													# Closing Input

		# because you should enjoy our game, we hashed the passwords,so that you can't cheat
		passwords = {
			"uhr": 			["2fff34d191bba06fb75656221c86a25ac8da7d4de4d422f2a7d94163352b4a90"],
			"sudoku": 		["47ac62edfb4591f3272ed7afe81a824df595d7bc1facb930399e2c31aafc2de0"],
			"ecken" : 		["6739d7f3fdec51c4dde1605df9e89ac803d9192425dd69a77caf22accd824200"],
			"vigenere": 	["8812f9ddb860c21e316b26b24da1c857fa9208e440127380459248ce23ba0f78",
							 "86412f67842d001875cce8e805f968e92ce6a698a6f40270e42e6accf3ec568f",
							 "3828fd2f9b3c907b3ef3418f5415082087e82ef50ef8a6c6a001bdf916e129e9",
							 "df47849e971fcaa48c239f7ecb57c4b3439d9e8aa9ab35a299a78338de01d082"],
			"striche": 		["5fa3188cc950d6d3a7806ffa0cd2addce49dbcdb24cbc2e37abc2fba24b5b1e0",
							 "c55da503600697df3f5d1097c0fca18e47d8f9446ed3a5d465cc8ddb387e977f"],
			"umschlag": 	["19158c4a7252e121f7367e7e86a3baabbf93fded76110076cfab2b31eb7df887"],
			"rahmen": 		["82e6cca4de612976839b3f5debb8bb4b10e0e7d1226ba06fa9376d5fb8a3f85e"],
			"player": 		["03a3d955b8799a90f1ff5a39479fde8e618f8ca3282d5b187186f2cf361abd32"],
			"sudokub": 		["6d74723c3105966e3bfda900f70004bba9ea1aceb26b4f02a12e16f3cb041f18"],
			"musik": 		["7899c152b1dc06f8cd8b59916aedcfea97714f77ac6ef256edac85fe4c759e1c",
					  		 "3dffc13f0bde086c321569b3c108df473321f6c7573b986641f57900c023eaba"],
			"geburtstag": 	["5ad4fca71d720f79036d7ba27b999f6a423d69b57877558d43e5d6bdd7b7a8a9"],
			"mathe": 		["ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d"],
			"gruenBett":	["8527a891e224136950ff32ca212b45bc93f69fbb801c3b1ebedac52775f99e61"],
			"schalter": 	["4a2f0440723b8c7d2de7b3630d4baf2efd150930d8c91251a4f4279d7800c962"],
			"gruenZahlen": 	["624b60c58c9d8bfb6ff1886c2fd605d2adeb6ea4da576068201b6c6958ce93f4"],
			"chemie" : 		["03fc7970516f9e6b75fd68f92e0372d70ff0f2382bddae7a099de87ac2f64350"],
			"objekte": 		["86b700fab5db37977a73700b53a0654b21bdad0896914cc19ad70dee5f5fb3f6",
							 "1e5ee5e58c8f490ae68e7e91b1575ebefc2bf6c211f302a553ff0c4925e85321",
							 "c86a2932e1c79343a3c16fb218b9944791aaeedd3e30c87d1c7f505c0e588f7c",
							 "10ba045e9ee40807e57f6093280b9fa9eaf640ba4955e340ae4c749382ad96fc",
							 "6cb6d4b2fa122bf8bd63280061e4a230565fdec3ce03268caa2f48ccd931c691",
							 "8f97d9164b8fa131f0361abbe49fe706d3abfd77663ed7939ee20d361a0c6a67"]
		}

		# check password
		if str(hashlib.sha256(str(answer).encode()).hexdigest()) in passwords[str(riddle_str)]:
			if DEBUGGING: print("Code was correct")
			# load dialog, because you solved the riddle
			self.add_dialog(dialog_str="riddle_solved", name="Mr. James")
			self.Player.reset_life()							# reset life, because you have 3 again in a new riddle
			self.update_hearts()													# update hearts
			self.Player.call_move(self.add_random_key() + self.Constructor.SIZE ) 	# load new random cell
		else:
			if DEBUGGING: print("Code was wrong : " + str(answer) + " is not " + str(passwords[str(riddle_str)]))
			# loose life
			self.Player.decrease_life()

			if self.Player.get_life() == 0:							# game over
				self.call_end_menu()								# load end dialog
			else:
				self.Player.decrease_score_by(0.30) 				# decrease the highscore because of loosing life
				self.update_hearts() 								# update heart images

				if DEBUGGING: print("New Life Count " + str(self.Player.get_life()))
				# load dialog because you failed riddle
				self.add_dialog(dialog_str="riddle_failed", name="Mr. James")

	# Function to set Music-Volume
	def call_volume(self, volume):
		if DEBUGGING: print("Updated Volume : " + str(volume))
		self.audio.set_volume_db(int(-(98-volume)))					# set Volume

	# Function to reload the Game
	def call_game_over(self, a):
		self.get_tree().reload_current_scene()						# Reload Main

	# Function to navigate in the Prison
	def call_switch(self, SceneIndex):
		if not self.freeze:
			AllRooms = self.Constructor.get_all_rooms()
			SIZE = self.Constructor.SIZE

			# Check if call_switch should move the player to the Right or Left and the Player is not in a Cell
			if -3 < SceneIndex < 0 and self.Player.get_current() < SIZE:
				if SceneIndex == -1:								# Check if call_switch should go to the right
					SceneIndex = self.Player.get_current() + 1
				elif SceneIndex == -2:								# Check if call_switch should go to the left
					SceneIndex = self.Player.get_current() - 1

				if SceneIndex >= SIZE: SceneIndex -= SIZE			# Make Movement Loop through setback if not in Cell
				if SceneIndex < 0: SceneIndex += SIZE				# Make Movement Loop through push

			elif SceneIndex == -3:									# Check if call_switch should enter or exit a Cell
				if self.Player.get_current() < SIZE:				# Enter Cell
					SceneIndex = self.Player.get_current() + SIZE
				else:												# Exit Cell
					SceneIndex = self.Player.get_current() - SIZE

			elif SceneIndex == -4:								# Check if call_switch should get back to the last Hall
				last = self.Player.get_last()					# Getting last
				if last >= self.Constructor.SIZE:				# Check if last is a Cell
					last -= self.Constructor.SIZE				# Getting associated Hall
				SceneIndex = last

			elif 0 <= SceneIndex: pass					# Check if call_switch was given a SceneIndex for a real Scene

			else: return						# If in Cell and call_switch should not move out of the Cell, don't move

			# Check if the Player is allowed to Move to the SceneIndex based on Keys or Cheats
			if SceneIndex < SIZE or SceneIndex >= SIZE*2 or SceneIndex - SIZE in self.Constructor.Open or ALL_KEYS:

				if self.scene is not None:						# Update Saved Room State if Scene is loaded
					self.remove_child(self.scene)				# Unload loaded Room
					self.Constructor.call_update_room(self.Player.get_current(), self.scene)  # Update Room

				self.Player.call_move(SceneIndex)				# Move the Player

				if AllRooms[SceneIndex] is not None:			# Check if Moving Target already exists in Room Save
					Room = AllRooms[SceneIndex]					# Load Scene from Room Save
				else:
					Room = self.Constructor.add_room()			# or Create Room

				self.scene = Room["RoomInstance"]				# Updating MainScenePointer
				self.add_child(self.scene)						# loading Room
				debug("con", "Added a room node with scene index of " + str(SceneIndex) + "as a child of main node")

				self.on_enter_room(Room["RoomInstance"], Room["Type"], SceneIndex)		# Call on_entered_room
			else:
				self.add_dialog("door","Tür")

	# ==================================================================================================================
	# ADD FUNCTIONS ( 	# IMAGES / ZOOMED / LABELS / INPUTS #  )
	# ==================================================================================================================

	# Function to add an Image
	def add_image(self, texture_from_res, scene=None, x=DEFAULT_RESOLUTION.x / 2, y=DEFAULT_RESOLUTION.y / 2):
		if scene is None: scene = self.scene								# Setting Scene if none was given
		pos = self.convert_pos(x, y)										# Converting the given position to Vector
		new_image = texture_from_res.duplicate()							# Getting Image from res
		new_image.set_position(pos)											# Setting Position of Image
		scene.add_child(new_image)											# Adding Image in Scene
		debug("con", "Added a image node as a child of given scene node")
		return new_image

	# Function to add an PriorityImage
	def add_priority_image(self, TextureFromRes , x=DEFAULT_RESOLUTION.x/2 , y=DEFAULT_RESOLUTION.y/2):
		if self.priority_image is None and not self.freeze:									# Checking for barrier
			self.scene.modulate = Color(0.1, 0.1, 0.1, 1)									# Darken the current Scene
			self.priority_image = self.add_image(TextureFromRes, scene=self, x=x, y=y)		# Opening and Defining
			if DEBUGGING: print("Opened new priority Image " + str(self.priority_image))
			return self.priority_image

	# Function to add an Text
	def add_label(self, text, scene=None, x=0, y=0):
		if scene is None: scene = self.scene			# Setting Scene if none was given
		pos = self.convert_pos(x, y)					# Converting the given position to Vector
		label = Label.new()								# Creating new Label
		label.text = text								# Setting TText of Label
		label.set_position(pos)							# Setting Position of Label
		label.set_theme(self.res["Theme"])				# Setting Appearance of Label
		scene.add_child(label)							# Adding Label in Scene
		debug("con", "Added a label node with text: '" + text + "' as a child of given scene node")
		return label

	# Function to add an TextButton
	def add_text_input(self, scene=None, x=0, y=0, event="text_entered"):
		if scene is None: scene = self						# Setting Scene if none was given
		pos = self.convert_pos(x, y)						# Converting the given position to Vector
		edit = LineEdit.new()								# Creating the LineEdit
		edit.rect_size = Vector2(58, 24)					# Setting Size of LineEdit
		edit.set_position(pos - edit.rect_size*4)			# Setting position of LineEdit
		edit.set_theme(self.res["Theme"])					# Setting Appearance of LineEdit
		edit.connect(event, self, "call_check")				# Connecting LineEdit to call_check
		self.ui = edit										# Updating MainUiPointer
		self.scene.modulate = Color(0.1, 0.1, 0.1, 1)		# Darken the current Scene
		scene.add_child(edit)								# Adding LineEdit in Scene
		debug("con", "Added a Input node as a child of given scene node")
		self.freeze = True									# Setting Freeze, so other objects cant be executed
		if DEBUGGING: print("Added " + str(edit) + " to " + str(scene))

	# Function to add an InputSlider
	def add_slider_input(self, scene=None, x=0, y=0, event="value_changed"):
		if scene is None: scene = self						# Setting Scene if none was given
		pos = self.convert_pos(x, y)						# Converting the given position to Vector
		edit = HSlider.new()								# Creating new Slider
		edit.rect_size = Vector2(300, 16)					# Setting Size of Slider
		edit.set_position(pos)								# Setting Position of Slider
		edit.set_value(60.0)								# Setting Slider default value
		edit.set_theme(self.res["Theme"])					# Setting Appearance
		edit.connect(event, self, "call_volume")			# Connecting SliderUpdate to call_volume
		scene.add_child(edit)								# Adding Slider to Scene
		debug("con", "Added a Slider node as a child of given scene node")
		if DEBUGGING: print("Added " + str(edit) + " to " + str(scene))

	# ==================================================================================================================
	# BUTTON FUNCTIONS
	# ==================================================================================================================

	# Function to add to a Button given attributes
	def __create_button(self, button, function_execution_id=None, x=0, y=0, event="pressed"):
		# Convert and Set Position
		pos = self.convert_pos(x, y)
		button.set_position(pos)

		# Check if there is a function to add to pressed
		if function_execution_id is not None:
			# Pass function Execution ID converted for Godot in Array
			arr = Array()
			arr.append(function_execution_id)
			button.connect(event, self, "execute", arr)

		if DEBUGGING: print("Created " + str(button))
		return button

	# Function to create a Text-Button
	def create_text_button(self, text="", function_execution_id=None, x=0, y=0, event="pressed"):
		# Create TextButton
		button = Button.new()
		button.text = text
		button.set_theme(self.res["Theme"])

		# Modify with basics
		button = self.__create_button(button, function_execution_id, x, y, event)

		return button

	# Function to create a Texture-Button
	def create_texture_button(self, texture_from_res, function_execution_id=None, x=0, y=0, event="pressed"):
		# Create TextureButton
		button = TextureButton.new()
		button.texture_normal = texture_from_res.texture

		# Modify with basics
		button = self.__create_button(button, function_execution_id, x, y, event)

		return button

	# Function to add a Text-Button
	def add_text_button(self, text="", scene=None, function_execution_id=None, x=0, y=0, event="pressed"):
		if scene is None: scene = self.get_child(0)
		button = self.create_text_button(text, function_execution_id, x, y, event)
		scene.add_child(button)
		debug("con", "Added a button node with the text: '" + text + "' as a child of given scene node")
		return button

	# Function to add a Texture-Button
	def add_texture_button(self, texture_from_res, scene=None, function_execution_id=None, x=0, y=0, event="pressed"):
		if scene is None: scene = self.get_child(0)
		button = self.create_texture_button(texture_from_res, function_execution_id, x, y, event)
		scene.add_child(button)
		debug("con", "Added a button node with an image as a child of given scene node")
		return button

	# ==================================================================================================================
	# KEY MANAGEMENT FUNCTIONS
	# ==================================================================================================================

	# Function to add a key and unlock a Cell
	def add_key(self, key):
		if len(self.Constructor.Keys) > 0 and key in self.Constructor.Keys:
			self.Constructor.Keys.pop(self.Constructor.Keys.index(key))
			self.Constructor.Open.append(key)
			if DEBUGGING: print("Added Key for relative Cell Index " + str(key))
			return key
		return None

	# Function to add a random key and unlock a random Cell, which hasn't been opened yet
	def add_random_key(self):
		return self.add_key(choice(self.Constructor.Keys))

	# ==================================================================================================================
	# UI FUNCTIONS
	# ==================================================================================================================

	# Function to add a MainDialog
	def add_main_dialog(self, dialog_str, name, x=0, y=0):
		dia = self.add_dialog(dialog_str, name, x, y)
		dia.get_child(1).set_position(Vector2(700, 400))
		dia.get_child(2).set_position(Vector2(700, 500))

	# Function to add a Dialog
	def add_dialog(self, dialog_str, name, x=0, y=0):
		if not self.freeze:
			pos = self.convert_pos(x, y)
			dialog_box = Node2D.new()
			dialog_box.set_position(pos)
			dialog = Dialog(self.res["Dialogs"][dialog_str], self, dialog_box)

			self.add_image(texture_from_res=self.res["DialogBG"], scene=dialog_box, x=DEFAULT_RESOLUTION.x / 2, y=DEFAULT_RESOLUTION.y / 2)
			self.add_label(text=name, scene=dialog_box, x=20, y=790)
			debug("dia", "New Dialog with the name of dialog partner: " + name)
			id = lambda x: self.Executor.add_execution(dialog.next_dialog_part, {"used": dialog.dia_data["following"][x], "kw": dialog.dia_data["func_kw"][x]})
			text = choice(dialog.dia_data["other"])
			l = self.add_label(text=text, scene=dialog_box, x=20, y=850)
			debug("dia", "Dialog partner said: '" + text + "'" )
			l.set_autowrap(True)
			l.set_size(self.convert_pos(x=640, y=0))

			for i in range(len(dialog.dia_data["responses"])):
				num = str(i+1) + "."
				if i == 0: num = " " + num
				self.add_label(text=num, scene=dialog_box, x=700, y=850 + 50 * i)
				text = choice(dialog.dia_data["responses"][i])
				self.add_text_button(text=text, scene=dialog_box, x=740, y=850 + 50 * i, function_execution_id=id(i))
				debug("dia", num_to_text[i+1] + "option of the player is: '" + text + "' with the keyword: '" + str(dialog.dia_data["func_kw"][i]) + "'")

			# Finishing Up
			del dialog
			self.ui = dialog_box
			self.add_child(dialog_box)
			debug("con", "Added a dialog box with dialog name: '" + dialog_str + "' node as a child of given scene node")
			self.freeze = True
			debug("con", "Added a new dialog box from the dialog: '" + dialog_str + "'")
			return dialog_box

	# Function to add a Map
	def add_map(self, current):
		Map = Node2D.new()
		Scale = (666 / ((self.Constructor.SIZE / 4 - 1) * 10 + 2 * 15)) * 0.9

		#functions to close the map
		exe = self.Executor.add_execution(self.call_switch, self.Constructor.SIZE*2)
		exe1 = self.Executor.add_execution(self.close_and_execute, {"scene": self.ui, "id": exe})
		exe3 = self.Executor.add_execution(self.call_switch, current)
		exe2 = self.Executor.add_execution(self.close_and_execute, {"scene": self.ui, "id": exe3})
		#button to jump to cantine
		button = self.create_text_button(text="K", x=DEFAULT_RESOLUTION.x/2, y=DEFAULT_RESOLUTION.y/2, function_execution_id=exe1)
		button.rect_size *= Scale / 6
		#button to close map
		xbutton= self.create_text_button(text="close",function_execution_id=exe2,x=1200, y=220, event="pressed")
		#map background
		self.add_image(texture_from_res=self.res["MapBG"].duplicate(), scene=Map)

		#if current scene is cantine, add red dot to cantine
		if current == self.Constructor.SIZE * 2:
			dot = self.res["RedDot"].duplicate()
			dot.scale *= Scale
			pos = DEFAULT_RESOLUTION / 2
			dot.set_position(pos)
			Map.add_child(dot)
		Map.add_child(xbutton)
		Map.add_child(button)
		debug("con", "Added a Button node as a child of the map node")

		flip = 0
		position = Vector2((self.Constructor.SIZE / 4)/2 * 10, -(self.Constructor.SIZE / 4)/2 * 10)
		direction = Vector2(0.0, 0.0)

		for Cells in enumerate(self.Constructor.Cells):
			Room = Sprite.new()
			exe = self.Executor.add_execution(self.call_switch, Cells[0])
			exe1 = self.Executor.add_execution(self.close_and_execute, {"scene": self.ui, "id": exe})

			if not (Cells[0] % (self.Constructor.SIZE / 4) == 0):
				if Cells[1] is not None:
					Room = self.res["MapCell"].duplicate()
				else:
					Room = self.res["MapCellClosed"].duplicate()
				pos = (DEFAULT_RESOLUTION / 2 + position * Scale) - Vector2(-direction.y, direction.x) * 2 * Scale

			else:
				flip += 1
				if flip == 1: direction = Vector2(0.0, 1.0)
				if flip == 2: direction = Vector2(-1.0, 0.0)
				if flip == 3: direction = Vector2(0.0, -1.0)
				if flip == 4: direction = Vector2(1.0, 0.0)

				if Cells[1] is not None:
					Room = self.res["MapCorner"].duplicate()
				else:
					Room = self.res["MapCornerClosed"].duplicate()
				pos = DEFAULT_RESOLUTION / 2 + position * Scale

			Room.scale *= Scale
			Room.rotation_degrees = flip * 90
			Room.set_position(pos)
			button = self.create_text_button(text=str(Cells[0]), x=pos.x, y=pos.y, function_execution_id=exe1)
			button.rect_size = Vector2(1, 1)
			button.rect_size *= Scale / 6
			Map.add_child(Room)
			debug("con", "Added a room image as a child of the map node")
			#if current scene is a cell, place red button in the current cell
			if current == Cells[0] or current == Cells[0]+self.Constructor.SIZE:
				dot = self.res["RedDot"].duplicate()
				dot.set_position(pos)
				dot.scale *= Scale
				Map.add_child(dot)
				debug("con", "Added the red position dot as a child of the map node")
			Map.add_child(button)
			debug("con", "Added a button node with the text: '" + str(Cells[0]) + "' as a child of the map node")
			position += direction * 10


		self.add_child(Map)
		debug("con", "Added the map node as a child of the main node")
		self.ui = Map
		if DEBUGGING: print("Opened Map " + str(Map))
		return Map

	# ==================================================================================================================
	# RIDDLE FUNCTIONS
	# ==================================================================================================================

	# Setting current Riddle
	def solve_riddle_dialog(self, a):
		try:
			Riddle_Convert = {
				"0": "uhr",
				"1": "sudoku",
				"2": "ecken",
				"3": "vigenere",
				"4": "striche",
				"5": "umschlag",
				"6": "rahmen",
				"7": "player",
				"8": "sudokub",
				"9": "musik",
				"10": "geburtstag",
				"11": "mathe",
				"12": "gruenBett",
				"13": "chemie",
				"14": "objekte",
				"15": "schalter",
				"16": "gruenZahlen"
			}
			active_riddle_str = Riddle_Convert[riddlelist[-1][6:]]
			self.add_dialog(dialog_str=active_riddle_str, name="Mr. James")
			self.Player.set_current_riddle(active_riddle_str)
			if DEBUGGING: print("Updated Current Riddle : " + active_riddle_str)
		except:
			pass

	# ==================================================================================================================
	#
	# ==================================================================================================================

	# Start Help-Dialog
	def load_help(self, a):
		if DEBUGGING: print("Open help")
		self.add_dialog("help", "Anonym")

	# Start Birthday-Dialog
	def load_birthday(self, a):
		if DEBUGGING: print("Open birthday")
		self.add_dialog("birthday", "Zellennachbar")

	# Start Me-Dialog
	def load_me(self, a):
		if DEBUGGING: print("Open me")
		self.add_dialog("me", "Zellennachbar")

	# Start Start-Dialog
	def load_start(self, a):
		self.add_main_dialog("intro", "Unbekannter", y=-200)

	# ==================================================================================================================
	# EXECUTE AND CLOSE
	# ==================================================================================================================

	# Execute a Function
	def execute(self, executer_id):
		MAX_LENGTH = 20
		function_var = self.Executor.Buffer[executer_id][1]
		function = self.Executor.Buffer[executer_id][0]
		var_out = str(function_var)
		if len(var_out) > MAX_LENGTH:
			var_out = var_out[0:MAX_LENGTH]
			var_out += "..."
		if DEBUGGING: print("Executing function " + str(function) + " with Var " + var_out + " at Index " + str(
			executer_id) + " in the Executer Function Buffer")
		function(function_var)

	# Close a Scene
	def close(self, scene):
		if scene is not None:
			scene.queue_free()
			self.freeze = False
			self.ui = None
			if DEBUGGING: print("Closed ", str(scene))

	# Close a Scene and Execute a Function
	def close_and_execute(self, dict):
		self.close(dict["scene"])
		self.execute(dict["id"])

	# ==================================================================================================================
	# CONVERTER FUNCTIONS
	# ==================================================================================================================

	def convert_pos(self, x, y):
		pos = Vector2()
		pos.x = x
		pos.y = y
		return pos

	# ==================================================================================================================
	# UPDATE FUNCTIONS
	# ==================================================================================================================

	# Function to update a Dialog
	def update_dialog(self, dialog_box, label=None, text=None, buttons=None):
		if buttons is None: buttons = []
		if label is not None: dialog_box.get_child(1).text = label
		if text is not None: dialog_box.get_child(2).text = text
		if text != "DEBUG OTHER":
			debug("dia", "Dialog partner said: '" + text + "'")
		for button in dialog_box.get_children()[3:]:
			button.queue_free()
		for i, button in enumerate(buttons):
			num = str(i+1) + "."
			if i == 0: num = " " + num
			self.add_label(text=num, scene=dialog_box, x=700, y=850 + 50 * i)
			dialog_box.add_child(button)
		debug("con", "Updated the dialog box")

	# Function to update the Hearts
	def update_hearts(self):
		scene = self.Constructor.get_all_rooms()[self.Player.get_current()]["RoomInstance"]
		for i in range(3):
			self.close(self.Constructor.heart_images[i])

		self.Constructor.heart_images = [None] * 3
		life = self.Player.get_life()
		if DEBUGGING: print("Updated Hearts : " + str(life))
		for i in range(life):
			self.Constructor.heart_images[i] = self.add_image(
				scene=scene,
				texture_from_res=self.res["Heart"].duplicate(),
				x=75 + i * 100,
				y=75
			)

	# Function to update the Cigarette-Count
	def update_cigs(self):
		scene = self.Constructor.get_all_rooms()[self.Player.get_current()]["RoomInstance"]
		self.close(self.Constructor.cig_counter)
		self.Constructor.cig_counter = None
		self.Constructor.cig_counter = self.add_image(
			scene=scene,
			texture_from_res=self.res["NumRahmen" + str(self.Player.get_cigs())].duplicate(),
			x=1860,
			y=1030
		)
		if DEBUGGING: print("Updated Cigs : " + str(self.Player.get_cigs()))

	# Function to update Volume
	def update_audio(self):
		if self.last_audio is None or self.last_audio == self.res["StopAudio"]:
			self.audio.stream = self.res["StartAudio"]

		elif self.last_audio == self.res["StartAudio"]:
			self.audio.stream = self.res["MainAudio"]

		elif self.last_audio == self.res["MainAudio"]:
			self.audio.stream = choice([self.res["MainAudio"], self.res["StopAudio"]])

		if DEBUGGING: print("Now playing " + str(self.audio.stream))
		self.last_audio = self.audio.stream
		self.audio.play()

	# ==================================================================================================================
	# ON EVENTS
	# ==================================================================================================================

	def on_enter_room(self, Room, Type, Index):
		if DEBUGGING: print("Entered " + str(Room) + " of Type " + Type + " at Index " + str(Index))
		self.update_hearts()
		self.update_cigs()

	def on_resize(self):
		# Default 1920x1080
		size = self.get_viewport_rect().size
		pos_x = 0
		pos_y = 0
		if size.x / DEFAULT_RESOLUTION.x <= size.y / DEFAULT_RESOLUTION.y:
			new_scale = size.x / DEFAULT_RESOLUTION.x
			pos_y = size.y / 2 - DEFAULT_RESOLUTION.y * new_scale / 2
		else:
			new_scale = size.y / DEFAULT_RESOLUTION.y
			pos_x = size.x / 2 - DEFAULT_RESOLUTION.x * new_scale / 2
		self.position = Vector2(pos_x, pos_y)
		self.set_scale(Vector2(new_scale, new_scale))




