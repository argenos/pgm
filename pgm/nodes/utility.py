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
    def graph(self):
        return pydot.Node(name=self.name, shape='diamond')

    def __repr__(self):
        return '<Utility %s>' % self.name

    def ut(self):
        # Index for parents
        """
        index = MultiIndex.from_product([rain, sprinkler],names = ['rain','sprinkler'])
        cols = MultiIndex.from_product([['Grass'],domain])
        df = DataFrame(np.random.rand(4,2),index,columns=cols)
        :return:
        """

        parents_names = []
        parents_domains = []
        m = 1
        n = 1
        for parent in self.parents:
            parents_names.append(parent.name)
            parents_domains.append(parent.domain)
            m = m * parent.domain.__len__()

        # print rows, m
        # cols = MultiIndex.from_product([self.domain], names=[self.name])

        if self.parents.__len__() != 0:
            rows = MultiIndex.from_product(parents_domains, names=parents_names)
            u = DataFrame(np.random.rand(m, n), index=rows, columns=['Utility'])
        else:
            u = DataFrame(np.random.rand(m, n), columns=['Utility'])

        print u
