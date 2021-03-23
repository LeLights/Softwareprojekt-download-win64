# ======================================================================================================================
# TITLE: 		Dialog.py
# AUTHOR: 		Anika Seidel
# 				Cedric Rönnfeld
# 				Till Mack
# 				Florian Lehmann
# LAST EDIT: 	21.03.2021
# ======================================================================================================================


# ======================================================================================================================
# IMPORTING
# ======================================================================================================================

#using godot as main engine
from godot import *

# ======================================================================================================================
# PLAYER CLASS
# ======================================================================================================================

# defining the Player Class, the main Object to save player referring variables

@exposed
class Player(Node2D):
	def init(self, START, SIZE):
		# set starting indices
		self.current_scene_index = START
		self.last_scene_index = START - SIZE
		# save the current riddle
		self.current_riddle_str = None
		self.items = {"Zigaretten": 0}
		# count of collected cigarettes
		self.cigs = 0
		# life count
		self.life = 3
		# score
		self.score = 1000



	# ==================================================================================================================
	# MOVING THE PLAYER
	# ==================================================================================================================

	# moving the player by changing the last scene and current scene index by shifting
	def call_move(self, new_current):
		if new_current != self.current_scene_index:
			self.last_scene_index = self.current_scene_index
			self.current_scene_index = new_current

	# ==================================================================================================================
	# GETTER
	# ==================================================================================================================

	# get items dict
	def get_items(self, kw):
		return self.items[kw]

	# get cigarette count
	def get_cigs(self):
		return self.cigs

	# get the current riddle string
	def get_current_riddle(self):
		return  self.current_riddle_str

	# get the current scene index
	def get_current(self):
		return self.current_scene_index

	# get the last scene index
	def get_last(self):
		return self.last_scene_index

	# get the life amount
	def get_life(self):
		return self.life

	# get the score
	def get_score(self):
		return self.score
	# ==================================================================================================================
	# SETTER
	# ==================================================================================================================

	# set a new riddle string
	def set_current_riddle(self, riddle_str):
		self.current_riddle_str = riddle_str

	# add a new item by increasing the referred index
	def add_item(self, item_str):
		# Conversion Godot -> Python
		if isinstance(item_str, GDString):
			item_str = str(item_str)
		self.items[item_str] += 1
		self.cigs +=1

	# remove a item by poping the matching item
	def remove_item(self, item_str):
		for i, item in enumerate(self.items):
			if item == item_str:
				self.items.pop(i)
				return

	# decrease the life count by 1
	def decrease_life(self):
		self.life -= 1

	# reset the life count to 3
	def reset_life(self):
		self.life = 3

	# decrease the score, by subtracting n% of it
	def decrease_score_by(self, multiplicator):
		self.score *= 1-multiplicator
