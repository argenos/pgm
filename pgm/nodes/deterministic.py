__author__ = 'Argen'

import pydot
import node

class Deterministic(node.Node):
    def __init__(self, name, parents = [], children = []):
        self.name = name
        self.parents = parents[:]
        self.children = children[:]
