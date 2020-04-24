# -*- coding: utf-8 -*-
"""
:Project: routing_emulator
:File: movable_node.py

:Author: Tanbixuan
:Created: 2020-04-20
"""


import pygame
import copy
import random


class MovableNode(object):
    def __init__(self):
        self.location = [[],[]]  # first list stores the location of pixel, next stores the location of map
        self.volecity = []

    def __repr__(self):
        return str(self.location)

    def move(self):
        pass