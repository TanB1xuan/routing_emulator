# -*- coding: utf-8 -*-
"""
:Project: routing_emulator
:File: trace_point.py

:Author: Tanbixuan
:Created: 2020-04-30
"""


import pygame


class TracePoint(object):
    def __init__(self, v):
        self.color = [0xFE - 8 * v, 0x0A + 8 * v, 0x20]
        self.fill_color = [0xE8, 0xFF, 0xFF]
        self.size = 10
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.fill_color)
        pygame.draw.circle(self.image, self.color, [5, 5], 5, )  # inner

        self.image.set_colorkey(self.fill_color)
