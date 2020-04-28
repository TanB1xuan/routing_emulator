# -*- coding: utf-8 -*-
"""
:Project: routing_emulator
:File: test_emulator.py

:Author: Tanbixuan
:Created: 2020-04-15
"""


# import pygame
# import pymunk


# import pytest
import sys
import pygame
import pymunk
from pymunk import pygame_util
from .test_config import TestConfig
from .font import Font


def pygame_disp():
    pygame.init()

    test_config = TestConfig()
    map_size = test_config.map_size
    size = width, height = map_size, map_size
    sea_map = test_config.sea_map
    floating_node_list = test_config.floating_node_list
    begin_font = Font('Initializing', (0x77, 0x88, 0xCC), 150)

    black = 0, 0, 0
    FPS = 15
    counter = 0
    ticket_to_update_water = 0
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(size)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(black)

        counter += 1
        if counter < 20 and counter > 0:
            screen.blit(begin_font.surface, [0, 0])

        elif counter < 40 and counter > 12:
            screen.fill([0xFF, 0xFF, 0xFF])
            screen.blit(sea_map.image, [0, 0])
            screen.blit(begin_font.surface, [0, 0])

        # Below: true rouiting
        elif counter > 41:
            ticket_to_update_water += 1
            if ticket_to_update_water >= FPS * 1:
                ticket_to_update_water = 0
                sea_map.rand_update()
                sea_map.draw_image()
            screen.blit(sea_map.image, [0, 0])
            screen.blit(test_config.convex_hull_obj.hull_image, [0, 0])
            for floating_node in floating_node_list:
                floating_node.update_node()
                screen.blit(floating_node.image, floating_node.location[0])

            """ movable node control"""
            test_config.movable_node.update_status()
            test_config.movable_node.update_image()
            screen.blit(test_config.movable_node.image, test_config.movable_node.location[0])

            test_config.floating_node_space.step(0.1)
            test_config.floating_node_space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(FPS)

def test_pygame_disp():
    pygame_disp()
