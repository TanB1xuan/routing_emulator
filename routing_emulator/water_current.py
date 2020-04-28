# -*- coding: utf-8 -*-
"""
:Project: routing_emulator
:File: water_current.py

:Author: Tanbixuan
:Created: 2020-04-21
"""


import pygame
import copy
import random
from math import sqrt, degrees, radians, acos, cos, sin, exp, pi


class Arrow(object):
    def __init__(self, fill_color: list, arrow_length: int):
        assert arrow_length >= 0, "arrow length must not be a negative"
        self.size = [16, 16]
        self.image = pygame.Surface(self.size)
        self.image.fill(fill_color)
        point_list = [
            [4, 12],
            [6, 12],
            [3, 15],
            [0, 12],
            [2, 12],
            # below data can define the length of arrow
            [2, 11 - arrow_length],
            [4, 11 - arrow_length],
        ]
        pygame.draw.polygon(self.image, (0x00 + 12 * arrow_length, 0xDD - 18 * arrow_length, 0xFF), point_list)

    def rotate_image(self, angle: int):
        self.image = pygame.transform.rotate(self.image, angle)


class Wave(object):
    def __init__(self, fill_color: list, ):
        self.size = [10, 10]
        self.image = pygame.Surface(self.size)
        self.image.fill(fill_color)
        point_list = [
            [2, 0],
            [3, 2],
            [2, 4],
            [4, 6],
            [3, 4],
            [4, 1],
        ]
        pygame.draw.polygon(self.image, (0x00, 0xCC, 0xCC), point_list)

    def rotate_image(self, angle: int):
        self.image = pygame.transform.rotate(self.image, angle)


class LambVorticeMap(object):
    def __init__(self, water_array: list, **kwargs):

        def get_new_location(x, y):
            change_zoom = 1
            rand_change_flag = random.randrange(0,2)
            if x <= map_size / 2 and y <= map_size / 2:
                if rand_change_flag:
                    x -= change_zoom
                    y += change_zoom
                    if x < 5:
                        x = 5
                else:
                    x += change_zoom
                    y -= change_zoom
                    if y < 5:
                        y = 5
            elif x <= map_size / 2 and y >= map_size / 2:
                if rand_change_flag:
                    x += change_zoom
                    y += change_zoom
                    if y > map_size - 5:
                        y = map_size
                else:
                    x -= change_zoom
                    y -= change_zoom
                    if x < 5:
                        x = 5
            elif x >= map_size / 2 and y >= map_size / 2:
                if rand_change_flag:
                    x += change_zoom
                    y -= change_zoom
                    if x > map_size - 5:
                        x = map_size
                else:
                    x -= change_zoom
                    y += change_zoom
                    if y > map_size - 5:
                        y = map_size
            elif x >= map_size / 2 and y <= map_size / 2:
                if rand_change_flag:
                    x -= change_zoom
                    y -= change_zoom
                    if y < 5:
                        y = 5
                else:
                    x += change_zoom
                    y += change_zoom
                    if x > map_size - 5:
                        x = map_size
            return x, y

        self.gaussian_distr_force = copy.deepcopy(water_array)
        self.gaussian_value = copy.deepcopy(water_array)
        map_size = len(water_array)
        zoom_value = 5
        self.location: dict = {}
        self.args_dict: dict = {}
        if kwargs:
            x = kwargs['x']
            y = kwargs['y']
            x, y = get_new_location(x, y)
            self.location['x'] = x
            self.location['y'] = y
            self.args_dict['mu_1'] = kwargs['mu_1']
            self.args_dict['mu_2'] = kwargs['mu_2']
            self.args_dict['sigma_1'] = kwargs['sigma_1']
            self.args_dict['sigma_2'] = kwargs['sigma_2']
            self.args_dict['rho'] = kwargs['rho']
        else:
            self.location['x'] = random.randrange(5, map_size - 5)
            self.location['y'] = random.randrange(5, map_size - 5)
            self.args_dict['mu_1'] = self.location['x'] / zoom_value
            self.args_dict['mu_2'] = self.location['y'] / zoom_value
            self.args_dict['sigma_1'] = 0.25 + 1.25 * random.random()
            self.args_dict['sigma_2'] = self.args_dict['sigma_1'] + 0.5 * random.random()
            self.args_dict['rho'] = 0
        for x in range(len(self.gaussian_value)):
            for y in range(len(self.gaussian_value[x])):
                self.gaussian_value[x][y] = self.get_gaussian_value(x / zoom_value, y / zoom_value, self.args_dict)

        max_value = 0
        for raw in self.gaussian_value:
            cur_max = max(raw)
            if cur_max > max_value:
                max_value = cur_max
        half_max_value = max_value / 2
        for x in range(len(self.gaussian_value)):
            for y in range(len(self.gaussian_value[x])):
                if self.gaussian_value[x][y] > half_max_value:
                    self.gaussian_value[x][y] = max_value - self.gaussian_value[x][y]
        self.generate_current()
                
    def get_gaussian_value(self, x: float, y: float, args_dict: dict):
        mu_1 = args_dict['mu_1']
        mu_2 = args_dict['mu_2']
        sigma_1 = args_dict['sigma_1']
        sigma_2 = args_dict['sigma_2']
        rho = args_dict['rho']

        gaussian_value = exp(-(1 / (2 * (1 - rho ** 2))) * (\
                             ((x - mu_1) ** 2) / sigma_1 ** 2 -\
                             2 * rho * (x - mu_1) * (y * mu_2) / (sigma_1 * sigma_2) +\
                             (y - mu_2) ** 2 / sigma_2 ** 2
                            ))/\
                         (2 * pi * sigma_1 * sigma_2 * sqrt(1 - rho ** 2))
        return gaussian_value

    def generate_current(self):
        max_value = 0
        max_force = 3
        """get max_value as using for normalization"""
        for raw in self.gaussian_value:
            cur_max = max(raw)
            if cur_max > max_value:
                max_value = cur_max

        for x in range(len(self.gaussian_value)):
            for y in range(len(self.gaussian_value[x])):
                cur_force = 3 * self.gaussian_value[x][y] / max_value
                x_edge = self.location['x'] - x
                y_edge = self.location['y'] - y
                third_edge = sqrt(x_edge ** 2 + y_edge ** 2)
                try:
                    angle_r = acos(x_edge / third_edge)
                except ZeroDivisionError:
                    self.gaussian_distr_force[x][y] = [0, 0]
                    continue
                if y < self.location['y']:
                    angle_r = 3/2 * pi - angle_r
                else:
                    angle_r = 3/2 * pi + angle_r
                self.gaussian_distr_force[x][y] = [cur_force * cos(angle_r), -(cur_force * sin(angle_r))]

    def __repr__(self):
        ret_str = 'location' + str(self.location) + ';'
        ret_str = ret_str + 'args_dict' + str(self.args_dict)
        return ret_str

