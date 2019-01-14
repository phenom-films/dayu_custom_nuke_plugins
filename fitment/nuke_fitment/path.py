#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'pengyuxuan'

import os
from functools import partial

SEP = os.sep


class Path(unicode):

    def __init__(self, path_string):
        super(Path, self).__init__(path_string)

        self.isfile = partial(os.path.isfile, path_string)
        self.isdir = partial(os.path.isdir, path_string)

    def isfile(self):
        return os.path.isfile(self)

    def isdir(self):
        return os.path.isdir(self)

    def child(self, *args):
        path_list = list(args)
        path_list.insert(0, self)
        return self.__class__(SEP.join(path_list))

    @property
    def parent(self):
        return self.__class__(os.path.dirname(self))

    @property
    def ext(self):
        return os.path.splitext(self)[-1]

    @property
    def name(self):
        return os.path.basename(self)

    @property
    def stem(self):
        path_base = os.path.splitext(self)[0]
        return os.path.basename(path_base)

    def listdir(self, file_filter=None):
        names = os.listdir(self)
        ret = [self.child(x) for x in names]
        if file_filter:
            ret = filter(file_filter, ret)
        return ret

    def walk(self, filter=None):
        return self._walk(filter, seen=set())

    def _walk(self, filter, seen):
        if not self.isdir():
            raise OSError("not a directory: %s" % self)
        real_dir = os.path.realpath(self)

        if real_dir in seen:
            return  # We've already recursed this directory.

        seen.add(real_dir)
        for child in self.listdir():
            is_dir = child.isdir()
            if filter is None or filter(child):
                yield child
            if is_dir:
                for grandkid in child._walk(filter, seen):
                    yield grandkid

    def absolute(self):
        return self.__class__(os.path.abspath(self))
