#!/usr/bin/env python3

from enum import Enum


class NodeType(Enum):
    Comment = 1
    Definition = 2
    Other = 3


class Node:
    def __init__(self, node_type: NodeType):
        self.node_type = node_type