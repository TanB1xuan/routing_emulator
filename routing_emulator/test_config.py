# -*- coding: utf-8 -*-
"""
:Project: routing_emulator
:File: test_config.py

:Author: Tanbixuan
:Created: 2020-04-20
"""


import random
import pymunk
from pymunk import pygame_util
from .water_current import SeaMap
from .floating_node import FloatingNode
from .algorithm import RoutingAlgorithm
from .trace_point import TracePoint
from math import sqrt
from routing_emulator import movable_node


class TestConfig(object):
    def __init__(self, config_dict):

        pymunk.pygame_util.positive_y_is_up = False
        self.map_size = 1000
        self.recursive_speed = 0.1
        self.minimum_dis = 100
        self.sea_map = SeaMap(self.map_size)
        self.sea_map.draw_image()

        self.floating_node_space = pymunk.Space()
        self.floating_node_space.gravity = 0, 0
        self.floating_node_list = []
        self.floating_node_num = config_dict['floating_node_num']
        self.enable_update_vertices = config_dict['vertices_value']
        self.communication_scope = config_dict['communication_scope']

        '''set random value of floating nodes' valocation, witch satisfied to gaussian distribute. '''
        self.rand_value_matrix = []
        for i in range(self.floating_node_num):
            while True:
                rerand_flag = False
                x = random.randrange(self.map_size / 10, self.map_size * 9 / 10)
                y = random.randrange(self.map_size / 10, self.map_size * 9 / 10)
                for point in self.rand_value_matrix:
                    if sqrt( (x - point[0]) ** 2 + (y - point[1]) ** 2) < self.minimum_dis:
                        rerand_flag = True
                        break
                if not rerand_flag:
                    break
            self.rand_value_matrix.append([x, y])
        for i in range(self.floating_node_num):
            self.floating_node_list.append(
                FloatingNode([0xE8, 0xFF, 0xFF],
                             self.map_size, self.rand_value_matrix[i],
                             self.floating_node_space,
                             self.sea_map,
                             self.communication_scope)
            )
            self.floating_node_list[i].id = i
        for i in range(self.floating_node_num):
            self.floating_node_space.add(self.floating_node_list[i].static_body)
            self.floating_node_space.add(self.floating_node_list[i].node_body.body,
                                         self.floating_node_list[i].node_body)
            self.floating_node_list[i].update_callback()

        """ get and draw the hull """
        self.algorithm_obj = RoutingAlgorithm(self)
        self.algorithm_obj.get_convex_hulls()
        
        """ add movable node """
        ori_location_node_num = self.algorithm_obj.hull.vertices[0]
        movable_node_ori_location = self.algorithm_obj.node_list[ori_location_node_num]
        self.movable_node = movable_node.ConvexHullMovableNode(self, movable_node_ori_location)

        self.movable_node_space = pymunk.Space()
        self.movable_node_space.gravity = 0, 0
        self.movable_node_space.add(self.movable_node.node_body.body, self.movable_node.node_body)
        self.movable_node.update_callback()
        self.trace_point_surface_list = []
        for i in range(30):
            cur_trace_point = TracePoint(i)
            self.trace_point_surface_list.append(cur_trace_point)
        self.trace_point_list = []
        self.velocity_log = []

    def set_trace(self):
        x = self.movable_node.location[0][0] + 15
        y = self.movable_node.location[0][1] + 15
        self.trace_point_list.append([x, y])
        if len(self.trace_point_list) >= 2:
            new_point = self.trace_point_list[-1]
            old_point = self.trace_point_list[-2]
            dis = sqrt((new_point[0] - old_point[0]) ** 2 + (new_point[1] - old_point[1]) ** 2)
            self.velocity_log.append(dis)
        else:
            self.velocity_log.append(0)

    def copy_info(self, test_config):
        self.sea_map = test_config.sea_map
        self.rand_value_matrix = test_config.rand_value_matrix
        # self.floating_node_space = pymunk.Space()
        # self.floating_node_space.gravity = 0, 0
        self.floating_node_list = []
        for i in range(self.floating_node_num):
            self.floating_node_list.append(
                FloatingNode([0xE8, 0xFF, 0xFF],
                             self.map_size, self.rand_value_matrix[i],
                             self.floating_node_space,
                             self.sea_map,
                             self.communication_scope)
            )
            self.floating_node_list[i].id = i
        for i in range(self.floating_node_num):
            self.floating_node_space.add(self.floating_node_list[i].static_body)
            self.floating_node_space.add(self.floating_node_list[i].node_body.body,
                                         self.floating_node_list[i].node_body)
            self.floating_node_list[i].update_callback()

        """ get and draw the hull """
        self.algorithm_obj = RoutingAlgorithm(self)
        self.algorithm_obj.get_convex_hulls()

    def add_movable_node(self, test_node):
        """ add movable node """
        ori_location_node_num = self.algorithm_obj.hull.vertices[0]
        movable_node_ori_location = self.algorithm_obj.node_list[ori_location_node_num]

        """ add movable node according to arg info """
        if test_node == 'ConvexHullMovableNode':
            self.movable_node = movable_node.ConvexHullMovableNode(self, movable_node_ori_location)
        elif test_node == 'MultilayeredPathPlanningNode':
            self.movable_node = movable_node.MultilayeredPathPlanningNode(self, movable_node_ori_location)

        self.movable_node_space = pymunk.Space()
        self.movable_node_space.gravity = 0, 0
        self.movable_node_space.add(self.movable_node.node_body.body, self.movable_node.node_body)
        self.movable_node.update_callback()
        self.trace_point_list = []
        self.velocity_log = []
