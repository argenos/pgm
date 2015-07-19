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
from pandas import DataFrame, MultiIndex
import numpy as np

class Node(object):
    def __init__(self, name='Node', parents=None, children=None):
        self._name = name

        if parents is None:
            self._parents = []
        else:
            self._parents = parents[:]

        if children is None:
            self._children = []
        else:
            self._children = children[:]

        self._neighbors = []
        self._neighbors.extend(self.parents)
        self._neighbors.extend(self.children)

    def __iter__(self):
        return self

    def __hash__(self):
        return hash(self.name)

    @property
    def graph(self):
        return pydot.Node(name=self._name, shape='ellipse')

    def __str__(self):
        return self._name

    def __repr__(self):
        return '<Node %s>' % self._name

    @property
    def domain(self):
        return self._domain

    @property
    def parents(self):
        return self._parents

    @property
    def children(self):
        return self._children

    @property
    def name(self):
        return self._name

    @domain.setter
    def domain(self, value):
        self._domain = value

    @parents.setter
    def parents(self, value):
        # TODO: check probability tables when assigning parents (keep values if there are any)
        # TODO: update validate method to only check for right dimensions in table
        self._parents = value

    @children.setter
    def children(self, value):
        self._children = value

    @name.setter
    def name(self, value):
        self._name = value


class Table(object):
    def __init__(self, node_name):
        self._name = node_name

        self.m = 1
        self.n = 1

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, value):
        assert value.shape == (self.m, self.n)
        self._table = DataFrame(value, index=self.rows, columns=self.cols)
        #print self._table

    def __repr__(self):
        return '<Table %s>' % self._name

    def __str__(self):
        return self._table.to_string()