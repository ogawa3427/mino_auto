import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import copy
import networkx as nx

id_counter = 0 
class Operation:
    def __init__(self, shape_name, rotation, flip, position):
        self.shape_name = shape_name
        self.rotation = rotation
        self.flip = flip
        self.position = position

    def __str__(self):
        return f"形状: {self.shape_name}, 回転: {self.rotation}度, 反転: {'あり' if self.flip else 'なし'}, 位置: {self.position}"

o = [["o", "o"], ["o", "o"]]
i = [["i", "i", "i", "i", "i"]]
l = [["l",""], ["l",""], ["l",""], ["l", "l"]]
n = [["n", "n", "", ""], ["", "n", "n", "n"]]
w = [["", "w", "w"], ["w", "w", ""], ["w", "", ""]]
x = [["", "x", ""], ["x", "x", "x"], ["", "x", ""]]
u = [["u", "", "u"], ["u", "u", "u"]]
z = [["z", "z", ""], ["", "z", ""], ["", "z", "z"]]
f = [["", "f", "f"], ["f", "f", ""], ["", "f", ""]]
p = [["p", "p", ""], ["p", "p", "p"]]
t = [["t", "t", "t"], ["", "t", ""], ["", "t", ""]]
v = [["v", "", ""], ["v", "", ""], ["v", "v", "v"]]
y = [["y", "y", "y", "y"], ["", "", "y", ""]]

color_map = {"o": [255, 255, 255],
                "i": [0, 255, 0],
                "l": [0, 0, 255],
                "n": [255, 255, 0],
                "w": [0, 255, 255],
                "x": [255, 0, 255],
                "u": [198, 30, 90],
                "z": [90, 198, 30],
                "f": [30, 90, 198],
                "p": [198, 198, 0],
                "t": [0, 198, 198],
                "v": [198, 0, 198],
                "y": [255, 0, 0],
                "": [0, 0, 0],
                "E": [50, 50, 50]}

color_list = list(color_map.values())
cmap = mcolors.LinearSegmentedColormap.from_list('custom_map', color_list)

error_num = 0

operationses = []

non_empty_cells_list = []