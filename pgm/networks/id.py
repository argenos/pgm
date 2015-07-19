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

import matplotlib.pyplot as plt
from itertools import combinations
import networkx as nx
from pgm.nodes.chance import Chance
from pgm.nodes.decision import Decision
from pgm.nodes.utility import Utility


class ID(object):
    def __init__(self, title, nodes=None, edges=None):
        print 'Influence Diagram'
        self.title = title
        self.net = nx.DiGraph()
        self._moralgraph = nx.Graph()

        self.decision = []
        self.chance = []
        self.utility = []

        if nodes is None:
            self.nodes = []
        else:
            self.nodes = nodes[:]
            self.node_types()
            self.net.add_nodes_from(self.nodes)

        if edges is None:
            self.edges = []
        else:
            self.edges = edges[:]
            self.net.add_edges_from(self.edges)

    def node_types(self):
        for n in self.nodes:
            if isinstance(n, Chance):
                self.chance.append(n)
            elif isinstance(n, Decision):
                self.decision.append(n)
            elif isinstance(n, Utility):
                self.utility.append(n)

    def show(self):
        nx.draw_networkx(self.net)
        plt.show()

    def validate(self, verbose=False):
        for n in self.nodes:
            n.parents = self.net.predecessors(n)
            n.children = self.net.successors(n)
            n.neighbors = self.net.neighbors(n)
            n.validate()
            if verbose:
                print '----------'
                print n
                print '----------'
                print 'Parents: ' + n.parents.__str__()
                print 'Children: ' + n.children.__str__()
                print 'Neighbors: ' + n.neighbors.__str__()
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
        # draw(self.graph, '1_graph')

        self.chance, self.decision, self.utility = node_types(self.graph.nodes())

        # Remove information links
        for n in self.decision:
            for p in n.parents:
                self.graph.remove_edge(p, n)
        # draw(self.graph, "2_no_info_links")

        # Add moral links
        moral_edges = []
        for n in self.graph.nodes():
            moral_edges.extend(list(combinations(n.parents, 2)))
        self.graph.add_edges_from(moral_edges)
        # draw(self.graph, '3_moral_links')

        # Convert to undirected graph
        self.ugraph = nx.Graph(self.graph)
        # draw(self.ugraph, '4_undirected')

        # Remove utility nodes
        self.ugraph.remove_nodes_from(self.utility)

        print self.ugraph.edges()
        print nx.is_chordal(self.ugraph)
        # draw(self.ugraph, '5_moral_graph')

    @property
    def moralgraph(self):
        return self.ugraph


def node_types(nodes):
    chance = []
    decision = []
    utility = []
    for n in nodes:
        if isinstance(n, Chance):
            chance.append(n)
        elif isinstance(n, Decision):
            decision.append(n)
        elif isinstance(n, Utility):
            utility.append(n)

    return chance, decision, utility


def draw(graph, title='graph.png', show=False):
    # 's' = square
    # 'D' = diamond
    # 'o' = circle

    plt.figure()

    chance, decision, utility = node_types(graph.nodes())
    pos = nx.graphviz_layout(graph, prog='dot')

    if len(chance) > 0:
        nx.draw_networkx_nodes(graph, pos, nodelist=chance, node_size=800)
    if len(decision) > 0:
        nx.draw_networkx_nodes(graph, pos, nodelist=decision, node_size=800, node_shape='s')
    if len(utility) > 0:
        nx.draw_networkx_nodes(graph, pos, nodelist=utility, node_size=800, node_shape='D')

    nx.draw_networkx_edges(graph, pos=pos)
    nx.draw_networkx_labels(graph, pos=pos)

    nx.write_dot(graph, title + '.dot')
    plt.savefig(title + '.png')

    if show:
        plt.show()


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


if __name__ == '__main__':
    # weather_example()
    test_example()
