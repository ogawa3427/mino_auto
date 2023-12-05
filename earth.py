import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import copy
import json

o = [["o", "o"], ["o", "o"]]
i = [["i"], ["i"], ["i"], ["i"], ["i"]]
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
            shape_effective_height = max(ii for ii, row in enumerate(rotated_shape) if any(cell != "" for cell in row)) + 1
            shape_effective_width = max(jj for jj in range(len(rotated_shape[0])) if any(rotated_shape[ii][jj] != "" for ii in range(len(rotated_shape)))) + 1
            position = [random.randint(0, 8 - shape_effective_height), random.randint(0, 8 - shape_effective_width)]

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



def count_non_empty_cells(operations):
    field = [["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""]]
    non_empty_cells = 0
    for operation in operations:
        # operationが整数の場合はスキップ
        print('=====')
        print(operation)
        print('=====')
        # operationが期待する形状でなければスキップ
        if not isinstance(operation, list) or len(operation) != 4:
            continue
        shape, rotation, flip, position = operation
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
                    non_empty_cells += 1
    return non_empty_cells

def elite_selection(gen,times):
    gen.sort(key=lambda x: x[13], reverse=True)
    output = [{} for _ in range(times)]
    for _ in range(times):
        output[_] = {
            "joint": "elite",
            "par1": gen[_][12],
            "num": gen[_][13],
        }
        #print(output[_])
    return output

def tornament_selection(old_gen,data,new_gen_num,tor_times):
    return_list = []
    output = [{} for _ in range(tor_times)]
    for _ in range(tor_times):
        candidates = random.sample(old_gen, 4)
        best_candidate = max(candidates, key=lambda x: x[13])
        return_list.append(best_candidate)

        output[_] = {
            "joint": "tornament",
            "par1": return_list[_][12],
            "num": return_list[_][13]
        }
    return output, return_list, data


def mutation_selection(old_gen, data, new_gen_num, mut_times):
    return_list = [{} for _ in range(mut_times)]
    for _ in range(mut_times):
        field = [["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""]]


        candidate = random.sample(old_gen, 1)[0]

        for ___ in range(12):
            operation_index = random.randint(0,11)
        # 選択した操作が整数であればスキップ
        while isinstance(candidate[operation_index], int):
            operation_index = random.randint(0,11)

        random_choice = random.randint(0,3)
        if random_choice == 0:
            repx = candidate[random.randint(0,11)][0]
            repy = candidate[random.randint(0,11)][1]
            candidate[random.randint(0,11)][0] = repy
            candidate[random.randint(0,11)][1] = repx
        elif random_choice == 1:
            candidate[random.randint(0,11)][1] = random.randint(0,3)
            rotation = random.randint(0, 3)
            rotated_shape = np.rot90(candidate[random.randint(0,11)][0], rotation)
            shape_effective_height = max(ii for ii, row in enumerate(rotated_shape) if any(cell != "" for cell in row)) + 1
            shape_effective_width = max(jj for jj in range(len(rotated_shape[0])) if any(rotated_shape[ii][jj] != "" for ii in range(len(rotated_shape)))) + 1
            position = [random.randint(0, 8 - shape_effective_height), random.randint(0, 8 - shape_effective_width)]
            candidate[random.randint(0,11)][3] = position
            candidate[random.randint(0,11)][1] = rotation
        elif random_choice == 2:
            candidate[random.randint(0,11)][2] = random.choice(["v", "h", "b", "n"])
        elif random_choice == 3:
            shape = candidate[random.randint(0,11)][0]
            shape_effective_height = max(ii for ii, row in enumerate(shape) if any(cell != "" for cell in row)) + 1
            shape_effective_width = max(jj for jj in range(len(shape[0])) if any(shape[ii][jj] != "" for ii in range(len(shape)))) + 1
            position = [random.randint(0, 8 - shape_effective_height), random.randint(0, 8 - shape_effective_width)]
            candidate[random.randint(0,11)][3] = position

        non_empty_cells = count_non_empty_cells(candidate)

        candidate[12] = _
        candidate[13] = non_empty_cells

        return_list.append(candidate)

    for _ in range(mut_times):
        output[_] = {
            "joint": "mutation",
            "par1": return_list[_][12],
            "num": return_list[_][13]
        }
    return output, return_list, data

def one_cross(old_gen, data, new_gen_num, one_times):
    return_list = []
    for _ in range(one_times):
        candidates = random.sample(old_gen, 2)
        candidate1 = candidates[0]
        candidate2 = candidates[1]
        cross_point = random.randint(0,11)
        outx = []
        outy = []
        alreadyx = []
        alreadyy = []
        for til in range(cross_point):
            outx.append(candidate1[til])
            alreadyx.append(candidate1[til][0])
        for item in candidate2:
            if item[0] not in alreadyx:
                outx.append(item)
        for til in range(cross_point):
            outy.append(candidate2[til])
            alreadyy.append(candidate2[til][0])
        for item in candidate1:
            if item[0] not in alreadyy:
                outy.append(item)
        return_list.append(outx)
        return_list.append(outy)

        nonx = count_non_empty_cells(outx)
        nony = count_non_empty_cells(outy)
    
        output[_] = {
            "joint": "one_cross",
            "par1": candidate1[12],
            "par2": candidate2[12],
            "num": nonx
        }
        output[_ + one_times] = {
            "joint": "one_cross",
            "par1": candidate1[12],
            "par2": candidate2[12],
            "num": nony
        }
    return output, return_list, data

def two_cross(old_gen, data, new_gen_num, two_times):
    return_list = []
    for _ in range(two_times):
        field = [["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""]]
        
        candidates = random.sample(old_gen, 2)
        candidate1 = candidates[0]
        candidate2 = candidates[1]
        cross_point1 = random.randint(0,10)
        cross_point2 = random.randint(cross_point1+1,11)
        outx = []
        outy = []
        alreadyx = []
        alreadyy = []

        # 1つ目の交叉点までの部分を追加
        for til in range(cross_point1):
            outx.append(candidate1[til])
            alreadyx.append(candidate1[til][0])
            outy.append(candidate2[til])
            alreadyy.append(candidate2[til][0])

        # 1つ目と2つ目の交叉点の間の部分を交換して追加
        for til in range(cross_point1, cross_point2):
            outx.append(candidate2[til])
            alreadyx.append(candidate2[til][0])
            outy.append(candidate1[til])
            alreadyy.append(candidate1[til][0])

        # 2つ目の交叉点以降の部分を追加
        for til in range(cross_point2, len(candidate1)):
            outx.append(candidate1[til])
            alreadyx.append(candidate1[til][0])
            outy.append(candidate2[til])
            alreadyy.append(candidate2[til][0])

        return_list.append(outx)
        return_list.append(outy)

        non_empty_cells = 0
        for __ in range(12):
            for ii in range(len(outx[__][0])):
                for jj in range(len(outx[__][0][0])):
                    if outx[__][0][ii][jj] != "" and field[ii + outx[__][3][0]][jj + outx[__][3][1]] != "":
                        field[ii + outx[__][3][0]][jj + outx[__][3][1]] = "E"
                    elif outx[__][0][ii][jj] != "":
                        field[ii + outx[__][3][0]][jj + outx[__][3][1]] = outx[__][0][ii][jj]
                        non_empty_cells += 1
        nonx = non_empty_cells
        for __ in range(12):
            for ii in range(len(outy[__][0])):
                for jj in range(len(outy[__][0][0])):
                    if outy[__][0][ii][jj] != "" and field[ii + outy[__][3][0]][jj + outy[__][3][1]] != "":
                        field[ii + outy[__][3][0]][jj + outy[__][3][1]] = "E"
                    elif outy[__][0][ii][jj] != "":
                        field[ii + outy[__][3][0]][jj + outy[__][3][1]] = outy[__][0][ii][jj]
                        non_empty_cells += 1
        nony = non_empty_cells - nonx

        output[_] = {
            "joint": "two_cross",
            "par1": candidate1[12],
            "par2": candidate2[12],
            "num": nonx
        }
        output[_ + two_times] = {
            "joint": "two_cross",
            "par1": candidate1[12],
            "par2": candidate2[12],
            "num": nony
        }
    return output, return_list, data

def uni_cross(old_gen, data, new_gen_num, uni_times):
    return_list = []
    for _ in range(uni_times):
        candidates = random.sample(old_gen, 2)
        candidate0 = candidates[0]
        candidate1 = candidates[1]
        outx = []
        outy = []
        name_list = [o, i, l, n, w, x, u, z, f, p, t, v, y]

        for name in name_list:
            if random.choice([True, False]):
                outx.append(next((item for item in candidate0 if item[0] == name), None))
                outy.append(next((item for item in candidate1 if item[0] == name), None))
            else:
                outx.append(next((item for item in candidate1 if item[0] == name), None))
                outy.append(next((item for item in candidate0 if item[0] == name), None))

        return_list.append(outx)
        return_list.append(outy)

        nonx = count_non_empty_cells(outx)
        nony = count_non_empty_cells(outy)

        output[_] = {
            "joint": "uni_cross",
            "par1": candidate0[12],
            "par2": candidate1[12],
            "num": nonx
        }
        output[_ + uni_times] = {
            "joint": "uni_cross",
            "par1": candidate0[12],
            "par2": candidate1[12],
            "num": nony
        }
    return output, return_list, data
            

def make_next_cycle(old_gen, data, new_gen_num):
    with open('record.json', 'w') as file:
        json.dump(data, file, indent=4)
    new_gen = []

    elite_times = 8
    elite = elite_selection(old_gen,elite_times)
    length = len(new_gen)
    for _ in range(elite_times):
        data[str(new_gen_num)][str(length + _)] = elite[_]
        #print(elite[_]['par1'])
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
    mutation, mutation_list, data = mutation_selection(old_gen, data, new_gen_num, mut_times)
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

with open('record.json', 'r') as file:
    data = json.load(file)
first_gen = create_first_generation()
#print(first_gen[20])
#print(first_gen[20][12])
output_images(first_gen,0)
second_gen = make_next_cycle(first_gen, data, "1")
output_images(second_gen,1)

        
