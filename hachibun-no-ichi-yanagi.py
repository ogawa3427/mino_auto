import random
import matplotlib.pyplot as plt
import numpy as np

class Operation:
    def __init__(self, shape_name, rotation, flip, position):
        self.shape_name = shape_name
        self.rotation = rotation
        self.flip = flip
        self.position = position

    def __str__(self):
        return f"形状: {self.shape_name}, 回転: {self.rotation}度, 反転: {'あり' if self.flip else 'なし'}, 位置: {self.position}"

o = [["o", "o"], ["o", "o"]]
i = [["i"], ["i"], ["i"], ["i"], ["i"]]
l = [["l","B"], ["l","B"], ["l","B"], ["l", "l"]]
n = [["n", "n", "B", "B"], ["B", "n", "n", "n"]]
w = [["B", "w", "w"], ["w", "w", "B"], ["w", "B", "B"]]
x = [["B", "x", "B"], ["x", "x", "x"], ["B", "x", "B"]]
u = [["u", "B", "u"], ["u", "u", "u"]]
z = [["z", "z", "B"], ["B", "z", "B"], ["B", "z", "z"]]
f = [["B", "f", "f"], ["f", "f", "B"], ["B", "f", "B"]]
p = [["p", "p", "B"], ["p", "p", "p"]]
t = [["t", "t", "t"], ["B", "t", "B"], ["B", "t", "B"]]
v = [["v", "B", "B"], ["v", "B", "B"], ["v", "v", "v"]]
y = [["y", "y", "y", "y"], ["B", "B", "y", "B"]]

color_map = {"o": [255, 255, 0],
                "i": [0, 255, 255],
                "l": [255, 0, 255],
                "n": [0, 0, 255],
                "w": [255, 255, 255],
                "x": [0, 255, 0],
                "u": [255, 0, 0],
                "z": [0, 0, 0],
                "f": [255, 128, 0],
                "p": [128, 0, 255],
                "t": [0, 128, 255],
                "v": [255, 0, 128],
                "y": [128, 255, 0],
                "B": [0, 0, 0],
                "E": [50, 50, 50]}

shapes = [o, i, l, n, w, x, u, z, f, p, t, v, y]

def perform_operations(field, operations, used_shapes):
    error_occurred = False
    for shape in shapes:
        if shape in used_shapes:
            continue

        for rotation in [0, 90, 180, 270]:
            for flip in [True, False]:
                for start_x in range(len(field[0]) - len(shape[0])):
                    for start_y in range(len(field) - len(shape)):
                        if error_occurred:
                            return False

                        shape_name = ['o', 'i', 'l', 'n', 'w', 'x', 'u', 'z', 'f', 'p', 't', 'v', 'y'][shapes.index(shape)]

                        for _ in range(rotation // 90):
                            shape = [list(x) for x in zip(*shape[::-1])]

                        if flip:
                            shape = shape[::-1]

                        operations.append(Operation(shape_name, rotation, flip, (start_x, start_y)))

                        for i in range(len(shape)):
                            for j in range(len(shape[0])):
                                if field[start_y + i][start_x + j] != "":
                                    error_occurred = True
                                    break
                                else:
                                    field[start_y + i][start_x + j] = shape[i][j]

        used_shapes.append(shape)

    if error_occurred:
        return False
    else:
        return operations

trial = 0
while True:
    field = [["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""]]
    operations = []
    used_shapes = []
    result = perform_operations(field, operations, used_shapes)
    if result:
        print(f"{trial}回目の試行で成功しました。操作手順は以下の通りです。")
        for operation in result:
            print(operation)
        break
    trial += 1
    if trial % 1000000 == 0:
        print(f"{trial}回目の試行")
