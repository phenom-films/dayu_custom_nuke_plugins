#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'pengyuxuan'

import os
import traceback
import types
from path import Path
from image_rc import *
# 启动
# 1，在环境变量NUKE_PATH 中加上 nuke_fitment 根目录
# 2，添加环境变量 MY_CUSTOM_FITMENT 指定为自定文件夹，各种脚本工具，放在此文件夹下,

# 在 MY_CUSTOM_FITMENT 指定的文件夹下，必须有一个 名为 nuke 的文件夹，层级结构参考本项目跟目录下的 nuke 文件夹
NUKE_FITMENT_ROOT_PATH = Path(os.environ.get('MY_CUSTOM_FITMENT', '')).child('nuke')

# 根目录下的默认文件夹 NUKE_MAIN_MENU_DIR 中的文件是加载到nuke主菜单上
# NUKE_TOOL_BAR_DIR 中的文件是加载到 nuke 的 toolbar 上
# NUKE_VIEWS_DIR 时用来存放LUT 的文件夹, 文件夹中的lut 文件将被加入到ViewerProcess监看之中
NUKE_MAIN_MENU_DIR = 'main_menu'
NUKE_TOOL_BAR_DIR = 'nodes'
NUKE_VIEWS_DIR = 'views'

# 默认工具的图标，和图标格式
NUKE_DEFAULT_ICON = ':/default.png'
RELOAD_ICON = Path(__file__).parent.child('refresh.png')
NUKE_ICON_EXT = '.png'


def _nodes_command(self):
    """
    如果找到的文件是 nk,gizmo,dll类型的文件，用nuke命令进行触发
    """
    command = ''
    if self.ext == '.nk':
        command = 'nuke.nodePaste("{}")'.format(self.file_path.absolute().replace('\\', '/'))
    elif self.ext in ['.gizmo', '.dll']:
        command = 'nuke.createNode("{}")'.format(self.file_path.stem)
    return command


def _python_command(self):
    """
    如果是py文件,则存成一条command
    """
    with open(self.file_path, 'r') as f:
        py_string = f.read()
    return py_string


def find_icon(path):
    """同层级，同名的png文件都会识别为icon"""
    path = Path(path.replace('\\', '/'))
    icon = path.parent.child(path.stem + NUKE_ICON_EXT)
    return icon if icon.isfile() else NUKE_DEFAULT_ICON


def find_hotkey(path):
    """
    同层级下，同名的.hotkey 文件会被识别为hotkey
    :param path:
    :return:
    """
    hotkey_file = os.path.sep.join([os.path.dirname(path), os.path.basename(path).split('.')[0] + '.hotkey'])
    if os.path.isfile(hotkey_file):
        with open(hotkey_file, 'r') as f:
            hotkey = f.read()
            return hotkey if hotkey else ''
    return ''


class MatchFile(object):

    def __init__(self, file_name, pre_dir):
        self.file_path = Path(file_name.replace('\\', '/'))
        self.pre_path = pre_dir.replace('\\', '/')
        self.ext = file_name.ext

        if self.ext == '.py':
            self._command = types.MethodType(_python_command, self)
        else:
            self._command = types.MethodType(_nodes_command, self)

    def _menu_level(self):
        """
        解析实例属性中的文件路径，去除掉前缀，拿到一个以文件夹层级为基准的 nuke menu 层级
        :return: menu_level 如 ‘ main/epsoid/gizmo/my_slate ’
        """
        return os.path.splitext(self.file_path.replace(self.pre_path + '/', ''))[0]

    def add_to_menu(self, parent_root):
        import nuke

        command = self._command()
        sub_level = self._menu_level()
        tooltip = self.file_path.stem

        nuke.pluginAppendPath(self.file_path.parent)
        parent_root.addCommand(sub_level, command=command, tooltip=tooltip)

        # 从根部层级 一层层的查找对应menu的icon
        parent_menu = parent_root
        icon_path = Path(self.pre_path)
        for sub in sub_level.split('/'):
            icon_path = icon_path.child(sub)
            parent_menu = parent_menu.menu(sub)
            parent_menu.setIcon(find_icon(icon_path))
            parent_menu.setShortcut(find_hotkey(icon_path))


def file_filter(f):
    if f.isfile() and f.name != '__init__.py' and f.ext in ['.py', '.nk', '.gizmo', '.dll', '.dylib', '.so']:
        return True


def lut_filter(f):
    if f.isfile() and f.ext in ['.3dl', '.blut', '.cms', '.csp', '.cub', '.cube', '.vf', 'vfz']:
        return True


def add_fitment():
    import os
    import nuke
    nuke_main_menu = nuke.menu('Nuke')
    nuke_nodes_menu = nuke.menu('Nodes')

    custom_path = os.environ.get('MY_CUSTOM_FITMENT', '')
    if not custom_path:
        return
    try:
        root_path = Path(custom_path).child('nuke')
        main_menu_dir = root_path.child(NUKE_MAIN_MENU_DIR)
        toolbar_menu_dir = root_path.child(NUKE_TOOL_BAR_DIR)
        views_dir = root_path.child(NUKE_VIEWS_DIR)

        #  main_menu 下的文件显示在主菜单上
        if main_menu_dir.isdir():
            for dir in main_menu_dir.listdir(file_filter=os.path.isdir):
                parent = nuke_main_menu.addMenu(dir.name)
                for match in dir.walk(filter=file_filter):
                    match_file = MatchFile(match, dir)
                    match_file.add_to_menu(parent)

        #  nodes 下的文件生成在 toolbar 上
        if toolbar_menu_dir.isdir():
            for dir in toolbar_menu_dir.listdir(file_filter=os.path.isdir):
                parent = nuke_nodes_menu.addMenu(dir.name, find_icon(dir))
                for match in dir.walk(filter=file_filter):
                    match_file = MatchFile(match, dir)
                    match_file.add_to_menu(parent)

        #  加载 views 下的LUT文件
        if views_dir.isdir():
            for file in views_dir.listdir(file_filter=lut_filter):
                nuke.ViewerProcess.register(file.stem, nuke.createNode,
                                            ("Vectorfield", 'vfield_file %s' % file.replace('\\', '/')))

        refresh_menu = nuke_nodes_menu.addMenu('refresh', RELOAD_ICON)
        refresh_command = refresh_menu.addCommand('refresh', command=add_fitment, tooltip='refresh')
        refresh_command.setIcon(RELOAD_ICON)

    except Exception as e:
        traceback.print_exc()
        return
