#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import os

import nuke


def quick_open_file():
    node = nuke.selectedNode()
    folder_name = os.path.dirname(nuke.filename(node))
    if os.path.isdir(folder_name):
        show(folder_name)


def show(path):
    import sys
    if sys.platform == 'win32':
        os.startfile(path)
    elif sys.platform == 'darwin':
        import subprocess
        subprocess.Popen(['open', path])
    elif sys.platform == 'linux2':
        import subprocess
        subprocess.Popen(['xdg-open', path])
    else:
        nuke.alert('not support open file in this OS')


quick_open_file()
