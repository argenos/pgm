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
    def __init__(self, name, parents=None, children=None, domain=None):
        if domain is None:
            self._domain = ['T', 'F']
        else:
            self._domain = domain[:]
        super(Chance, self).__init__(name, parents, children)
        self._jpt = CPT(self._name, self._parents, self._domain)

    def __repr__(self):
        return '<Chance Node %s>' % self.name

    def __str__(self):
        return '(%s)' % self.name

    def validate(self):
        self._jpt = CPT(self._name, self._parents, self._domain)

    @property
    def node(self):
        attr = (('type', 'chance'), ('domain', self._domain), ('jpt', self._jpt))
        return self._name, dict(attr)

    @property
    def edge(self):
        attr = (('type', 'causal'))
        return dict(attr)

    @property
    def jpt(self):
        return self._jpt

    @jpt.setter
    def jpt(self, table):
        self._jpt.table = table


class CPT(node.Table):
    def __init__(self, node_name, parents=None, node_domain=None):
        super(CPT, self).__init__(node_name)

        if node_domain is None or node_domain.__len__() == 0:
            self._domain = ['T', 'F']
        else:
            self._domain = node_domain[:]

        self.m = 1
        self.n = self._domain.__len__()

        if parents is None or parents.__len__() == 0:
            self.rows = [self._name]
            self.cols = MultiIndex.from_product([self._domain])
        else:
            parents_names = []
            parents_domains = []
            for parent in parents:
                parents_names.append(parent.name)
                parents_domains.append(parent.domain)
                self.m = self.m * parent.domain.__len__()
            self.cols = MultiIndex.from_product([self._domain], names=[self._name])
            self.rows = MultiIndex.from_product(parents_domains, names=parents_names)

        self._values = np.zeros((self.m, self.n))
        self._table = DataFrame(self._values, index=self.rows, columns=self.cols)

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, value):
        assert value.shape == (self.m, self.n)
        self._table = DataFrame(value, index=self.rows, columns=self.cols)
        # print self._table

    def __repr__(self):
        return '<CPT %s>' % self._name


if __name__ == "__main__":
    a = Chance('a')
    b = Chance('b')
    c = Chance('c', parents=[a, b])

    c.jpt = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    # print c.jpt

    '''
    x = CPT('x')
    print x.table
    j = np.array([[1,5]])
    print j
    x.table = j
    print x.table
    '''
    '''
    print a._domain
    print a.parents
    print a.children
    print c._domain
    '''
