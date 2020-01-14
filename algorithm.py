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

# calculate the intersection of two rectangles, returns a value, indicating the overlapping area
def intersectionRect(r1, r2):
    r1_right = r1[0] + r1[2]
    r2_right = r2[0] + r2[2]
    r1_left = r1[0]
    r2_left = r2[0]
    r1_top = r1[1]
    r2_top = r2[1]
    r1_bot = r1[1] + r1[3]
    r2_bot = r2[1] + r2[3]
    x_overlap = max(0, min(r1_right, r2_right) - max(r1_left, r2_left))
    y_overlap = max(0, min(r1_bot, r2_bot) - max(r1_top, r2_top))
    overlapArea = x_overlap * y_overlap

    sum_area = r1[2] * r1[3] + r2[2] * r2[3] - overlapArea

    return overlapArea / sum_area


# a geometric neighborhood is
# when a rectangle moves from one box to another
# returns a list of states
def geometric_neighbor(sol,i,it):
    initial = sol
    initial[1].sort(key=lambda item: (len(item), item))
    neighbors1 = []
    neighbor_limit = 100
    for box_src in initial[1]:
        if len(neighbors1) >= neighbor_limit:
            break
        for rect_src in box_src:
            if len(neighbors1) >= neighbor_limit:
                break
            stepsize = round(initial[0] * 0.1)
            for box_dst in initial[1]:
                if box_dst != box_src and len(box_dst) >= len(box_src) and len(neighbors1) < neighbor_limit:
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
                if box_dst != box_src and len(box_dst) >= len(box_src) and len(neighbors1) < neighbor_limit:
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

def objective_fn(state,i,it):
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


# [9, [[[0, 0, 5, 6]], [[0, 0, 3, 7]], [[0, 0, 6, 4]]]]
def overlay_neighbor(sol,i,it):
    initial = sol
    initial[1].sort(key=lambda item: (len(item), item))
    neighbors = []

    for box_src in initial[1]:
        for rect_src in box_src:
            stepsize = round(initial[0] * 0.1)
            for box_dst in initial[1]:
                w = rect_src[2]
                h = rect_src[3]
                for y in range(0, initial[0]-h, stepsize):
                    for x in range(0, initial[0]-w, stepsize):
                       # we do not test for collision but for intersection
                        maxIntersection = 0.0
                        for rect_dst in box_dst:
                           if rect_src != rect_dst and intersectionRect(rect_src, rect_dst) > maxIntersection:
                                maxIntersection = intersectionRect(rect_src, rect_dst)
                        if maxIntersection <= (1.0 - i/it):
                            addRect([x,y,w,h], box_dst)
                            removeRect(rect_src, box_src)
                            neighbors.append(copy.deepcopy(initial))
                            addRect(rect_src, box_src)
                            removeRect([x,y,w,h], box_dst)

                # 90 degree placement
                w = rect_src[3]
                h = rect_src[2]
                for y in range(0, initial[0] - h, stepsize):
                    for x in range(0, initial[0] - w, stepsize):
                        maxIntersection = 0.0
                        for rect_dst in box_dst:
                           if rect_src != rect_dst and intersectionRect(rect_src, rect_dst) > maxIntersection:
                                maxIntersection = intersectionRect(rect_src, rect_dst)
                        if maxIntersection <= (1.0 - i/it):
                            addRect([x,y,w,h], box_dst)
                            removeRect(rect_src, box_src)
                            neighbors.append(copy.deepcopy(initial))
                            addRect(rect_src, box_src)
                            removeRect([x,y,w,h], box_dst)

    print("# of Neightbor: " + str(len(neighbors)))
    return neighbors

def objective_fn_overlay(state,i,it):
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

    intersection_score = 0
    for box in boxes:
        for rect in box:
            for rect2 in box:
                if rect != rect2:
                    intersection_score += 1000* intersectionRect(rect, rect2) * i/it


    return emptybox_value + concentration + intersection_score

# testing intersection print(intersectionRect([0,0,100,100],[50,50,100,100]))