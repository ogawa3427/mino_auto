import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import copy
import json

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

def create_first_generation():
    firsters = []
    for __ in range(64):
        field = [["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                    ["", "", "", "", "", "", "", ""],
                    ["", "", "", "", "", "", "", ""],
                    ["", "", "", "", "", "", "", ""],
                    ["", "", "", "", "", "", "", ""]]
        shapes = [o, i, l, n, w, x, u, z, f, p, t, v, y]
        operationses = []
        for _ in range(12):
            shape = random.choice(shapes)
            shapes.remove(shape)

            rotation = random.randint(0, 3)
            flip = random.choice(["v", "h", "b", "n"])
            rotated_shape = np.rot90(shape, rotation)
            shape_effective_height = max(ii for ii, row in enumerate(rotated_shape) if any(cell != "" for cell in row)) + 1
            shape_effective_width = max(jj for jj in range(len(rotated_shape[0])) if any(rotated_shape[ii][jj] != "" for ii in range(len(rotated_shape)))) + 1
            position = [random.randint(0, 8 - shape_effective_height), random.randint(0, 8 - shape_effective_width)]

            operation = [shape, rotation, flip, position]
            operationses.append(operation)

        for operation in operationses:
            shape, rotation, flip, position = operation
            if flip == "v":
                shape = np.flipud(shape)
            elif flip == "h":
                shape = np.fliplr(shape)
            elif flip == "b":
                shape = np.flipud(shape)
                shape = np.fliplr(shape)
            elif flip == "n":
                pass

            shape = np.rot90(shape, rotation)

            for ii in range(len(shape)):
                for jj in range(len(shape[0])):
                    if shape[ii][jj] != "" and field[ii + position[0]][jj + position[1]] != "":
                        field[ii + position[0]][jj + position[1]] = "E"
                    elif shape[ii][jj] != "":
                        field[ii + position[0]][jj + position[1]] = shape[ii][jj]

        cell_count = sum(1 for row in field for cell in row if cell != "" and cell != "E")
        operationses.append(cell_count)
        operationses.append(__)
        #print(operationses[12]) #12はconunt
        #print(operationses[13]) #13がid 0~63

        field = [[color_map[item] for item in row] for row in field]
        plt.imshow(field, cmap=cmap, vmin=0, vmax=255)
        plt.axis('off')  # 目盛りを削除
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)  # 余白を削除
        #plt.savefig(f'0_{__}.png', bbox_inches='tight', pad_inches=0)  # 余白を削除して保存
    
        firsters.append(operationses)

    return firsters

first_gen = create_first_generation()
#print(first_gen[20])
#print(first_gen[20][12])

def elite_selection(gen,data,now_gen):
    gen.sort(key=lambda x: x[12], reverse=True)
    output = [{}, {}, {}, {}, {}, {}, {}, {}]
    for _ in range(8):
        output[_] = {
            "joint": "elite",
            "par1": gen[_][13],
            "num": gen[_][12],
        }
    return output

def tornament(gen,data,now_gen):
    tornament_list = []
    for _ in range(8):
        tornament_list.append(random.randint(0, 63))
    tornament_list.sort(key=lambda x: gen[x][12], reverse=True)
    output = [{}, {}, {}, {}, {}, {}, {}, {}]
    for _ in range(8):
        output[_] = {
            "joint": "tornament",
            "par1": tornament_list[_],
            "num": gen[tornament_list[_]][12],
        }
    return output


def mutation(gen, data, now_gen):
    for _ in range(64):
        if random.random() < 0.1:
            gen[_][random.randint(0, 11)] = random.choice(gen[_][12])
            gen[_][12] = random.randint(0, 64)
            gen[_][13] = random.randint(0, 63)
    return gen



old_gen = first_gen

for __ in range(1, 64):
    new_gen = []
    field = [["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""]]
    
    with open('record.json', 'r') as f:
        data = json.load(f)

    elite = elite_selection(old_gen, data, __)
    for _ in range(8):
        operationses = []
        data[str(__)][str(_)] = elite[_]
        for ii in range(12):
            # Add the operation of the elite individual to operationses
            operationses.append(old_gen[elite[_]['par1']][ii])
        # Add the 'num' and 'par1' of the elite individual to operationses
        operationses.append(old_gen[elite[_]['num']][12])
        operationses.append(old_gen[elite[_]['par1']][13])
        new_gen.append(operationses)
    #print(len(new_gen))

    tornament = tornament(old_gen, data, __)
    for _ in range(8,16):
        operationses = []
        data[str(__)][str(_ + 8)] = tornament[_]
        for ii in range(12):
            # Add the operation of the tornament individual to operationses
            operationses.append(old_gen[tornament[_]['par1']][ii])
        # Add the 'num' and 'par1' of the tornament individual to operationses
        operationses.append(old_gen[tornament[_]['num']][12])
        operationses.append(old_gen[tornament[_]['par1']][13])
        new_gen.append(operationses)

    mutation = mutation(new_gen, data, __)
    for _ in range(16, 64):
        data[str(__)][str(_)] = {
            "joint": "mutation",
            "par1": mutation[_][13],
            "num": mutation[_][12],
        }
        new_gen.append(mutation[_])
        
