# -*- coding: utf-8 -*-
"""
:Project: routing_emulator
:File: movable_node.py

:Author: Tanbixuan
:Created: 2020-04-24
"""

from scipy.spatial import ConvexHull
import pygame


class RoutingAlgorithm(object):
    def __init__(self, test_config,):
        self.test_config = test_config


    def get_convex_hulls(self):
        floating_node_list = self.test_config.floating_node_list
        self.node_list = [x.location[0] for x in floating_node_list]
        for node in self.node_list:
            node[0] += 51
            node[1] += 51
        self.hull = ConvexHull(self.node_list)
        self.fill_color = [0xE8, 0xFF, 0xFF]
        self.map_size = self.test_config.map_size
        self.hull_image = pygame.Surface([self.map_size, self.map_size])
        self.hull_image.fill(self.fill_color)
        self.hull_image.set_colorkey(self.fill_color)
        self.line_color = [0x88, 0x11, 0x66]
        point_list = [self.node_list[x] for x in self.hull.vertices]
        pygame.draw.lines(self.hull_image, self.line_color, True, point_list, 3)