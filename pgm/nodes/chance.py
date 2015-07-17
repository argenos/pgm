#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pgm.nodes.chance

Chance

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

import node
from pandas import DataFrame, MultiIndex
import numpy as np


class Chance(node.Node):

    def jpt(self):
        # Index for parents
        '''
        index = MultiIndex.from_product([rain, sprinkler],names = ['rain','sprinkler'])
        cols = MultiIndex.from_product([['Grass'],domain])
        df = DataFrame(np.random.rand(4,2),index,columns=cols)
        :return:
        '''

        parents_names = []
        parents_domains = []
        m = 1
        n = self.domain.__len__()
        for parent in self.parents:
            parents_names.append(parent.name)
            parents_domains.append(parent.domain)
            m = m * parent.domain.__len__()

        cols = MultiIndex.from_product([self.domain], names=[self.name])

        if self.parents.__len__() != 0:
            rows = MultiIndex.from_product(parents_domains, names=parents_names)
            t = DataFrame(np.random.rand(m, n), index=rows, columns=cols)
        else:
            t = DataFrame(np.random.rand(m, n), columns=cols)

        print t

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
        return self._id

    @domain.setter
    def domain(self, value):
        self._domain = value

    @parents.setter
    def parents(self, value):
        self._parents = value

    @children.setter
    def children(self, value):
        self._children = value

    @name.setter
    def name(self, value):
        self._id = value


if __name__ == "__main__":
    a = Chance('a')
    b = Chance('b')
    c = Chance('c', parents=[a, b])
    c.jpt()

    # print a.domain
    # print a.parents
    # print a.children
    # print c.domain
