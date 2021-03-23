# ======================================================================================================================
# TITLE: 		Debugger.py
# AUTHOR: 		Anika Seidel
# 				Cedric Rönnfeld
# 				Till Mack
# 				Florian Lehmann
# LAST EDIT: 	21.03.2021
# ======================================================================================================================

DEBUG = {
    "KEYS": False,
    "DIALOGS": False,
    "EXECUTOR": False,
    "CONSTRUCTOR": False
}


def debug(key, msg):
    if key == "key" and DEBUG["KEYS"]: print("DEBUG - KEYS:", msg)
    if key == "exe" and DEBUG["EXECUTOR"]: print("DEBUG - EXECUTOR:", msg)
    if key == "dia" and DEBUG["DIALOGS"]: print("DEBUG - DIALOG:", msg)
    if key == "con" and DEBUG["CONSTRUCTOR"]: print("DEBUG - CONSTRUCTOR:", msg)
