#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pgm.nodes.decision

Decision

"""
__author__ = "Argentina Ortega Sáinz"
__copyright__ = "Copyright 2015, Argentina Ortega Sáinz"
__credits__ = ["Argentina Ortega Sáinz"]
__date__ = "July 15, 2015"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Argentina Ortega Sáinz"
__email__ = "argentina.ortega@smail.inf.h-brs.de"
__status__ = "Development"

import pydot
import node


class Decision(node.Node):
    def __init__(self, name, parents=None, children=None, domain=None):
        if domain is None:
            domain = ['d1', 'd2']
        super(Decision, self).__init__(name, parents, children, domain)

    @property
    def graph(self):
        return pydot.Node(name=self.name, shape='box')
