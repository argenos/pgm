#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pgm.networks.jt

Strong Join Tree for Influence Diagrams

"""
__author__ = "Argentina Ortega Sainz"
__copyright__ = "Copyright 2015, Argentina Ortega Sainz"
__credits__ = ["Argentina Ortega Sainz"]
__date__ = "July 19, 2015"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Argentina Ortega Sainz"
__email__ = "argentina.ortega@smail.inf.h-brs.de"
__status__ = "Development"

import matplotlib.pyplot as plt

from itertools import combinations
import networkx as nx

from pgm.nodes.chance import Chance
from pgm.nodes.decision import Decision
from pgm.nodes.utility import Utility

from pgm.utils.tools import draw, node_types, ancestors

class TriangulatedGraph(object):
    def __init__(self, graph, ugraph):
        """


        :type ugraph: DiGraph
        :type graph: Graph
        """
        self.graph = graph.copy()
        self.ugraph = ugraph.copy()
        self.ordering = []

        self.chance, self.decision, self.utility = node_types(self.graph)




    def neighbors(self, node):
        pass


    #Get strong elimination order In, Dn, In-1, Dn-1...
    '''
    1. Eliminate simplicial node X; fa(x) is a clique candidate
    2. if fa(x) does not include all remaining nodes go to 1
    3. prune the set of clique candidates by removing sets that are subsets of other clique candidates

    '''


class JoinTree(object):
    def __init__(self):
        pass


class StronJunctionTree(object):
    def __init__(self):
        pass


