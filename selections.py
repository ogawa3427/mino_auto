import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import copy
import json

from const import color_map, o, i, l, n, w, x, u, z, f, p, t, v, y, shapes

def elite_selection(gen,times,now_gen_num):
    with open("record.json", "r") as file:
        data = json.load(file)
    score_key_pairs = [(sub_data["score"], key) for key, sub_data in data[str(now_gen_num -1)].items()]
    score_key_pairs.sort(reverse=True)
    top8_key = [key for _, key in score_key_pairs[:8]]

    cp_old_gen = copy.deepcopy(gen)

    return_list = []
    for _ in range(len(top8_key)):
        key = top8_key[_]
        return_list.append(cp_old_gen[int(key)])

        data[str(now_gen_num)][str(_)] = {
            "joint": "elite",
            "par1": int(key),
            "score": data[str(now_gen_num -1)][str(key)]["score"]
        }
    
    with open("record.json", "w") as file:
        json.dump(data, file, indent=4)
    return return_list

def tornament_selection(old_gen,new_gen_num,tor_times):
    with open("record.json", "r") as file:
        data = json.load(file)
    cp_old_gen = copy.deepcopy(old_gen)
    return_list = []
    for _ in range(tor_times):
        samples = random.sample(list(enumerate(cp_old_gen)), 4)
        samples_index = [index for index, sample in samples]
        scores = []
        for index in samples_index:
            scores.append(data[str(new_gen_num -1)][str(index)]["score"])
        max_score_index = samples_index[scores.index(max(scores))]
        return_list.append(cp_old_gen[max_score_index])

        data[str(new_gen_num)][str(_ +8)] = {
            "joint": "tornament",
            "par1": max_score_index,
            "score": max(scores)
        }
    with open("record.json", "w") as file:
        json.dump(data, file, indent=4)
    return return_list

