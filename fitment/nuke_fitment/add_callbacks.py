#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import importlib
import os
from collections import defaultdict

import nuke

NUKE_FITMENT_ROOT_PATH = os.path.sep.join([os.environ.get('MY_CUSTOM_FITMENT', ''), 'nuke'])


def add_callbacks():
    callback_folder = os.path.sep.join([NUKE_FITMENT_ROOT_PATH, 'callbacks'])
    if not os.path.isdir(callback_folder):
        return

    nuke.pluginAppendPath(callback_folder)
    all_callback_files = [f.split('.')[0] for f in os.listdir(callback_folder) if f.endswith('.py')]
    callback_auto_load_structure = _go_through_and_find_callback_files(all_callback_files)
    for node_class, events in callback_auto_load_structure.items():
        for e in events:
            _register_callback_on_node(e, node_class)


def _register_callback_on_node(e, node_class):
    try:
        module = importlib.import_module('_'.join([node_class, e]))
        callback_func = getattr(module, 'callback', None)
        nuke_register_callback_func = getattr(nuke, 'add{}'.format(e), None)
        if callback_func and nuke_register_callback_func:
            nuke_register_callback_func(callback_func, nodeClass=node_class if node_class != 'All' else '*')
    except Exception as e:
        print e
        pass


def _go_through_and_find_callback_files(all_callback_files):
    callback_auto_load_structure = defaultdict(set)
    for f in all_callback_files:
        node_class, event = f.split('_')[:2]
        callback_auto_load_structure[node_class].add(event)
    return callback_auto_load_structure
