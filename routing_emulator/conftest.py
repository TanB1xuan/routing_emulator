# -*- coding: utf-8 -*-
"""
:Project: routing_emulator
:File: conftest.py

:Author: Tanbixuan
:Created: 2020-05-06
"""


import pytest
import tkinter
import pygame
import time
from .test_config import TestConfig

config_dict = [{}]

def pytest_runtest_setup(item):
    setup_window = tkinter.Tk()
    setup_window.title("SETUP")

    """ set floating number """
    floating_node_num_frame = tkinter.Frame(setup_window)

    floating_node_num_label = tkinter.Label(floating_node_num_frame, text="Floating Node Number", justify=tkinter.LEFT)
    floating_node_num_label.pack(side=tkinter.LEFT)
    default_num = tkinter.StringVar()
    floating_node_num_entry = tkinter.Entry(floating_node_num_frame, textvariable=default_num)
    floating_node_num_entry.pack(side=tkinter.RIGHT)
    default_num.set("15")

    """ set communication scope """
    communication_scope_frame = tkinter.Frame(setup_window)

    communication_scope_label = tkinter.Label(communication_scope_frame, 
                                              text="Communication Scope(30~50)", 
                                              justify=tkinter.LEFT)
    communication_scope_label.pack(side=tkinter.LEFT)
    default_communication_scope = tkinter.StringVar()
    communication_scope_entry = tkinter.Entry(communication_scope_frame, textvariable=default_communication_scope)
    communication_scope_entry.pack(side=tkinter.RIGHT)
    default_communication_scope.set("50")

    """ set update vertices check """
    vertices_check_frame = tkinter.Frame(setup_window)

    vertices_check_label = tkinter.Label(vertices_check_frame, text="Enable Vertices Update", justify=tkinter.LEFT)
    vertices_check_label.pack(side=tkinter.LEFT)
    vertices_value = tkinter.IntVar()
    vertices_check_check_button = tkinter.Checkbutton(vertices_check_frame,
                                                      variable=vertices_value,
                                                      onvalue=1,
                                                      offvalue=0)
    vertices_check_check_button.pack(side=tkinter.RIGHT)

    """ set OK button """
    def OK_command():
        nonlocal setup_window, floating_node_num_entry, communication_scope_entry, vertices_value
        floating_node_num = int(floating_node_num_entry.get())
        config_dict[0]["floating_node_num"] = floating_node_num
        communication_scope = int(communication_scope_entry.get())
        config_dict[0]["communication_scope"] = communication_scope
        config_dict[0]["vertices_value"] = vertices_value.get()
        setup_window.destroy()

    OK_frame = tkinter.Frame(setup_window)
    OK_button = tkinter.Button(OK_frame, text="OK", command=OK_command)
    OK_button.pack()

    floating_node_num_frame.pack()
    communication_scope_frame.pack()
    vertices_check_frame.pack()
    OK_frame.pack()
    setup_window.mainloop()


@pytest.fixture(name='test_config', scope='session', params=config_dict)
def get_test_config(request):
    time.sleep(0.1)  # for waiting for destroy of setup_window
    pygame.init()
    test_config = TestConfig(request.param)
    yield test_config


def pytest_runtest_teardown(item):
    test_config = item.funcargs['test_config']
    print(test_config.velocity_log)


def pytest_runtest_call(item):
    print(item)