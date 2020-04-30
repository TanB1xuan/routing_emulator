# -*- coding: utf-8 -*-
"""
:Project: routing_emulator
:File: movable_node.py

:Author: Tanbixuan
:Created: 2020-04-20
"""


import pygame
import copy
import pymunk
import copy
from math import sqrt, acos, degrees, radians, cos, sin
from .font import Font, BolderFont
from .water_current import SeaMap
# import random


class BaseMovableNode(object):
    def __init__(self, test_config, ori_location):
        from .test_config import TestConfig
        self.location = [[], []]  # first list stores the location of pixel, next stores the location of map
        self.self_acceleration = [0, 0]
        self.velocity = [0, 0]
        self.target_position = []
        self.test_config: TestConfig = test_config
        self.location[0] = copy.deepcopy(ori_location)
        self.location[0][0] -= 15
        self.location[0][1] -= 15
        self.location[1].append(int(self.location[0][0] / 20))
        self.location[1].append(int(self.location[0][1] / 20))
        self.visited_node = []
        self.connected_ticket = 0
        self.battery = 100
        self.max_velocity = 18
        self.max_acc = 6
        self.rotation_angle = 0
        self.ticket_to_update_acc = 0
        ''' initialize all target node from convex hull '''
        self.ori_target_list = list(test_config.convex_hull_obj.hull.vertices)
        self.ori_target_list.remove(self.ori_target_list[0])

        self.status = "Planning"
        self.status_list = [
            'Connecting',
            'Planning',
            'Moving',
            'Missing'
        ]

        '''initialize the pymunk node'''
        mass = 10
        radius = 20
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = (self.location[0][0], self.location[0][1])
        self.node_body = pymunk.Circle(body, radius, (0, 0))
        self.node_body.elasticity = 0.8
        self.node_body.friction = 0

        self.sea_map: SeaMap = self.test_config.sea_map
        self.node_body.body.movable_node = self

    def update_image(self):
        """ update rotation angle according to """
        self.fill_color = [0xE8, 0xFF, 0xFF]
        self.image = pygame.Surface([300, 100])
        self.image.fill(self.fill_color)
        point_list = [
            [0, 5],
            [0, 25],
            [20, 25],
            [30, 15],
            [20, 5],
            [0, 5]
        ]

        """ draw inner image, it contains rotated image velocity """
        self.inner_surface = pygame.Surface([30,30])

        self.inner_surface.fill(self.fill_color)
        # self.inner_surface.fill([0, 0, 0])  # use this for debug

        pygame.draw.polygon(self.inner_surface, (0x30, 0xEF, 0xA6), point_list)
        pygame.draw.polygon(self.inner_surface, (0x55, 0xAA, 0xAA), point_list, 3)
        self.inner_surface = pygame.transform.rotate(self.inner_surface, self.rotation_angle)

        self.image.blit(self.inner_surface, [0, 0])
        self.image.set_colorkey(self.fill_color)
        self.update_font()
        self.image.blit(self.location_font.surface, [60, 0])
        self.image.blit(self.status_font.surface, [60, 25])
        self.image.blit(self.target_font.surface, [60, 50])

    def __repr__(self):
        return str(self.location)

    def update_font(self):
        """ font for location, status and target """
        """ font for location """
        location_font_text = f"X:{self.location[0][0]}; Y:{self.location[0][1]}"
        self.location_font = BolderFont(location_font_text, (0x00, 0x00, 0x00), 20)

        """ font for status """
        if self.status == 'Connecting':
            self.status_font = BolderFont("Connecting", (0xFF, 0x00, 0xFF), 20)
        if self.status == 'Planning':
            self.status_font = BolderFont("Planning", (0x33, 0xCC, 0x55), 20)
        if self.status == 'Moving':
            self.status_font = BolderFont("Moving", (0xAA, 0x88, 0x00), 20)

        """font for target"""
        target_font_text = f"Target:[{self.target_position[0]}, {self.target_position[1]}]"
        self.target_font = BolderFont(target_font_text, (0x00, 0x00, 0x00), 20)

    def update_status(self):
        """ update target, location and status"""
        """ update status """
        self.status = 'Moving'
        for floating_node in self.test_config.floating_node_list:
            if floating_node.id not in self.visited_node:
                f_x = floating_node.location[0][0] + 51
                f_y = floating_node.location[0][1] + 51
                cur_location_x = self.location[0][0] + 15
                cur_location_y = self.location[0][1] + 15
                if (sqrt((cur_location_x - f_x) ** 2 + (cur_location_y - f_y) ** 2) <=
                        floating_node.communication_distance):
                    self.connected_ticket += 1
                    if self.connected_ticket >= 15:
                        self.visited_node.append(floating_node.id)
                        if floating_node.id in self.ori_target_list:
                            self.ori_target_list.remove(self.ori_target_list[0])
                        self.connected_ticket = 0
                        self.status = 'Moving'
                    else:
                        self.status = 'Connecting'

        """ update target """
        cur_target_num = self.ori_target_list[0]
        self.target_position = copy.deepcopy(self.test_config.floating_node_list[cur_target_num].location[0])
        self.target_position[0] += 51
        self.target_position[1] += 51

        """ update location """
        x = self.node_body.body.position.int_tuple[0]
        y = self.node_body.body.position.int_tuple[1]
        self.location[0][0] = x
        self.location[0][1] = y
        self.location[1][0] = int(self.location[0][0] / 20)
        self.location[1][1] = int(self.location[0][1] / 20)

        self.ticket_to_update_acc += 1
        if self.ticket_to_update_acc >= 15*1:
            self.ticket_to_update_acc = 0
            self.update_acceleration()

    def update_acceleration(self):
        tar_x = self.target_position[0]
        tar_y = self.target_position[1]
        x_edge = tar_x - self.location[0][0]
        y_edge = tar_y - self.location[0][1]
        third_edge = sqrt(x_edge ** 2 + y_edge ** 2)
        angle_r = acos(x_edge / third_edge)
        angle_d = degrees(angle_r)
        if y_edge > 0:
            angle_d = 360 - angle_d
        self.rotation_angle = angle_d
        angle_r = radians(angle_d)
        self.self_acceleration = [self.max_acc * cos(angle_r), - self.max_acc * sin(angle_r)]

    def update_callback(self):

        def update_velocity(body, gravity, damping, dt):
            sea_map = body.movable_node.sea_map
            x, y = body.movable_node.location[1]
            x_velocity = body.movable_node.velocity[0] * 3 / 4
            y_velocity = body.movable_node.velocity[1] * 3 / 4
            x_force = sea_map.water_cur_force[x][y][0][0]
            y_force = sea_map.water_cur_force[x][y][0][1]

            if body.movable_node.status == "Connecting":
                x_velocity = x_velocity + x_force / 2
                y_velocity = y_velocity + y_force / 2

                body.movable_node.velocity = [x_velocity, y_velocity]
                body.velocity = (x_velocity, y_velocity)
            else:
                x_acc = body.movable_node.self_acceleration[0]
                y_acc = body.movable_node.self_acceleration[1]

                x_velocity = x_velocity + x_acc
                y_velocity = y_velocity + y_acc
                cur_velocity = sqrt(x_velocity ** 2 + y_velocity ** 2)
                if cur_velocity > body.movable_node.max_velocity:
                    x_velocity = x_velocity * (self.max_acc / cur_velocity)
                    y_velocity = y_velocity * (self.max_acc / cur_velocity)
                x_velocity = x_velocity + x_force
                y_velocity = y_velocity + y_force

                body.movable_node.velocity = [x_velocity, y_velocity]
                body.velocity = (x_velocity, y_velocity)

        self.node_body.body.velocity_func = update_velocity

class ConvexHullMovableNode(BaseMovableNode):
    def update_status(self):
        super(ConvexHullMovableNode, self).update_status()

    def update_acceleration(self):
        super(ConvexHullMovableNode, self).update_acceleration()
