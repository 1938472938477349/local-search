import instance_gen
import copy

# HOW A STATE/SOLUTION IS ENCODED
# [boxsize, boxes]
# boxes = [box1, box2, ...]
# box1 = [rect1, rect2, ...]
# rect1 = [x, y, w, h]

# the trivial solution would be to put each rectangle into its own box
def trivia_sol(input):
    boxes = []
    sol = [input[0], boxes]
    for i in input[1]:
        x = 0
        y = 0
        sol[1].append([[x, y, i[0], i[1]]])
    return sol

# check if 2 rects collide with each other
def isCollision(rect1, rect2):
    return rect1[0] < rect2[0] + rect2[2] and rect1[0] + rect1[2] > rect2[0] and rect1[1] < rect2[1] + rect2[3] and rect1[1] + rect1[3] > rect2[1]

# check if a rect is out of bound
def isOutOfBound(L, rect):
    return rect[0] < 0 or rect[1] < 0 or rect[0] + rect[2] > L or rect[1] + rect[3] > L

# move a rect from one box to another
def moveRect(rect ,box_src, box_dst):
    if rect in box_src:
        box_dst.append(rect)
        box_src.remove(rect)

# remove rect from a box
def removeRect(rect, box_src):
    if rect in box_src:
        box_src.remove(rect)

# add rect from a box
def addRect(rect, box_dst):
    box_dst.append(rect)

# a geometric neighborhood is
# when a rectangle moves from one box to another
# returns a list of states
def geometric_neighbor(sol):
    initial = sol
    initial[1].sort(key=lambda item: (len(item), item))
    neighbors1 = []
    for box_src in initial[1]:
        if len(neighbors1) >= 2:
            break
        for rect_src in box_src:
            if len(neighbors1) >= 2:
                break
            stepsize = round(initial[0] * 0.1)
            for box_dst in initial[1]:
                if box_dst != box_src and len(box_dst) >= len(box_src) and len(neighbors1) < 2:
                    w = rect_src[2]
                    h = rect_src[3]
                    for y in range(0, initial[0]-h, stepsize):
                        for x in range(0, initial[0]-w, stepsize):
                            collide = False
                            for rect_dst in box_dst:
                                if isCollision([x, y, w, h], rect_dst):
                                    collide = True
                                    break
                            if not collide:
                                addRect([x,y,w,h], box_dst)
                                removeRect(rect_src, box_src)
                                neighbors1.append(copy.deepcopy(initial))
                                addRect(rect_src, box_src)
                                removeRect([x,y,w,h], box_dst)
                                break
                        else:
                            continue
                        break

                # 90 degree placement
                if box_dst != box_src and len(box_dst) >= len(box_src) and len(neighbors1) < 2:
                    w = rect_src[3]
                    h = rect_src[2]
                    for y in range(0, initial[0] - h, stepsize):
                        for x in range(0, initial[0] - w, stepsize):
                            collide = False
                            for rect_dst in box_dst:
                                if isCollision([x, y, w, h], rect_dst):
                                    collide = True
                                    break
                            if not collide:
                                addRect([x, y, w, h], box_dst)
                                removeRect(rect_src, box_src)
                                neighbors1.append(copy.deepcopy(initial))
                                addRect(rect_src, box_src)
                                removeRect([x, y, w, h], box_dst)
                                break
                        else:
                            continue
                        break
    return neighbors1

# returns the centroid of a given rectangle
# [1, 1, 30, 40]
def rect_centroid(rect):
    x = rect[0] + (rect[2] / 2)
    y = rect[1] + (rect[3] / 2)
    return x, y

def objective_fn(state):
    # the more empty boxes, the better
    # therefore counting empy boxes
    boxes = state[1]
    emptybox = 0
    for box in boxes:
        if len(box) == 0:
            emptybox += 1
    emptybox_value = 1 / (1 + emptybox)

    # a box needs to have as many triangle as possible
    score = 0
    for box in boxes:
        for rect in box:
            score = score + len(box)
    concentration = 1 / (1 + score)
    return emptybox_value + concentration
