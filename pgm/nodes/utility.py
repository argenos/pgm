#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pgm.nodes.utility

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
from pandas import DataFrame, MultiIndex
import numpy as np


class Utility(node.Node):
    def __init__(self, name, parents=None, children=None):
        super(Utility, self).__init__(name, parents, children)
        self._ut = UT(self._name, self._parents)

    def validate(self):
        self._ut = UT(self._name, self._parents)

    def graph(self):
        return pydot.Node(name=self.name, shape='diamond')

    def __repr__(self):
        return '<Utility %s>' % self.name

    def __str__(self):
        return '<%s>' % self.name

    @property
    def ut(self):
        return self._ut

    @ut.setter
    def ut(self, table):
        self._ut.table = table

class UT(node.Table):
    def __init__(self, node_name, parents=None):
        super(UT, self).__init__(node_name)
        self.m = 1
        self.n = 1
        if parents is None or parents.__len__() == 0:
            self.rows = [self._name]
        else:
            parents_names = []
            parents_domains = []
            for parent in parents:
                parents_names.append(parent.name)
                parents_domains.append(parent.domain)
                self.m = self.m * parent.domain.__len__()
            self.rows = MultiIndex.from_product(parents_domains, names=parents_names)
        self.cols = ['Utility']

        # self._table = DataFrame(np.zeros((0, self.n)), columns=self.cols)
        self._table = DataFrame(np.zeros((self.m, self.n)), index=self.rows, columns=self.cols)
        #print self._table

    def __repr__(self):
        return '<Utility Table %s>' % self._name

