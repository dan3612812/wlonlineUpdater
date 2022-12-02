from os.path import normpath

programPath = normpath("\\".join(__file__.split(
    "\\")[::-1][3::][::-1]))
