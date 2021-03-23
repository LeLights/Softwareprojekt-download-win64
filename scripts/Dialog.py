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

# using the re library for filtering in keywords
import re
# getting random dialog expressions
from random import choice
# getting the debug function
from .Debugger import debug

# convert cardinal to ordinal numbers
num_to_text = {
	1: "First",
	2: "Second",
	3: "Third"
}

# ======================================================================================================================
# DIALOG CLASS
# ======================================================================================================================

# defining the Dialog Class, the main Object to handling the dialog box and the process of decision making
# the Class is directly connected to the Main Frame and sends commands to it


class Dialog:
	def __init__(self, dia_data, main_class, dialog_box):

		# get some important objects from the main frame (main object, dialog node, data for dialog)
		self.main_class = main_class
		self.dialog_box = dialog_box
		self.dia_data = dia_data

	# ==================================================================================================================
	# LOADING A NEW DIALOG PART
	# ==================================================================================================================

	# function for loading a new part of a dialog, executed by pressing on a button from the dialog part before

	def next_dialog_part(self, args):

		# start with checking for the keywords and possible functions triggered by the button press
		self.kw_check(args["kw"])

		# define the id of a executable godot function
		def execution_id(index):
			# return the function object suitable for a godot button
			return self.main_class.Executor.add_execution(
				function=self.next_dialog_part,
				function_var={
					"used": args["used"]["following"][index],
					"kw": args["used"]["func_kw"][index]
				}
			)

		# in case you reach the end of a dialog, the following attribute of the dialog part will be empty,
		# if so the dialog box should get closed after pressing any button
		if not len(args["used"]["following"]):
			# redefining the id of a executable godot function
			def execution_id(index):
				# this time the button press should close the dialog box, for this,
				# every button refer to the close_dialog function
				return self.main_class.Executor.add_execution(
					function=self.close_dialog,
					function_var=args["used"]["func_kw"][index]
				)

		# predefine a list with all buttons, which should displayed in the dialog box
		buttons = list()

		debug_msg = []

		# iterate thew the possible responses, for each, define a new button
		for i in range(len(args["used"]["responses"])):
			text = choice(args["used"]["responses"][i])
			buttons.append(
				# creating a button with a text attribute which represent the response option
				self.main_class.create_text_button(
					text=text,
					function_execution_id=execution_id(i),
					# define the position of the button (relativ)
					x=750,
					y=850 + i * 50
				)
			)
			if len(text) != 1:
				debug_msg.append(num_to_text[i + 1] + "option of the player is: '" + text + "' with the keyword: '" + str(args["used"]["func_kw"][i]) + "'")
			else:
				debug_msg.append(None)

		# at the last step, update the dialog box with the new label about the saying of the other person
		# and the buttons which were defined before
		self.main_class.update_dialog(
			dialog_box=self.dialog_box,
			text=choice(args["used"]["other"]),
			buttons=buttons
		)
		for i in range(len(debug_msg)):
			if debug_msg[i]:
				debug("dia", debug_msg[i])

	# ==================================================================================================================
	# KEYWORDS CHECK
	# ==================================================================================================================

	# function to check, if the keyword, given by the last pressed button is referring to a external function
	# This function will be executed with the feature of grouping in regex to use parameters in keywords

	def kw_check(self, kw):

		# the check is based on try-except iterations where a regex expression searches for a keyword
		# referring to a function. If the search wasn't the successful, the search return a None
		# the following group command would fail with an attribute error, and the next keyword get checked

		# checking if the player was unpolite
		try:
			par=re.search(r"^unpolite_(.+)", kw).group(1)
			print("UNPOLITE _________________")
			self.main_class.Player.decrease_score_by(int(par)/100)
		except (AttributeError, TypeError):
			pass

		# checking if the player was polite
		try:
			par = re.search(r"^polite_(.+)", kw).group(1)
			self.main_class.Player.decrease_score_by(-int(par) / 100)
		except (AttributeError, TypeError):
			pass

		# checking if a hint got used
		try:
			re.search(r"hint", kw).group(0)
			self.main_class.Player.decrease_score_by(0.2)
		except (AttributeError, TypeError):
			pass

		# checking if the player requests to input a riddle key
		try:
			re.search(r"open_riddle_input_(.+)", kw).group(1)
			self.main_class.close(self.dialog_box)
			self.main_class.add_text_input(x=1920 / 2, y=1080 / 2)
		except (AttributeError, TypeError):
			pass

		# check for close command
		try:
			re.search(r"^close", kw).group(0)
			self.main_class.close(self.dialog_box)
			self.main_class.call_switch(self.main_class.Player.get_current())
			debug("con", "Closed the dialog box")
		except (AttributeError, TypeError):
			pass

		# check for start command
		try:
			re.search(r"start", kw).group(0)
			self.main_class.close(self.dialog_box)
			self.main_class.call_switch(self.main_class.START)
		except (AttributeError, TypeError):
			pass

		# check if the player wsa uppolite at last msg
		try:
			par = re.search(r"onpolite_and_close_(.+)", kw).group(1)
			self.main_class.Player.decrease_score_by(int(par) / 100)
			self.main_class.close(self.dialog_box)
			self.main_class.call_switch(self.main_class.Player.get_current())
		except (AttributeError, TypeError):
			pass

		# check if the player wsa polite at last msg
		try:
			par = re.search(r"opolite_and_close_(.+)", kw).group(1)
			self.main_class.Player.decrease_score_by(-int(par) / 100)
			self.main_class.close(self.dialog_box)
			self.main_class.call_switch(self.main_class.Player.get_current())
		except (AttributeError, TypeError):
			pass

		# check for call score command
		try:
			re.search(r"call_score", kw).group(0)
			self.main_class.call_score_menu()
		except (AttributeError, TypeError):
			pass

	# ==================================================================================================================
	# OTHER FUNCTIONS
	# ==================================================================================================================

	# if the dialog should be closed after the button press, the keyword check wouldn't be executed,
	# that's why both functions, the close and the check, where compressed into one, which is executable
	def close_dialog(self, kw):
		self.main_class.close(self.dialog_box)
		self.kw_check(kw)
