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

from itertools import combinations

import matplotlib.pyplot as plt
import networkx as nx

from pgm.nodes.chance import Chance
from pgm.nodes.decision import Decision
from pgm.nodes.utility import Utility
from pgm.utils.tools import draw_graph, node_types
from pgm.networks.jt import TriangulatedGraph


class ID(object):
    def __init__(self, name, nodes=None, edges=None):
        print 'Influence Diagram'
        self.title = name
        self.net = nx.DiGraph(title=name)
        self._moralgraph = nx.Graph(title=name + '_moral')

        if nodes is None:
            self.nodes = []
        else:
            self.nodes = [n.node for n in nodes]
            self.net.add_nodes_from(self.nodes)

        self.chance, self.decision, self.utility = node_types(self.net)

        if edges is None:
            self.edges = []
        else:
            self.edges = [(e[0].name, e[1].name) for e in edges]
            self.net.add_edges_from(self.edges)

        self.windows = {}
        self.order = {}
        self.temporal_order()

    def temporal_order(self):
        des = []
        observed = []

        # Sort decision orders
        for d in self.decision:
            pred = list(set(nx.ancestors(self.net, d)) & set(self.decision))
            des.insert(len(pred), d)
            n = len(pred) * 2
            parents = self.net.predecessors(d)
            observed.extend(parents)
            self.windows[n + 1] = [d]
            self.windows[n] = list(set(parents).difference(set(self.decision)))
            self.order[d] = n + 1
            self.order.update({p: n for p in parents})
        n = max(self.order.values()) + 1
        unobserved = list(set(self.chance).difference(observed))
        self.order.update({u: n for u in unobserved})
        self.windows.update({n: unobserved})
        print 'Order', self.order
        print 'Windows: ', self.windows
        # l = [[1, 2, 3, 4], [5, 6, 7, 8]]
        # dict(tuple(zip(*l)))
        # {1: 5, 2: 6, 3: 7, 4: 8}

    def show(self):
        nx.draw_networkx(self.net)
        plt.show()

    def validate(self, verbose=False):
        for n in self.net.nodes():
            if verbose:
                print '----------'
                print n
                print '----------'
                print 'Parents: ' + self.net.predecessors(n).__str__()
                print 'Children: ' + self.net.successors(n).__str__()
                print 'Neighbors: ' + self.net.neighbors(n).__str__()
                print
        print 'ID is validated.'

    def add_nodes(self, new):
        assert all(isinstance(n, (Chance, Decision, Utility)) for n in new)
        self.nodes.extend(new)
        self.net.add_nodes_from(new)

    def add_edges(self, edg):
        self.edges.extend(edg)
        self.net.add_edges_from(edg)

    def moralize(self):
        moral = MoralGraph(self.net)
        self._moralgraph = moral.moralgraph

    def triangulate(self):
        tgraph = TriangulatedGraph(self._moralgraph, (self.windows, self.order))
        return tgraph

    @property
    def evidence(self):
        return 0

    @evidence.setter
    def evidence(self, ev):
        pass

    @property
    def moralgraph(self):
        draw_graph(self._moralgraph)
        return self._moralgraph


class MoralGraph(object):
    def __init__(self, graph):
        """
        Domain graph of influence diagram.
        Remove information links, adds moral links, removes directions and utility nodes.
        :param graph:
        :return:
        """
        """
        :param graph:
        :return:
        """
        self.graph = graph.copy()
        # draw_graph(self.graph, '1_graph')

        self.chance, self.decision, self.utility = node_types(self.graph)

        # Remove information links
        for n in self.decision:
            for p in self.graph.predecessors(n):
                self.graph.remove_edge(p, n)
        # draw_graph(self.graph, "2_no_info_links")

        # Add moral links
        moral_edges = []
        for n in self.graph.nodes_iter():
            moral_edges.extend(list(combinations(self.graph.predecessors(n), 2)))
        self.graph.add_edges_from(moral_edges)
        # k[::-1] reverses a tuple
        # draw_graph(self.graph, '3_moral_links')

        # Convert to undirected graph
        self.ugraph = self.graph.to_undirected()
        # draw_graph(self.ugraph, '4_undirected')
        # print self.ugraph.node
        # Remove utility nodes
        self.ugraph.remove_nodes_from(self.utility)
        # draw_graph(self.ugraph, '5_moral_graph')

    @property
    def moralgraph(self):
        return self.ugraph


