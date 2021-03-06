from unittest import TestCase
from io import StringIO
from plot import plot
from load_graph import load_graph


class TestLoadGraph(TestCase):
    def test_load_graph(self):
        input_str = """1
        300,300,255,0,0,0,255,0,0,0,255,0,0,0
        5
        0,300,300,0
        2
        0,300,300,0,100,100,100
        3
        0,300,300,300,255,255,0
        3
        0,0,0,300,255,0,255
        3
        0,0,300,0,0,0,100
        3
        300,0,300,300,0,100,0
        """

        graph = load_graph(StringIO(input_str))
        plot(graph)
