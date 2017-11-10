from threading import Thread
from queue import Queue

from .node import Node, PeriodicNode, RateLimitedNode


class Graph:
    def __init__(self):
        self.nodes = []

    def node(self, input=None, num_outputs=1, target=None):
        return self.__node_internal(input=input, num_outputs=num_outputs, target=target,
                                    node_type=Node)

    def rate_limited_node(self, interval, input=None, num_outputs=1, target=None):
        return self.__node_internal(input=input, num_outputs=num_outputs, target=target, interval=interval,
                                    node_type=RateLimitedNode)

    def periodic_node(self, period):
        return self.__make_node(args={
            'period': period,
        }, node_type=PeriodicNode)

    def __node_internal(self, input, num_outputs, target, node_type, **kwargs):
        args = {
            'inputs': Graph.__clean_input(input),
            'num_outputs': num_outputs,
        }
        for key, value in kwargs.items():
            args[key] = value

        # If there is no target, assume we're working as an annotation
        if target is None:
            # And return a function that takes a function, makes a node out of it, and adds it
            def wrapper(f) -> Node:
                args['target'] = f
                return self.__make_node(args=args, node_type=node_type)
            return wrapper

        else:
            # If there is a target, make a standard node out of that
            args['target'] = target
            return self.__make_node(args=args, node_type=node_type)

    def __make_node(self, args, node_type):
        n = node_type(**args)
        self.nodes.append(n)
        return n

    @staticmethod
    def __clean_input(inp):
        if not inp:
            return []
        elif isinstance(inp, Queue):
            return [inp]
        else:
            return inp

    def run(self):
        for node in self.nodes:
            t = Thread(target=node.run)
            t.start()

'''
    def rate_limited_node(self, interval, input=None, num_outputs=1, target=None):
        if not input:
        if isinstance(input, Queue):
            inp = [input]
        else:
            inp = input

        if target is None:
            def wrapper(f) -> Node:
                n = RateLimitedNode(interval=interval, target=f, inputs=inp, num_outputs=num_outputs)
                self.nodes.append(n)
                return n
            return wrapper

        else:
            n = Node(target=target, inputs=inp, num_outputs=num_outputs)
            self.nodes.append(n)
            return n
            '''