def weather_example():
    # Weather example
    weather = Chance('Weather', domain=['no rain', 'rain'])
    forecast = Chance('Forecast', domain=['sunny', 'rainy', 'cloudy'])
    umbrella = Decision('Umbrella', domain=['take it', 'leave it'])
    utility = Utility('V')

    nodes = [weather, forecast, umbrella, utility]
    edges = [(weather, forecast), (forecast, umbrella), (weather, utility), (umbrella, utility)]

    example = ID('Take Umbrella', nodes, edges)
    example.show()
    example.validate(True)
    example.moralize()

    print 'Weather'
    print weather.jpt
    print '\nForecast'
    print forecast.jpt
    print '\nUtility'
    print utility.ut


def test_example():
    a = Chance('A')
    b = Chance('B')
    c = Chance('C')
    d = Chance('D')
    e = Chance('E')
    f = Chance('F')
    g = Chance('G')
    h = Chance('H')
    i = Chance('I')
    j = Chance('J')
    k = Chance('K')
    l = Chance('L')

    d1 = Decision('D1')
    d2 = Decision('D2')
    d3 = Decision('D3')
    d4 = Decision('D4')

    v1 = Utility('V1')
    v2 = Utility('V2')
    v3 = Utility('V3')
    v4 = Utility('V4')

    nodes = [a, b, c, d, e, f, g, h, i, j, k, l, d1, d2, d3, d4, v1, v2, v3, v4]
    edges = [(a, c), (b, c), (b, d1), (b, d), (d1, v1), (d1, d),
             (c, e), (d, e), (d, f), (e, g), (e, d2), (f, d2), (f, h),
             (g, d4), (g, i), (d2, i), (d2, d3), (h, k), (h, j), (d3, k), (d3, v2), (d3, d4),
             (d4, l), (i, l), (j, v3), (k, v3), (l, v4)]

    test = ID('Test', nodes, edges)
    test.validate(True)
    test.moralize()


def nx_example():
    a = Chance('A')
    b = Chance('B')
    c = Chance('C')
    d = Chance('D')
    e = Chance('E')
    f = Chance('F')
    g = Chance('G')
    h = Chance('H')
    i = Chance('I')
    j = Chance('J')
    k = Chance('K')
    l = Chance('L')

    d1 = Decision('D1')
    d2 = Decision('D2')
    d3 = Decision('D3')
    d4 = Decision('D4')

    v1 = Utility('V1')
    v2 = Utility('V2')
    v3 = Utility('V3')
    v4 = Utility('V4')

    chance = [a, b, c, d, e, f, g, h, i, j, k, l]
    decision = [d1, d2, d3, d4]
    utility = [v1, v2, v3, v4]

    edges = [(a, c), (b, c), (b, d1), (b, d), (d1, v1), (d1, d),
             (c, e), (d, e), (d, f), (e, g), (e, d2), (f, d2), (f, h),
             (g, d4), (g, i), (d2, i), (d2, d3), (h, k), (h, j), (d3, k), (d3, v2), (d3, d4),
             (d4, l), (i, l), (j, v3), (k, v3), (l, v4)]
    nodes = []
    nodes.extend(chance)
    nodes.extend(decision)
    nodes.extend(utility)

    test = ID('Test', nodes, edges)
    test.validate()
    test.moralize()
    # print nx.is_chordal(test.moralgraph)
    # cliques = list(nx.find_cliques(test.moralgraph))
    # print cliques
    test.triangulate()


if __name__ == '__main__':
    # weather_example()
    # test_example()
    nx_example()