def mutation_selection(old_gen, new_gen_num, mut_times, cmap):
    with open("record.json", "r") as file:
        data = json.load(file)
    global shapes
    cp_old_gen = copy.deepcopy(old_gen)
    for operations in cp_old_gen:
        if len(operations) != 13:
            print(f"lenError: {len(operations)}")
            print("fsefsrehrtsLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLEN")
    return_list = []
    for _ in range(mut_times):
        field = [["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""]]

        candidate = random.sample(cp_old_gen, 1)[0]
        #solo_test(candidate,0,cmap)
        random_choice = random.randint(1,3)
        candipos = random.randint(0,11)

        if random_choice == 1:
            candidate[candipos][1] = random.randint(0,3)
        elif random_choice == 2:
            candidate[candipos][2] = random.choice(["v", "h", "b", "n"])
        elif random_choice == 3:
            pass
        
        shape_name = candidate[candipos][0]
        shape = np.array(shapes[shape_name])
        rotated_shape = np.rot90(shape, candidate[candipos][1])
        xoffset = random.randint(0, 8 - len(rotated_shape))
        yoffset = random.randint(0, 8 - len(rotated_shape[0]))
        position = [xoffset, yoffset]

        candidate[candipos][3] = position

        non_empty_cells = count_non_empty_cells(candidate,cmap)

        return_list.append(candidate)

        data[str(new_gen_num)][str(_ + 16)] = {
            "joint": "mutation",
            "par1": candipos,
            "score": non_empty_cells
        }
        with open("record.json", "w") as file:
            json.dump(data, file, indent=4)
    return return_list
            

def one_cross_selection(old_gen, new_gen_num, one_times):
    with open("record.json", "r") as file:
        data = json.load(file)
    cp_old_gen = copy.deepcopy(old_gen)
    return_list = []
    for operations in cp_old_gen:
        if len(operations) != 13:
            print(f"lenError: {len(operations)}")
            print("LENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLENLEN")

    for _ in range(one_times):
        samples = random.sample(list(enumerate(cp_old_gen)), 2)
        candidate1_index, candidate1 = samples[0]
        candidate2_index, candidate2 = samples[1]

        cross_point = random.randint(0,11)
        outx = []
        outy = []
        alreadyx = []
        alreadyy = []
        for til in range(cross_point):
            alreadyx.append(candidate1[til][0])
            outx.append(candidate1[til])

        candidate1 = [item for item in candidate1 if item[0] not in alreadyx]

        for item in candidate2:
            if item[0] not in alreadyx:
                outx.append(item)
            else:
                outy.append(item)

        candidate2 = [item for item in candidate2 if item[0] not in alreadyx]

        for item in candidate1:
            outy.append(item)

        nonx = count_non_empty_cells(outx,1)
        nony = count_non_empty_cells(outy,1)

        return_list.append(outx)
        return_list.append(outy)

    
        data[str(new_gen_num)][str(_ + 32)] = {
            "joint": "one_cross",
            "par1": candidate1_index,
            "par2": candidate2_index,
            "score": nonx
        }
        data[str(new_gen_num)][str(_ + 32 + one_times)] = {
            "joint": "one_cross",
            "par1": candidate1_index,
            "par2": candidate2_index,
            "score": nony
        }
        with open("record.json", "w") as file:
            json.dump(data, file, indent=4)
    return return_list

def two_cross_selection(old_gen, new_gen_num, two_times):
    with open("record.json", "r") as file:
        data = json.load(file)

    cp_old_gen = copy.deepcopy(old_gen)
    return_list = []
    for _ in range(two_times):
        samples = random.sample(list(enumerate(cp_old_gen)), 2)
        candidate1_index, candidate1 = samples[0]
        candidate2_index, candidate2 = samples[1]

        cross_point1 = random.randint(0, len(candidate1) - 1)
        cross_point2 = random.randint(cross_point1, len(candidate1))

        # Divide candidate1 into three parts
        part1 = candidate1[:cross_point1]
        part2 = candidate1[cross_point1:cross_point2]
        part3 = candidate1[cross_point2:]

        # Create outx by combining part1, part2 from candidate2, and part3
        outx = part1 + [item for item in candidate2 if item[0] in [x[0] for x in part2]] + part3

        # Create outy by combining part1, part2 from candidate1, and part3
        outy = part1 + part2 + [item for item in candidate2 if item[0] in [x[0] for x in part3]]

        nonx = count_non_empty_cells(outx,1)
        nony = count_non_empty_cells(outy,1)

        return_list.append(outx)
        return_list.append(outy)

        data[str(new_gen_num)][str(_ + 40)] = {
            "joint": "two_cross",
            "par1": candidate1_index,
            "par2": candidate2_index,
            "score": nonx
        }
        data[str(new_gen_num)][str(_ + 40 + two_times)] = {
            "joint": "two_cross",
            "par1": candidate1_index,
            "par2": candidate2_index,
            "score": nony
        }
    with open("record.json", "w") as file:
        json.dump(data, file, indent=4)
    return return_list

def uni_cross_selection(old_gen, new_gen_num, uni_times):
    with open("record.json", "r") as file:
        data = json.load(file)
    cp_old_gen = copy.deepcopy(old_gen)
    return_list = []
    for _ in range(uni_times):
        samples = random.sample(list(enumerate(cp_old_gen)), 2)
        candidate0_index, candidate0 = samples[0]
        candidate1_index, candidate1 = samples[1]
        outx = []
        outy = []
        name_list = ["o", "i", "l", "n", "w", "x", "u", "z", "f", "p", "t", "v", "y"]

        for name in name_list:
            if random.choice([True, False]):
                outx.append(next((item for item in candidate0 if item[0] == name), None))
                outy.append(next((item for item in candidate1 if item[0] == name), None))
            else:
                outx.append(next((item for item in candidate1 if item[0] == name), None))
                outy.append(next((item for item in candidate0 if item[0] == name), None))

        return_list.append(outx)
        return_list.append(outy)

        nonx = count_non_empty_cells(outx,1)
        nony = count_non_empty_cells(outy,1)

        data[str(new_gen_num)][str(_ + 48)] = {
            "joint": "uni_cross",
            "par1": candidate0_index,
            "par2": candidate1_index,
            "score": nonx
        }
        data[str(new_gen_num)][str(_ + 48 + uni_times)] = {
            "joint": "uni_cross",
            "par1": candidate0_index,
            "par2": candidate1_index,
            "score": nony
        }
    with open("record.json", "w") as file:
        json.dump(data, file, indent=4)
    return return_list



def count_non_empty_cells(operations,cmap):
    global shapes
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
        shape_name, rotation, flip, position = operation

        shape = np.array(shapes[shape_name])

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
