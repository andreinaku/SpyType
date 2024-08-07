# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
# from __future__ import print_function

import curses
import sys


class CursesAPI(object):

    """A dummy curses wrapper that allows us to intercept these
    calls when in a test environment"""

    def __init__(self):
        pass

    def useDefaultColors(self):
        curses.use_default_colors()

    def echo(self):
        curses.echo()

    def noecho(self):
        curses.noecho()

    def initPair(self, pairNumber, fg, bg):
        return curses.init_pair(pairNumber, fg, bg)

    def colorPair(self, colorNumber):
        return curses.color_pair(colorNumber)

    def getColorPairs(self):
        return curses.COLOR_PAIRS

    def exit(self):
        sys.exit(0)

    def allowFileOutput(self):
        return True
