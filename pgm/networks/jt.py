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

import networkx as nx

from pgm.utils.tools import node_types, draw_graph


class TriangulatedGraph(object):
    def __init__(self, ugraph, partial_order):
        """


        :type ugraph: DiGraph
        :type partial_order: Tuple
        """
        assert isinstance(ugraph, nx.Graph)
        # assert isinstance(window, list)

        self.ugraph = ugraph.copy()
        # print len(self.ugraph.edges())
        self.window, self.ordering = partial_order

        self.chance, self.decision, self.utility = node_types(self.ugraph)

        self.graph = nx.DiGraph(title='triangulated')
        self.graph.add_nodes_from(self.ugraph.nodes(data=True))
        # print self.graph.node
        # print len(self.graph.edges())
        # self.graph.add_nodes_from(self.ugraph.to_directed())
        # print self.ugraph.edges()

        for e in self.ugraph.edges_iter():
            if self.ordering.get(e[0]) > self.ordering.get(e[1]):
                # print e[0],'->',e[1]
                self.graph.add_edge(e[1], e[0])
            else:
                self.graph.add_edge(e[0], e[1])

        # print self.graph.edges()

        draw_graph(self.graph, True)

    # Get strong elimination order In, Dn, In-1, Dn-1...
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
