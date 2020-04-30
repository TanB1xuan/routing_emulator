# -*- coding: utf-8 -*-
"""
:Project: routing_emulator
:File: floating_node.py

:Author: Tanbixuan
:Created: 2020-04-20
"""


import pygame
import pymunk
import random
from .font import Font
from pymunk import pygame_util
from .water_current import SeaMap


class FloatingNode(object):
    def __init__(self, fill_color: list, map_size: int, rand_value: list, space, sea_map):
        self.fill_color = fill_color
        self.location = [[],[]]  # first list stores the location of pixel, next stores the location of map
        self.location[0].append(rand_value[0])  # position on x axis
        self.location[0].append(rand_value[1])  # position on y axis
        self.location[1].append(int(self.location[0][0] / 20))
        self.location[1].append(int(self.location[0][1] / 20))
        self.velocity = []
        self.original_location = self.location[0]
        self.worth_value = random.randrange(1, 4)
        self.communication_distance = 50
        self.size = [105, 105]
        self.fill_color = fill_color
        self.image = pygame.Surface(self.size)
        self.image.fill(fill_color)
        self.radius = 5 + 4 * self.worth_value
        inner_color = [0xD3, 0xEE, 0x66]
        edge_color = [0xFF, 0x77, 0x55]
        communication_color = [0x7C, 0xAE, 0xF8]
        font_text = f"X:{self.location[0][0]}; Y:{self.location[0][1]}"
        floating_node_font = Font(font_text, (0x00, 0x00, 0x00), 20)
        pygame.draw.circle(self.image, inner_color, [51, 51], self.radius, )  # inner
        pygame.draw.circle(self.image, edge_color, [51, 51], self.radius, 3)  # edge
        pygame.draw.circle(self.image, communication_color, [51, 51], self.communication_distance, 3)  # edge
        self.image.blit(floating_node_font.surface, [0, 0])  # font
        self.image.set_colorkey(fill_color)

        '''set the static_edge pymunk body '''
        static_body = space.static_body
        p_1 = (self.location[0][0] + 30,self.location[0][1] +  10)
        p_2 = (self.location[0][0] + 70, self.location[0][1] + 10)
        p_3 = (self.location[0][0] + 90, self.location[0][1] + 30)
        p_4 = (self.location[0][0] + 90, self.location[0][1] + 70)
        p_5 = (self.location[0][0] + 70, self.location[0][1] + 90)
        p_6 = (self.location[0][0] + 30, self.location[0][1] + 90)
        p_7 = (self.location[0][0] + 10, self.location[0][1] + 70)
        p_8 = (self.location[0][0] + 10, self.location[0][1] + 30)
        self.static_body = [
            pymunk.Segment(static_body, p_1, p_2, 0.0),
            pymunk.Segment(static_body, p_2, p_3, 0.0),
            pymunk.Segment(static_body, p_3, p_4, 0.0),
            pymunk.Segment(static_body, p_4, p_5, 0.0),
            pymunk.Segment(static_body, p_5, p_6, 0.0),
            pymunk.Segment(static_body, p_6, p_7, 0.0),
            pymunk.Segment(static_body, p_7, p_8, 0.0),
            pymunk.Segment(static_body, p_8, p_1, 0.0),
        ]

        '''initialize the pymunk node'''
        mass = 10
        radius = self.radius
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = (self.location[0][0] + 51,self.location[0][1] +  51)
        self.node_body = pymunk.Circle(body, radius, (0, 0))
        self.node_body.elasticity = 0.8
        self.node_body.friction = 0

        self.sea_map = sea_map
        self.node_body.body.floating_node = self

    def __repr__(self):
        return str(self.location)

    def update_node(self):
        x = self.node_body.body.position.int_tuple[0]
        y = self.node_body.body.position.int_tuple[1]
        self.location[0][0] = x - 51
        self.location[0][1] = y - 51
        self.location[1][0] = int(self.location[0][0] / 20)
        self.location[1][1] = int(self.location[0][1] / 20)
        self.image = pygame.Surface(self.size)
        self.image.fill(self.fill_color)
        self.radius = 5 + 4 * self.worth_value
        inner_color = [0xD3, 0xEE, 0x66]
        edge_color = [0xFF, 0x77, 0x55]
        communication_color = [0x7C, 0xAE, 0xF8]
        font_text = f"X:{self.location[0][0]}; Y:{self.location[0][1]}"
        floating_node_font = Font(font_text, (0x00, 0x00, 0x00), 20)
        pygame.draw.circle(self.image, inner_color, [51, 51], self.radius, )  # inner
        pygame.draw.circle(self.image, edge_color, [51, 51], self.radius, 3)  # edge
        pygame.draw.circle(self.image, communication_color, [51, 51], 50, 3)  # edge
        self.image.blit(floating_node_font.surface, [0, 0])  # font
        self.image.set_colorkey(self.fill_color)


    def update_callback(self):

        def update_gravity(body, gravity, damping, dt):
            x, y = body.floating_node.location[1]
            sea_map = body.floating_node.sea_map
            x_force = sea_map.water_cur_force[x][y][0][0]
            y_force = sea_map.water_cur_force[x][y][0][1]
            pymunk.Body.update_velocity(body, (x_force, y_force), damping, dt)

        self.node_body.body.velocity_func = update_gravity
