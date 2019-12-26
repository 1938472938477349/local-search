
import numpy as np


# returns n boxes with max/min length and width
def generate_instance(L, box_n, box_l_min, box_l_max, box_w_min, box_w_max):
    boxes = []

    for i in range(0, box_n):
        l = np.random.randint(box_l_min, box_l_max)
        w = np.random.randint(box_w_min, box_w_max)
        boxes.append((w,l))
    return [L, boxes]



#print(generate_instance(9, 3, 0, 9, 0, 9))


