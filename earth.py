import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import copy
import json

from const import color_map, o, i, l, n, w, x, u, z, f, p, t, v, y, shapes
from selections import elite_selection, tornament_selection, mutation_selection, one_cross_selection, two_cross_selection, uni_cross_selection, count_non_empty_cells


color_list = list(color_map.values())
cmap = mcolors.LinearSegmentedColormap.from_list('custom_map', color_list)

error_num = 0

def output_images(operationses,num):
    global shapes
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
            shape_name, rotation, flip, position = operation
            if flip == "v":
                shape = np.flipud(shapes[shape_name])
            elif flip == "h":
                shape = np.fliplr(shapes[shape_name])
            elif flip == "b":
                shape = np.flipud(shapes[shape_name])
                shape = np.fliplr(shape)
            elif flip == "n":
                shape = np.array(shapes[shape_name])
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
        plt.savefig(f'{num}_{index}.png', bbox_inches='tight', pad_inches=0)  # 画像を保存、余白を削除

def create_first_generation():
    global shapes
    with open('record.json', 'r') as file:
        data = json.load(file)
    operationses = []
    for __ in range(64):
        keys = ["o", "i", "l", "n", "w", "x", "u", "z", "f", "p", "t", "v", "y"]
        field = [["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""]]
        operations = []
        while len(keys) > 0:
            shape_name = random.choice(keys)
            shape = np.array(shapes[shape_name])

            keys.remove(shape_name)

            rotation = random.randint(0, 3)
            flip = random.choice(["v", "h", "b", "n"])
            rotated_shape = np.rot90(shape, rotation)

            posx = random.randint(0, 8 - len(rotated_shape))
            posy = random.randint(0, 8 - len(rotated_shape[0]))
            position = [posx, posy]
            operation = [shape_name, rotation, flip, position]
            operations.append(operation)

            # Write the shape to the field
        non_empty_cells = count_non_empty_cells(operations,1)
        data["0"][str(__)]["score"] = non_empty_cells
        operationses.append(operations)
    with open('record.json', 'w') as file:
        json.dump(data, file, indent=4)
    return operationses




def make_next_cycle(old_gen, new_gen_num):

    new_gen = [ [] for num_operations in range(64)]

    elite_times = 8
    elite = elite_selection(old_gen,elite_times,new_gen_num)
    length = 0
    for _ in range(elite_times):
        new_gen[length + _] = elite[_]
    length += elite_times

    tor_times = 8
    tornament = tornament_selection(old_gen, new_gen_num, tor_times)
    for _ in range(tor_times):
        new_gen[length + _] = tornament[_]
    length += tor_times

    mut_times = 16
    mutation = mutation_selection(old_gen, new_gen_num, mut_times, cmap)
    for _ in range(mut_times):
        new_gen[length + _] = mutation[_]
    length += mut_times

    one_times = 4
    one_cross = one_cross_selection(old_gen, new_gen_num, one_times)
    for _ in range(one_times*2):
        new_gen[length + _] = one_cross[_]
    length += one_times*2


    two_times = 4
    two_cross = two_cross_selection(old_gen, new_gen_num, two_times)
    for _ in range(two_times*2):
        new_gen[length + _] = two_cross[_]
    length += two_times*2

    uni_times = 8
    uni_cross = uni_cross_selection(old_gen, new_gen_num, uni_times)
    for _ in range(uni_times*2):
        new_gen[length + _] = uni_cross[_]
    return new_gen

def ndarray_to_list(ndarray):
    if isinstance(ndarray, np.ndarray):
        return ndarray_to_list(ndarray.tolist())
    elif isinstance(ndarray, list):
        return [ndarray_to_list(element) for element in ndarray]
    else:
        return ndarray
    
def gen_log(operationses):
    global shapes
    log = {}
    log["num_opess"] = len(operationses)
    for no, operations in enumerate(operationses):
        log[no] = {}
        for nono, operation in enumerate(operations):
            _ = operation
            log[no][nono] = _
    with open('log.json', 'w') as file:
        json.dump(log, file, indent=4)

def indiv_log(operations):
    log = {}
    log["num_ops"] = len(operations)
    for no, operation in enumerate(operations):
        if isinstance(operation, int):
            _ = operation
        else:
            _ = operation
        log[no] = _
    with open('log.json', 'w') as file:
        json.dump(log, file, indent=4)
        
    
