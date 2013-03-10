#!/usr/bin/env python
import pylirc

class Buttons:
    SELECT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3
    LEFT = 4

    def __init__(self, app, conf):
        if not pylirc.init(app, conf, 1):
            raise Exception("Unable to init pylirc");
        pylirc.blocking(0)

    def readButton(self):
        btn = pylirc.nextcode()
        if btn:
            return btn[0]
        else:
            return None
