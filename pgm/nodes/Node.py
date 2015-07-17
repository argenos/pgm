#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pgm.nodes.node

Node

"""
__author__ = "Argentina Ortega Sainz"
__copyright__ = "Copyright 2015, Argentina Ortega Sainz"
__credits__ = ["Argentina Ortega Sainz"]
__date__ = "July 15, 2015"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Argentina Ortega Sainz"
__email__ = "argentina.ortega@smail.inf.h-brs.de"
__status__ = "Development"

import pydot


class Node(object):
    def __init__(self, name='Node', parents=None, children=None, domain=None):
        self.name = name

        if parents is None:
            self.parents = []
        else:
            self.parents = parents[:]

        if children is None:
            self.children = []
        else:
            self.children = children[:]

        if domain is None:
            self.domain = ['T', 'F']
        else:
            self.domain = domain[:]

        self.neighbors = []
        self.neighbors.extend(self.parents)
        self.neighbors.extend(self.children)

    def __name__(self):
        pass

    def __iter__(self):
        return self

    def __hash__(self):
        return hash(self.name)

    def __doc__(self):
        pass

    def __module__(self):
        pass

    def __dict__(self):
        pass

    @property
    def graph(self):
        return pydot.Node(name=self.name, shape='ellipse')

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Node %s>' % self.name

    def jpt(self):
        pass
