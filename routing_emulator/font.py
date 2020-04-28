# -*- coding: utf-8 -*-
"""
:Project: routing_emulator
:File: font.py

:Author: Tanbixuan
:Created: 2020-04-21
"""


import pygame

class Font(object):
    def __init__(self, text, color, font_size):
        self.font = pygame.font.Font('./font/corbell.ttf',font_size)
        antialias = False
        self.surface = self.font.render(text, antialias, color)

class BolderFont(object):
    def __init__(self, text, color, font_size):
        self.font = pygame.font.Font('./font/tahoma.ttf',font_size)
        antialias = False
        self.surface = self.font.render(text, antialias, color)