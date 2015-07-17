#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pgm.networks.id

Influence Diagram


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

import networkx as nx
from pgm.nodes.chance import Chance
from pgm.nodes.decision import Decision
from pgm.nodes.utility import Utility


class InfluenceDiagram:
    def __init__(self, title, nodes=None, edges=None):
        print 'Influence Diagram'
        self.title = title
        if nodes is None:
            self.nodes = []
        else:
            self.nodes = nodes[:]

        if edges is None:
            self.edges = []
        else:
            self.edges = edges[:]

    def show(self):
        pass

    def add_nodes(self, new):
        assert all(isinstance(n, (Chance, Decision, Utility)) for n in new)
        self.nodes.extend(new)
    
    def add_edges(self, edg):
        self.edges.extend(edg)

if __name__ == '__main__':
    w = Chance('Weather', domain=['no rain', 'rain'])
    f = Chance('Forecast', parents=[w], domain=['sunny', 'rainy', 'cloudy'])
    d = Decision('Umbrella', parents=[f], domain=['take it', 'leave it'])
    u = Utility('V', parents=[w, d])

    net = nx.MultiDiGraph()
    # net.add_node(w)
    # net.add_node(f)
    net.add_nodes_from([w, f, d, u])
    net.add_edges_from([(w, f), (f, d), (w, u), (d, u)])

    print 'Weather'
    w.jpt()
    print 'Forecast'
    f.jpt()
    print 'Decision'
    d.jpt()
    print 'Utility'
    u.ut()

    print net.nodes()

    nx.draw(net)

    print net.neighbors(w)
    print net.predecessors(u)
    print net.successors(w)
