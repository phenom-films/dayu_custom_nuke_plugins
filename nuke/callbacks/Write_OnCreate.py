#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import nuke


def callback():
    node = nuke.thisNode()
    tab_knob = nuke.Tab_Knob('dayu', 'Dayu')
    node.addKnob(tab_knob)
    _add_auto_name_knobs(node)


def _add_auto_name_knobs(node):
    auto_ext_konb = nuke.CascadingEnumeration_Knob('dayu_write_ext_list', 'format', ['.exr',
                                                                                     '.dpx',
                                                                                     '.tif',
                                                                                     '.png',
                                                                                     '.jpg',
                                                                                     '.mov'])
    auto_ext_konb.setFlag(0x1000)
    node.addKnob(auto_ext_konb)
    user_sub_level_knob = nuke.EvalString_Knob('dayu_write_user_sub_level', 'Sub Level')
    user_sub_level_knob.setFlag(0x1000)
    node.addKnob(user_sub_level_knob)
    button_knob = nuke.PyScript_Knob('dayu_write_auto_name', 'Auto Rename')
    button_knob.setFlag(0x1000)
    node.addKnob(button_knob)