class SeaMap(object):
    def __init__(self, map_size: int, ):
        """initialize the water current, witch is also background force of water"""
        
        '''set an arrow per 20px'''
        water_array_size = int(map_size / 20)
        self.water_cur_direction = list(range(water_array_size))
        for i in range(water_array_size):
            self.water_cur_direction[i] = list(range(water_array_size))
        
        '''initial the water current's image'''
        self.map_size = map_size
        self.image = pygame.Surface([map_size, map_size])
        self.image_size = [map_size, map_size]
        self.fill_color = [0xE8, 0xFF, 0xFF]
        self.image.fill(self.fill_color)

        center_value = int(len(self.water_cur_direction)/2)
        
        '''initial the water current's force'''
        self.water_cur_force = copy.deepcopy(self.water_cur_direction)
        for x in range(len(self.water_cur_force)):
            for y in range(len(self.water_cur_force)):
                self.water_cur_force[x][y] = [[], []]
                cur_size = 0

                x_edge = center_value - x
                y_edge = center_value - y
                third_edge = sqrt(x_edge ** 2 + y_edge ** 2)
                try:
                    angle_r = acos(x_edge/third_edge)
                except ZeroDivisionError:
                    angle_d = 90
                    cur_length = 0
                    self.water_cur_force[x][y][0].append(0)
                    self.water_cur_force[x][y][0].append(0)
                    self.water_cur_force[x][y][1].append(cur_length)
                    self.water_cur_force[x][y][1].append(angle_d)
                    continue
                angle_d = degrees(angle_r)

                if y < center_value:
                    angle_d = 360 - angle_d
                cur_length = cur_size
                self.water_cur_force[x][y][1].append(cur_length)
                self.water_cur_force[x][y][1].append(angle_d)

                self.water_cur_force[x][y][0].append(cur_size * cos(radians(angle_d - 90)))
                # water background force on x axis
                self.water_cur_force[x][y][0].append(cur_size * sin(radians(angle_d + 90)))
                # water background force on y axis
        self.lamb_vortice_list = []
        self.lamb_vortice_info = []
        self.num_lamb_v = random.randrange(3, 5)
        for _ in range(self.num_lamb_v):
            cur_lamb_v = LambVorticeMap(self.water_cur_direction)
            self.lamb_vortice_list.append(cur_lamb_v)
            cur_info = copy.deepcopy(cur_lamb_v.args_dict)
            cur_info['x'] = cur_lamb_v.location['x']
            cur_info['y'] = cur_lamb_v.location['y']
            self.lamb_vortice_info.append(cur_info)

        '''add the lamb vortices' force to water current'''
        for i in range(self.num_lamb_v):
            cur_lamb_v = self.lamb_vortice_list[i]
            for x in range(len(self.water_cur_force)):
                for y in range(len(self.water_cur_force)):
                    self.water_cur_force[x][y][0][0] = self.water_cur_force[x][y][0][0] + \
                                                       cur_lamb_v.gaussian_distr_force[x][y][0]
                    self.water_cur_force[x][y][0][1] = self.water_cur_force[x][y][0][1] + \
                                                       cur_lamb_v.gaussian_distr_force[x][y][1]
        self.update_water_cur()

    def draw_image(self,):
        self.image = pygame.Surface([self.map_size, self.map_size])
        self.image_size = [self.map_size, self.map_size]
        self.fill_color = [0xE8, 0xFF, 0xFF]
        self.image.fill(self.fill_color)
        self.arrow_image_array = copy.deepcopy(self.water_cur_direction)
        for x in range(len(self.arrow_image_array)):
            for y in range(len(self.arrow_image_array[x])):
                cur_length = self.water_cur_force[x][y][1][0]
                cur_angle = self.water_cur_force[x][y][1][1]
                if cur_length != 0:
                    cur_arrow = Arrow(self.fill_color, cur_length)
                    cur_arrow.rotate_image(cur_angle)
                    self.image.blit(cur_arrow.image, [x * 20, y * 20])
                else:
                    cur_wave = Wave(self.fill_color)
                    cur_wave.rotate_image(cur_angle)
                    self.image.blit(cur_wave.image, [x * 20, y * 20])

    def update_water_cur(self):
        max_force = 0
        max_length = 11
        for x in range(len(self.water_cur_force)):
            for y in range(len(self.water_cur_force)):
                cur_force = sqrt(self.water_cur_force[x][y][0][0] ** 2 + self.water_cur_force[x][y][0][1] ** 2)
                if cur_force > max_force:
                    max_force = cur_force

        '''update length and angle'''
        for x in range(len(self.water_cur_force)):
            for y in range(len(self.water_cur_force)):
                x_force = self.water_cur_force[x][y][0][0]
                y_force = self.water_cur_force[x][y][0][1]
                cur_force = sqrt(x_force ** 2 + y_force ** 2)
                self.water_cur_force[x][y][1][0] = max_length * cur_force / max_force
                try:
                    angle_r = acos(x_force / cur_force)
                except ZeroDivisionError:
                    angle_r = 0
                angle_d = degrees(angle_r)
                if y_force < 0:
                    if x_force < 0:
                        self.water_cur_force[x][y][1][1] = 90 + angle_d
                    else:
                        self.water_cur_force[x][y][1][1] = 90 + angle_d
                else:
                    if x_force > 0:
                        self.water_cur_force[x][y][1][1] = 90 - angle_d
                    else:
                        self.water_cur_force[x][y][1][1] = 450 - angle_d

    def rand_update(self):
        new_lamb_vortice_list = []
        new_lamb_vortice_info = []
        for i in range(len(self.lamb_vortice_list)):
            cur_info = self.lamb_vortice_info[i]
            cur_lamb_v = LambVorticeMap(self.water_cur_direction, **cur_info)
            new_lamb_vortice_list.append(cur_lamb_v)
            new_cur_info = copy.deepcopy(cur_lamb_v.args_dict)
            new_cur_info['x'] = cur_lamb_v.location['x']
            new_cur_info['y'] = cur_lamb_v.location['y']
            new_lamb_vortice_info.append(new_cur_info)
        self.lamb_vortice_list = new_lamb_vortice_list
        self.lamb_vortice_info = new_lamb_vortice_info
        for i in range(self.num_lamb_v):
            cur_lamb_v = self.lamb_vortice_list[i]
            for x in range(len(self.water_cur_force)):
                for y in range(len(self.water_cur_force)):
                    self.water_cur_force[x][y][0][0] = self.water_cur_force[x][y][0][0] * 2/3 + \
                                                       cur_lamb_v.gaussian_distr_force[x][y][0]
                    self.water_cur_force[x][y][0][1] = self.water_cur_force[x][y][0][1] * 2/3 + \
                                                       cur_lamb_v.gaussian_distr_force[x][y][1]
        self.update_water_cur()
