# -*- coding: utf-8 -*-
# Author: mihcuog@AILab
# Contatct: AI-Lab - Smart Things
# File running download video from youtube

from classes.X_GUI import ProgramGUI
from functions.aux_functions import createDesktopShortcut

def main():
    createDesktopShortcut()
    programGUI = ProgramGUI()
    programGUI.initGUI()

if __name__ == "__main__":
    main()
