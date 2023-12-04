import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

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
                "u": [198, 0, 0],
                "z": [0, 198, 0],
                "f": [0, 0, 198],
                "p": [198, 198, 0],
                "t": [0, 198, 198],
                "v": [198, 0, 198],
                "y": [255, 128, 128],
                "": [0, 0, 0],
                "E": [50, 50, 50]}

color_list = list(color_map.values())
cmap = mcolors.LinearSegmentedColormap.from_list('custom_map', color_list)

error_num = 0

fig, axs = plt.subplots(8, 8, figsize=(15, 15))

for q in range(64):
    shapes = [o, i, l, n, w, x, u, z, f, p, t, v, y]

    field = [["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""]]

    operations = []

    non_empty_cells = 0
    for ii in range(13):
        shape = random.choice(shapes)
        shapes.remove(shape)

        rotation = random.choice([0, 90, 180, 270])
        flip = random.choice(["none", "horizontal", "vertical", "both"])
        start_pos_x = random.randint(0, len(field[0]) - len(shape[0]))
        start_pos_y = random.randint(0, len(field) - len(shape))

        if flip == "horizontal":
            shape = shape[::-1]
        elif flip == "vertical":
            shape = [list(x) for x in zip(*shape[::-1])]
        elif flip == "both":
            shape = [list(x) for x in zip(*shape[::-1])]
            shape = shape[::-1]

        for _ in range(rotation // 90):
            shape = [list(x) for x in zip(*shape[::-1])]

        for shape_x in range(len(shape[0])):  
            for shape_y in range(len(shape)):  
                if start_pos_y + shape_y < len(field) and start_pos_x + shape_x < len(field[0]):
                    if field[start_pos_y + shape_y][start_pos_x + shape_x] != "" and shape[shape_y][shape_x] != "":
                        field[start_pos_y + shape_y][start_pos_x + shape_x] = "E" 
                    else:
                        field[start_pos_y + shape_y][start_pos_x + shape_x] = shape[shape_y][shape_x]

        # Count cells that are neither empty string nor "E"
        non_empty_cells = sum([1 for row in field for cell in row if cell != "" and cell != "E"])

    field_array = np.array([[color_map[item] for item in row] for row in field])
    axs[q // 8, q % 8].imshow(field_array)
    axs[q // 8, q % 8].set_title(f"{non_empty_cells}")  # Display the number of non-empty cells in the title

plt.show()
