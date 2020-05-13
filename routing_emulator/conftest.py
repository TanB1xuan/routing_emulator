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
import os.path as osp
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from .test_config import TestConfig

config_dict = [{}]
test_config_list = []
all_test_nodes = [
    'MultilayeredPathPlanningNode',
    'ConvexHullMovableNode'
]
runned_test_case = []


def first_collection(item):
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


def pytest_runtest_setup(item):
# def setup_module():
    if len(runned_test_case) == 0:
        runned_test_case.append(item.name)
        first_collection(item)
        time.sleep(0.1)  # for waiting for destroy of setup_window
        pygame.init()
        test_config = TestConfig(config_dict[0])
        temp_test_config = copy_test_config(test_config)
        test_config_list.append(temp_test_config)
        config_dict[0]['test_case'] = 0
    else:
        time.sleep(0.1)  # for waiting for destroy of setup_window
        pygame.init()
        runned_test_case.append(item.name)
        # test_flag = cur_name.find(']')
        # test_num = int(cur_name[test_flag - 1])

        # config_dict[test_num]['test_case'] = test_num
        # test_config_list[test_num] = test_config_list[0]

@pytest.fixture(name='test_config', scope='session', params=all_test_nodes)
def get_test_config(request):
    temp_test_config = test_config_list[0]
    print(request.param)
    test_config = copy_test_config(temp_test_config)
    test_config.add_movable_node(request.param)

    yield test_config


# @pytest.fixture(name='test_movable_node', scope='session', params=all_test_nodes)
# def get_test_node(request):
#
#     yield request.param


def pytest_runtest_teardown(item):
    test_config = item.funcargs['test_config']
    y = test_config.velocity_log
    x = range(len(y))
    plt.title("Time-Velocity Curve")
    plt.plot(x, y)
    plt.xlabel("Time")
    plt.ylabel("Velocity")
    plt.savefig('images/' + item.name + time.strftime("-%Y-%m-%d[%H:%M:%S]", time.localtime()))
    # plt.show()


def pytest_runtest_call(item):
    print(item)


def copy_test_config(test_config: TestConfig):
    temp_obj = TestConfig(config_dict[0])
    temp_obj.copy_info(test_config)

    return temp_obj
