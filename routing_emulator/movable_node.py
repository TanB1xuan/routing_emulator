# -*- coding: utf-8 -*-
"""
:Project: routing_emulator
:File: movable_node.py

:Author: Tanbixuan
:Created: 2020-04-20
"""


import pygame
import copy
from .font import Font, BolderFont
# import random


class BaseMovableNode(object):
    def __init__(self, test_config, ori_location):
        self.location = [[], []]  # first list stores the location of pixel, next stores the location of map
        self.acceleration = []
        self.volecity = []
        self.target_position = []
        self.test_config = test_config
        self.location[0] = copy.deepcopy(ori_location)
        self.location[0][0] -= 30
        self.location[0][1] -= 30
        self.location[1].append(int(self.location[0][0] / 20))
        self.location[1].append(int(self.location[0][1] / 20))
        self.battery = 100

        self.status: str
        self.status_list = [
            'Connecting',
            'Planning',
            'Moving',
            'Missing'
        ]

    def update_image(self):
        self.fill_color = [0xE8, 0xFF, 0xFF]
        self.image = self.image = pygame.Surface([300, 100])
        self.image.fill(self.fill_color)
        point_list = [
            [0, 15],
            [0, 45],
            [35, 45],
            [50, 30],
            [35, 15],
            [0, 15]
        ]
        pygame.draw.polygon(self.image, (0x30, 0xEF, 0xA6), point_list)
        pygame.draw.polygon(self.image, (0x55, 0xAA, 0xAA), point_list, 3)
        self.image.set_colorkey(self.fill_color)
        self.update_font()
        self.image.blit(self.location_font.surface, [50, 0])
        self.image.blit(self.status_font.surface, [50, 25])

    def __repr__(self):
        return str(self.location)

    def update_font(self):
        location_font_text = f"X:{self.location[0][0]}; Y:{self.location[0][1]}"
        self.location_font = BolderFont(location_font_text, (0x00, 0x00, 0x00), 20)
        if self.status == 'Connecting':
            self.status_font = BolderFont("Connecting", (0xFF, 0x00, 0xFF), 20)

    def update_status(self):
        """ update target and status"""
        self.status = 'Connecting'

    def update_acceleration(self):
        pass


class ConvexHullMovableNode(BaseMovableNode):
    def update_status(self):
        self.status = 'Connecting'

    def update_acceleration(self):
        sea_map = self.test_config.sea_map
