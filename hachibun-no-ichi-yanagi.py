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

def choose_shape(shapes):
    shape = random.choice(shapes)
    shapes.remove(shape)
    return shape, shapes

def apply_flip_and_rotation(shape, flip, rotation):
    if flip == "horizontal":
        shape = shape[::-1]
    elif flip == "vertical":
        shape = [list(x) for x in zip(*shape[::-1])]
    elif flip == "both":
        shape = [list(x) for x in zip(*shape[::-1])]
        shape = shape[::-1]

    for _ in range(rotation // 90):
        shape = [list(x) for x in zip(*shape[::-1])]
    return shape

def place_shape_on_field(field, shape, start_pos_x, start_pos_y):
    for shape_x in range(len(shape[0])):  
        for shape_y in range(len(shape)):  
            if start_pos_y + shape_y < len(field) and start_pos_x + shape_x < len(field[0]):
                if field[start_pos_y + shape_y][start_pos_x + shape_x] != "" and shape[shape_y][shape_x] != "":
                    field[start_pos_y + shape_y][start_pos_x + shape_x] = "E" 
                else:
                    field[start_pos_y + shape_y][start_pos_x + shape_x] = shape[shape_y][shape_x]
    return field

def create_operation(shape, rotation, flip, start_pos_x, start_pos_y):
    operation = {
        "shape_name": shape,
        "rotation": rotation,
        "flip": flip,
        "position": (start_pos_x, start_pos_y),
        "parents": []  # This line was added
    }
    return operation

# 各操作に一意のIDを割り当てる
id_counter = 0
for operations in operationses:
    for operation in operations:
        operation['id'] = id_counter
        id_counter += 1

# 交叉や突然変異の際に、新たな操作がどの操作から派生したかを記録する
def crossover(op1, op2):
    global id_counter  # この行を追加
    crossover_point = len(op1) // 2
    new_op1 = op1[:crossover_point] + op2[crossover_point:]
    new_op2 = op2[:crossover_point] + op1[crossover_point:]
    for operation in new_op1[crossover_point:]:
        operation['id'] = id_counter
        if 'id' in op1[0] and 'id' in op2[0]:  # This line was added
            operation['parents'] = [op1[0]['id'], op2[0]['id']]
        id_counter += 1
    for operation in new_op2[crossover_point:]:
        operation['id'] = id_counter
        if 'id' in op1[0] and 'id' in op2[0]:  # This line was added
            operation['parents'] = [op1[0]['id'], op2[0]['id']]
        id_counter += 1
    return new_op1, new_op2

def mutate(op):
    global id_counter  # 追加
    idx = random.choice(range(len(op)))
    op[idx]['rotation'] = random.choice([0, 90, 180, 270])
    op[idx]['flip'] = random.choice(["none", "horizontal", "vertical", "both"])
    op[idx]['position'] = (random.randint(0, 7), random.randint(0, 7))
    op[idx]['id'] = id_counter
    op[idx]['parents'] = [op[idx]['id']]
    id_counter += 1
    return op

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
        shape, shapes = choose_shape(shapes)
        rotation = random.choice([0, 90, 180, 270])
        flip = random.choice(["none", "horizontal", "vertical", "both"])
        start_pos_x = random.randint(0, len(field[0]) - len(shape[0]))
        start_pos_y = random.randint(0, len(field) - len(shape))
        shape = apply_flip_and_rotation(shape, flip, rotation)
        field = place_shape_on_field(field, shape, start_pos_x, start_pos_y)
        operation = create_operation(shape, rotation, flip, start_pos_x, start_pos_y)
        operations.append(operation)
        non_empty_cells = sum([1 for row in field for cell in row if cell != "" and cell != "E"])
    operationses.append(operations)
    non_empty_cells_list.append(non_empty_cells)
    field_array = np.array([[color_map[item] for item in row] for row in field])


top8_indices = sorted(range(len(non_empty_cells_list)), key=lambda i: non_empty_cells_list[i])[-8:]


top8_operations = [operationses[i] for i in top8_indices]

selected_operations = []

top8_indices = sorted(range(len(non_empty_cells_list)), key=lambda i: non_empty_cells_list[i])[-8:]
selected_operations.extend([operationses[i] for i in top8_indices])

remaining_indices = sorted(range(len(non_empty_cells_list)), key=lambda i: non_empty_cells_list[i])[:-8]
for _ in range(2):  
    selected_indices = random.sample(remaining_indices, 4)
    selected_operations.extend([operationses[i] for i in selected_indices])

def crossover(op1, op2):
    global id_counter  # この行を追加
    crossover_point = len(op1) // 2
    new_op1 = op1[:crossover_point] + op2[crossover_point:]
    new_op2 = op2[:crossover_point] + op1[crossover_point:]
    for operation in new_op1[crossover_point:]:
        operation['id'] = id_counter
        if 'id' in op1[0] and 'id' in op2[0]:  # This line was added
            operation['parents'] = [op1[0]['id'], op2[0]['id']]
        id_counter += 1
    for operation in new_op2[crossover_point:]:
        operation['id'] = id_counter
        if 'id' in op1[0] and 'id' in op2[0]:  # This line was added
            operation['parents'] = [op1[0]['id'], op2[0]['id']]
        id_counter += 1
    return new_op1, new_op2

new_operations = []
for _ in range(8):
    idx1, idx2 = random.sample(range(len(operationses)), 2)
    op1 = copy.deepcopy(operationses[idx1])
    op2 = copy.deepcopy(operationses[idx2])
    new_op1, new_op2 = crossover(op1, op2)
    new_operations.extend([new_op1, new_op2])

def two_point_crossover(op1, op2):
    size = min(len(op1), len(op2))
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    new_op1 = op1[:cxpoint1] + op2[cxpoint1:cxpoint2] + op1[cxpoint2:]
    new_op2 = op2[:cxpoint1] + op1[cxpoint1:cxpoint2] + op2[cxpoint2:]
    return new_op1, new_op2

new_operations_two_point = []
for _ in range(8):
    idx1, idx2 = random.sample(range(len(operationses)), 2)
    op1 = copy.deepcopy(operationses[idx1])
    op2 = copy.deepcopy(operationses[idx2])
    new_op1, new_op2 = two_point_crossover(op1, op2)
    new_operations_two_point.extend([new_op1, new_op2])

def mutate(op):
    global id_counter  # 追加
    idx = random.choice(range(len(op)))
    op[idx]['rotation'] = random.choice([0, 90, 180, 270])
    op[idx]['flip'] = random.choice(["none", "horizontal", "vertical", "both"])
    op[idx]['position'] = (random.randint(0, 7), random.randint(0, 7))
    op[idx]['id'] = id_counter
    op[idx]['parents'] = [op[idx]['id']]
    id_counter += 1
    return op

for _ in range(16):
    idx = random.choice(range(len(operationses)))
    op = copy.deepcopy(operationses[idx])
    mutated_op = mutate(op)
    new_operations.append(mutated_op)

all_operations = new_operations + new_operations_two_point + [mutated_op]

# サブプロットする操作のリストを初期化
subplot_operations = []

for generation in range(64):
    new_generation = []

    top8_indices = sorted(range(len(all_operations)), key=lambda i: non_empty_cells_list[i])[-8:]
    new_generation.extend([all_operations[i] for i in top8_indices])

    remaining_indices = sorted(range(len(all_operations)), key=lambda i: non_empty_cells_list[i])[:-8]
    for _ in range(2):  
        selected_indices = random.sample(remaining_indices, 4)
        new_generation.extend([all_operations[i] for i in selected_indices])

    for _ in range(8):
        idx1, idx2 = random.sample(range(len(all_operations)), 2)
        op1 = copy.deepcopy(all_operations[idx1])
        op2 = copy.deepcopy(all_operations[idx2])
        new_op1, new_op2 = crossover(op1, op2)
        new_generation.extend([new_op1, new_op2])

    for _ in range(8):
        idx1, idx2 = random.sample(range(len(all_operations)), 2)
        op1 = copy.deepcopy(all_operations[idx1])
        op2 = copy.deepcopy(all_operations[idx2])
        new_op1, new_op2 = two_point_crossover(op1, op2)
        new_generation.extend([new_op1, new_op2])

    for _ in range(16):
        idx = random.choice(range(len(all_operations)))
        op = copy.deepcopy(all_operations[idx])
        mutated_op = mutate(op)
        new_generation.append(mutated_op)

    all_operations = new_generation

    # 10世代ごとに操作をサブプロットリストに追加
    if (generation + 1) % 1 == 0:
        top_operation = sorted(all_operations, key=lambda op: sum([1 for operation in op if operation['shape_name'] != "" and operation['shape_name'] != "E"]))[-1]
        subplot_operations.append(top_operation)
        print(f"{generation + 1}")
    

# 640世代が完了したら64個の操作をサブプロット
fig, axs = plt.subplots(8, 8, figsize=(15, 15))
for i, operation in enumerate(subplot_operations):
    # フィールドを初期化
    field = [["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""]]
    # 操作をフィールドに適用
    for op in operation:
        shape = apply_flip_and_rotation(op['shape_name'], op['flip'], op['rotation'])
        field = place_shape_on_field(field, shape, op['position'][0], op['position'][1])
    # フィールドを配列に変換
    field_array = np.array([[color_map[item] for item in row] for row in field])
    # サブプロット
    axs[i // 8, i % 8].imshow(field_array)
    axs[i // 8, i % 8].set_title(f"Gen {(i+1)*1}: " + str(sum([1 for row in field for cell in row if cell != "" and cell != "E"])))
plt.show()

# 最終的な解決策を特定
final_solution = sorted(all_operations, key=lambda op: sum([1 for operation in op if operation['shape_name'] != "" and operation['shape_name'] != "E"]))[-1]

# 最終的な解決策の一部となる操作のIDをリストアップ
final_solution_ids = [op['id'] for op in final_solution]

# グラフを初期化
G = nx.DiGraph()

# 最終的な解決策の一部となる操作だけをグラフに追加
for operation in all_operations:
    if 'id' in operation[0] and operation[0]['id'] in final_solution_ids:
        G.add_node(operation[0]['id'])
        for parent_id in operation[0]['parents']:
            G.add_edge(parent_id, operation[0]['id'])

# グラフを描画
nx.draw(G, with_labels=True)
plt.show()