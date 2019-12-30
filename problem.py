import instance_gen
import copy
import random
import numpy as np

# HOW A STATE/SOLUTION IS ENCODED
# [boxsize, boxes]
# boxes = [box1, box2, ...]
# box1 = [rect1, rect2, ...]
# rect1 = [x, y, w, h]



input = instance_gen.generate_instance(9, 3, 1, 9, 1, 9)


# the trivial solution would be to put each rectangle into its own box
def trivia_sol(input):
    boxes = []
    sol = [input[0], boxes]
    for i in input[1]:
        #x = random.randint(0, input[0]-i[0]) in case I want to randomize the position initially
        #y = random.randint(0, input[0]-i[1])
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
# 1. when a rectangle moves from one box to another without any positional change
# 2. a rectagle moves one unit
# 3. a rectagle rotates
# returns a list of states
def geometric_neighbor(sol):
    initial = sol

    neighbors1 = []
    neighbors2 = []

    # geometric operation type 1, moving from one box to another

    # for box_src in initial[1]:
    #     for rect_src in box_src:
    #         # every rect in src can be moved
    #         for box_dst in initial[1]:
    #             if box_dst != box_src:
    #
    #                 # can rect can be moved?
    #                 collide = False
    #                 for rect_dst in box_dst:
    #                     if isCollision(rect_src, rect_dst):
    #                         collide = True
    #                 if not collide:
    #                     moveRect(rect_src, box_src, box_dst)
    #                     neighbors.append(copy.deepcopy(initial))
    #                     moveRect(rect_src, box_dst, box_src)

    for box_src in initial[1]:
        if len(neighbors1) > 1:
            break
        for rect_src in box_src:
            if len(neighbors1) >1:
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

    # geometric operation type 2, moving a rectagle within a box


    # initial = sol
    # stepsize = round(initial[0] * 0.1)
    #
    # for box in initial[1]:
    #     box_initial = copy.deepcopy(box)
    #
    #     for rect in box:
    #         rect_initial = copy.deepcopy(rect)
    #
    #         # forward x + 1
    #         rect[0] = rect[0] + stepsize
    #         collide = False
    #         for rect2 in box_initial:
    #             if rect_initial != rect2:
    #                 if isCollision(rect, rect2):
    #                     collide = True
    #                     break
    #         if not collide and not isOutOfBound(initial[0], rect):
    #             neighbors2.append(copy.deepcopy(initial))
    #
    #         # backward x - 1
    #         rect[0] = rect[0] - 2*stepsize
    #         collide = False
    #         for rect2 in box_initial:
    #             if rect_initial != rect2:
    #                 if isCollision(rect, rect2):
    #                     collide = True
    #                     break
    #         if not collide and not isOutOfBound(initial[0], rect):
    #             neighbors2.append(copy.deepcopy(initial))
    #         rect[0] = rect[0] + stepsize # undo
    #
    #
    #         # forward y + 1
    #         rect[1] = rect[1] + stepsize
    #         collide = False
    #         for rect2 in box_initial:
    #             if rect_initial != rect2:
    #                 if isCollision(rect, rect2):
    #                     collide = True
    #                     break
    #         if not collide and not isOutOfBound(initial[0], rect):
    #             neighbors2.append(copy.deepcopy(initial))
    #
    #         # backward y - 1
    #         rect[1] = rect[1] - 2*stepsize
    #         collide = False
    #         for rect2 in box_initial:
    #             if rect_initial != rect2:
    #                 if isCollision(rect, rect2):
    #                     collide = True
    #                     break
    #         if not collide and not isOutOfBound(initial[0], rect):
    #             neighbors2.append(copy.deepcopy(initial))
    #         rect[1] = rect[1] + stepsize # undo



    neighbors = neighbors1 + neighbors2
    # print("Number of Neighbor1: " + str(len(neighbors1)))
    # print("Number of Neighbor2: " + str(len(neighbors2)))
    #print("Number of Neighbor: " + str(len(neighbors)))
    return neighbors


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


    # between the boxes, the rectangles should be farther apart
    # therefore I need to maximize the distance between the boxes (inter variance)
    # centroids = []
    # for box in boxes:
    #     if len(box) != 0:
    #         box_centroid_x = 0
    #         box_centroid_y = 0
    #
    #         for rect in box:
    #             x, y = rect_centroid(rect)
    #             box_centroid_x += x
    #             box_centroid_y += y
    #
    #         box_centroid_x = box_centroid_x / len(box)
    #         box_centroid_y = box_centroid_y / len(box)
    #         centroids.append([box_centroid_x, box_centroid_y])
    #
    # inter_variance = 1 / 1 + np.var(centroids)



    # within a box the rectangles should be close together
    # therefor minimize intra variance
    # intra_variances = []
    # for box in boxes:
    #     if len(box) != 0:
    #         rectcen = []
    #         for rect in box:
    #             x, y = rect_centroid(rect)
    #             rectcen.append([x,y])
    #         intra_variances.append(np.var(rectcen))
    #
    # intra_variances_mean = sum(intra_variances) / len(intra_variances)



    # a box needs to have as many triangle as possible
    score = 0
    for box in boxes:
        for rect in box:
            score = score + len(box)
    concentration = 1 / (1 + score)



    #print("Concentration " + str(concentration))
    #print("Inter Variance " + str(inter_variance))
    #print("Intra Variance " + str(intra_variances_mean))
    eval  = 1000 * concentration #+  intra_variances_mean # +  inter_variance +  intra_variances_mean + 1000000 * emptybox_value +


    return eval








#print(input)
#print(trivia_sol(input))
#print("[9, [[[0, 0, 5, 6]], [[0, 0, 3, 7]], [[0, 0, 6, 4]]]]")

#print(geometric_neighbor([2, [[[0, 0, 1, 1], [1, 0, 1, 1]]]]))