import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import copy
import json

from const import color_map, o, i, l, n, w, x, u, z, f, p, t, v, y, shapes
from selections import elite_selection, tornament_selection, mutation_selection, one_cross_selection, two_cross_selection, uni_cross_selection, count_non_empty_cells
from earth import create_first_generation, output_images, make_next_cycle

oldgen = create_first_generation()
output_images(oldgen, 0)


for saikuru in range(63):
    newgen = make_next_cycle(oldgen, saikuru + 1)
    output_images(newgen, saikuru + 1)
    oldgen = newgen
    print(f"cycle: {saikuru + 1}")
    
    