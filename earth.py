import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import copy
import json

from const import color_map, o, i, l, n, w, x, u, z, f, p, t, v, y
from selections import elite_selection, tornament_selection, mutation_selection, one_cross, two_cross, uni_cross



color_list = list(color_map.values())
cmap = mcolors.LinearSegmentedColormap.from_list('custom_map', color_list)

error_num = 0

def output_images(operationses,num):
    for index, operations in enumerate(operationses):
        field = [["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""]]
        for operation in operations:
            # operationが整数の場合はスキップ
            if isinstance(operation, int):
                continue
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

        field = [[color_map[item] for item in row] for row in field]
        plt.imshow(field, cmap=cmap, vmin=0, vmax=255)
        plt.axis('off')  # 目盛りを削除
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)  # 余白を削除
        #plt.savefig(f'{num}_{index}.png', bbox_inches='tight', pad_inches=0)  # 画像を保存、余白を削除

def create_first_generation():
    operationses = []
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
        operations = []
        non_empty_cells = 0
        for _ in range(12):
            shape = np.array(random.choice(shapes))

            shapes.remove(shape.tolist())  # shapeをリストに戻してから削除

            rotation = random.randint(0, 3)
            flip = random.choice(["v", "h", "b", "n"])
            rotated_shape = np.rot90(shape, rotation)

            posx = random.randint(0, 7 - len(rotated_shape))
            posy = random.randint(0, 7 - len(rotated_shape[0]))
            position = [posx, posy]
            operation = [shape, rotation, flip, position]
            operations.append(operation)

            # Write the shape to the field
            for ii in range(len(rotated_shape)):
                for jj in range(len(rotated_shape[0])):
                    if rotated_shape[ii][jj] != "" and field[ii + position[0]][jj + position[1]] != "":
                        field[ii + position[0]][jj + position[1]] = "E"
                    elif rotated_shape[ii][jj] != "":
                        field[ii + position[0]][jj + position[1]] = rotated_shape[ii][jj]
                        non_empty_cells += 1
        operations.append(_) #par1は12
        operations.append(non_empty_cells) #スコアは13
        operationses.append(operations)
        

    return operationses




def make_next_cycle(old_gen, data, new_gen_num):
    with open('record.json', 'w') as file:
        json.dump(data, file, indent=4)
    new_gen = []

    elite_times = 8
    elite = elite_selection(old_gen,elite_times)
    length = len(new_gen)
    for _ in range(elite_times):
        data[str(new_gen_num)][str(length + _)] = elite[_]
        new_gen.append(old_gen[elite[_]['par1']])
        new_gen[length + _][12] = length + _

    tor_times = 8
    tornament, tornament_list, data = tornament_selection(old_gen, data, new_gen_num, tor_times)
    length = len(new_gen)
    for _ in range(tor_times):
        data[str(new_gen_num)][str(length + _)] = tornament[_]
        new_gen.append(tornament_list[_])
        new_gen[length + _][12] = length + _

    mut_times = 16
    mutation, mutation_list, data = mutation_selection(old_gen, data, new_gen_num, mut_times, cmap)
    length = len(new_gen)
    for _ in range(mut_times):
        data[str(new_gen_num)][str(length + _)] = mutation[_]
        new_gen.append(mutation_list[_])
        new_gen[length + _][12] = length + _

    one_times = 4
    one_cross, one_cross_list, data = one_cross(old_gen, data, new_gen_num, one_times)
    length = len(new_gen)
    for _ in range(one_times):
        data[str(new_gen_num)][str(length + _)] = one_cross[_]
        new_gen.append(one_cross_list[_])
        new_gen[length + _][12] = length + _

    two_times = 4
    two_cross, two_cross_list, data = two_cross(old_gen, data, new_gen_num, two_times)
    length = len(new_gen)
    for _ in range(two_times):
        data[str(new_gen_num)][str(length + _)] = two_cross[_]
        new_gen.append(two_cross_list[_])
        new_gen[length + _][12] = length + _

    uni_times = 8
    uni_cross, uni_cross_list, data = uni_cross(old_gen, data, new_gen_num, uni_times)
    length = len(new_gen)
    for _ in range(uni_times):
        data[str(new_gen_num)][str(length + _)] = uni_cross[_]
        new_gen.append(uni_cross_list[_])
        new_gen[length + _][12] = length + _

    with open('record.json', 'w') as file:
        json.dump(data, file, indent=4)


    return new_gen, data



def ndarray_to_list(ndarray):
    if isinstance(ndarray, np.ndarray):
        return ndarray_to_list(ndarray.tolist())
    elif isinstance(ndarray, list):
        return [ndarray_to_list(element) for element in ndarray]
    else:
        return ndarray
with open('record.json', 'r') as file:
    data = json.load(file)
first_gen = create_first_generation()

output_images(first_gen,0)
with open('dumping.json', 'w') as file:
    json.dump(ndarray_to_list(first_gen), file, indent=4)

new_gen, data = make_next_cycle(first_gen, data, 1)
