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

from .Debugger import debug

# Because of incompatibilities of Python and Godot in Function Management:
# The Executor stores all Functions that are
# Python but have to be Executed by a Godot Object to hand them out on request



# ======================================================================================================================
# EXECUTOR CLASS
# ======================================================================================================================

# defining the Executor, which is an Interface between Godot and Python

class Executor:
    def __init__(self):
        # Initiating the Function-Buffer for Python Function Storage
        self.Buffer = []

    # ==================================================================================================================
    # ADDER AND GETTER
    # ==================================================================================================================

    # Add a Execution Package to the Buffer
    def add_execution(self, function, function_var):
        # Debug Output-Length, set to 0 if you want to output all
        MAX_LENGTH = 20

        # Packaging the Function into a Function-Pack
        pack = [function, function_var]

        # Searching the Buffer for a package, which is the same
        for i, unpack in enumerate(self.Buffer):
            if unpack[0] == pack[0] and unpack[1] == pack[1]:
                # return the already existing package
                return i
        # Else add the package to the Buffer
        self.Buffer.append(pack)
        # Debugging

        str_max = MAX_LENGTH if(len(str(function_var)) > MAX_LENGTH and MAX_LENGTH) else len(str(function_var))
        debug_msg = "Added " + str(pack[0]) + " with Var " + (str(function_var)[0:str_max]) + " to Executor Function Buffer"
        debug("exe", debug_msg)

        # Return the Package index to the Requester
        return len(self.Buffer)-1
