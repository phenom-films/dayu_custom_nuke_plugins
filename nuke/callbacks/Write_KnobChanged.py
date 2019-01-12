#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import nuke


def callback():
    node = nuke.thisNode()
    knob = nuke.thisKnob()

    if knob.name() == 'dayu_write_auto_name':
        _auto_rename(node, knob)


def _auto_rename(node, knob):
    def get_current_nk_filename():
        nk_file = None
        try:
            nk_file = nuke.scriptName()
        except RuntimeError as e:
            nuke.alert(e.message)
        return nk_file

    ext_value = node['dayu_write_ext_list'].value()
    user_sub_level = node['dayu_write_user_sub_level'].value()

    current_nk_filename = get_current_nk_filename()
    if current_nk_filename:
        render_filename = _generate_filename(current_nk_filename, ext_value, user_sub_level)
        node['file'].setValue(render_filename)
        node['label'].setValue(user_sub_level)


def _generate_filename(current_nk_filename, ext_value, user_sub_level):
    import os
    basename = os.path.basename(current_nk_filename)
    components = basename.split('.')[0].split('_')
    render_root_path = os.environ.get('DAYU_NUKE_RENDER_PATH', '~')
    render_file_path = '{root}' \
                       '{sep}' \
                       '{sub_level}' \
                       '{filename}'.format(root=render_root_path,
                                           sep=os.path.sep,
                                           sub_level=user_sub_level + os.path.sep if user_sub_level else '',
                                           filename='_'.join(components) + '.%04d' + ext_value)
    return render_file_path
