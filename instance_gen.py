import random

# returns n boxes with max/min height and width
def generate_instance(L, box_n, box_l_min, box_l_max, box_w_min, box_w_max):
    boxes = []
    for i in range(0, box_n):
        h = random.randint(box_l_min, box_l_max)
        w = random.randint(box_w_min, box_w_max)
        boxes.append((w,h))
    return [L, boxes]

