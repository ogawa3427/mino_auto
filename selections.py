import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import copy
import json

from const import color_map, o, i, l, n, w, x, u, z, f, p, t, v, y, shapes

def elite_selection(gen,times):
    gen.sort(key=lambda x: x[13], reverse=True)
    output = [{} for _ in range(times)]
    for _ in range(times):
        output[_] = {
            "joint": "elite",
            "par1": gen[_][12],
            "num": gen[_][13],
        }
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


def mutation_selection(old_gen, data, new_gen_num, mut_times, cmap):
    return_list = []
    output = [{} for _ in range(mut_times)]
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
        #solo_test(candidate,0,cmap)
        random_choice = random.randint(1,3)

        if random_choice == 1:
            candipos = random.randint(0,11)
            candidate[candipos][1] = random.randint(0,3)
            rotation = candidate[candipos][1]
            shape = candidate[candipos][0]
            shape = np.rot90(shape, rotation)
            print("21111111111111111111111111111x")
        elif random_choice == 2:
            candipos = random.randint(0,11)
            candidate[candipos][2] = random.choice(["v", "h", "b", "n"])
            shape = candidate[candipos][0]
            print("222222222222222222222222")
        elif random_choice == 3:
            candipos = random.randint(0,11)
            shape = candidate[candipos][0]
            max_xpos = len(field) - len(shape)
            max_ypos = len(field[0]) - len(shape[0])
            xpos = random.randint(0, max_xpos)
            ypos = random.randint(0, max_ypos)
            candidate[candipos][3] = [xpos,ypos]
            print("333333333333333333333333333333")
        if random_choice != 3:
            try:
                for ii in range(len(shape)):
                    for jj in range(len(shape[0])):
                        if shape[ii][jj] != "" and field[ii + candidate[candipos][3][0]][jj + candidate[candipos][3][1]] != "":
                            field[ii + candidate[candipos][3][0]][jj + candidate[candipos][3][1]] = "E"
                        elif shape[ii][jj] != "":
                            field[ii + candidate[candipos][3][0]][jj + candidate[candipos][3][1]] = shape[ii][jj]
            except:
                print("error")
                max_xpos = len(field) - len(shape)
                max_ypos = len(field[0]) - len(shape[0])
                xpos = random.randint(0, max_xpos)
                ypos = random.randint(0, max_ypos)
                candidate[candipos][3] = [xpos,ypos]

        non_empty_cells = count_non_empty_cells(candidate,cmap)

        candidate.append(_)
        candidate.append(non_empty_cells)

        return_list.append(candidate)

        output[_] = {
            "joint": "mutation",
            "par1": candidate[12],
            "num": candidate[13]
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



def count_non_empty_cells(operations,cmap):
    field = [["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""]]
    non_empty_cells = 0
    #solo_test(operations,0,cmap)
    for operation in operations:
        # operationが整数の場合はスキップ
        # operationが期待する形状でなければスキップ
        if not isinstance(operation, list) or len(operation) != 4:
            continue
        shape, rotation, flip, position = operation

        # shapeがnumpy配列でない、または1次元未満の場合はスキップ
        if not isinstance(shape, np.ndarray) or shape.ndim < 2:
            continue

        print(f"shape: {shape}")

        if flip == "v":
            shape = np.flipud(shape)
        elif flip == "h":
            shape = np.fliplr(shape)
        elif flip == "b":
            shape = np.flipud(shape)
            shape = np.fliplr(shape)
        elif flip == "n":
            pass
        print(f"rotation: {rotation}")
        shape = np.rot90(shape, rotation)

        for ii in range(len(shape)):
            for jj in range(len(shape[0])):
                print(f"position: {position}")
                print(f"ii: {ii}, jj: {jj}")
                print(f"ii + position[0]: {ii + position[0]}, jj + position[1]: {jj + position[1]}")
                if shape[ii][jj] != "" and field[ii + position[0]][jj + position[1]] != "":
                    field[ii + position[0]][jj + position[1]] = "E"
                elif shape[ii][jj] != "":
                    field[ii + position[0]][jj + position[1]] = shape[ii][jj]
                    non_empty_cells += 1
    return non_empty_cells


            
def solo_test(operations, num, cmap):
    rows = 4
    cols = (len(operations) + rows - 1) // rows  # Round up division
    fig, axs = plt.subplots(rows, cols, figsize=(cols*5, rows*5))
    axs = axs.ravel()  # Flatten the array for easy indexing
    field = [["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""]]
    for index, operation in enumerate(operations):
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

        field_img = [[color_map[item] for item in row] for row in field]
        axs[index].imshow(field_img, cmap=cmap, vmin=0, vmax=155)
        axs[index].axis('off')
        axs[index].set_title(f'Operation {num}_{index}')

    plt.tight_layout()
    plt.show()
