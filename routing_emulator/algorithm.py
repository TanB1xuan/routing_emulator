# -*- coding: utf-8 -*-
"""
:Project: routing_emulator
:File: algorithm.py

:Author: Tanbixuan
:Created: 2020-04-24
"""

from scipy.spatial import ConvexHull
from math import fabs, pow
import pygame

def get_dis(pointX, pointY, lineX1, lineY1, lineX2, lineY2):
    a = lineY2 - lineY1
    b = lineX1 - lineX2
    c = lineX2 * lineY1 - lineX1 * lineY2
    dis = (fabs(a * pointX + b * pointY + c)) / (pow(a * a + b * b, 0.5))
    return dis

def get_second_value(elem):
    return elem[1]


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
        self.ori_target_list = list(self.hull.vertices)
        i = 0
        for _ in range(len(self.ori_target_list) - 1):
            point1 = self.node_list[self.ori_target_list[i]]
            point2 = self.node_list[self.ori_target_list[i + 1]]
            line_x1 = point1[0]
            line_y1 = point1[1]
            line_x2 = point2[0]
            line_y2 = point2[1]
            append_list = []
            for floating_node in floating_node_list:
                if floating_node.id not in self.ori_target_list:
                    cur_id = floating_node.id
                    cur_dis = get_dis(self.node_list[cur_id][0],
                                  self.node_list[cur_id][1],
                                  line_x1,
                                  line_y1,
                                  line_x2,
                                  line_y2)
                    if cur_dis <= floating_node.worth_value * 15:
                        append_list.append([cur_id, cur_dis])
            append_list.sort(key=get_second_value)
            for item in append_list:
                self.ori_target_list = self.ori_target_list[:i + 1] + [item[0]] + self.ori_target_list[i + 1:]
                i += 1
            i += 1
        point_list = [self.node_list[x] for x in self.ori_target_list]
        pygame.draw.lines(self.hull_image, self.line_color, True, point_list, 3)