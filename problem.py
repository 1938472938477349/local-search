import instance_gen
import copy
import random

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
        x = random.randint(0, input[0]-i[0])
        y = random.randint(0, input[0]-i[1])

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





# a geometric neighborhood is
# 1. when a rectangle moves from one box to another without any positional change
# 2. a rectagle moves one unit
# 3. a rectagle rotates
# returns a list of states
def geometric_neighbor(sol):
    initial = sol
    neighbors = []
    # geometric operation type 1, moving from one box to another
    for box_src in initial[1]:
        for rect_src in box_src:
            # every rect in src can be moved

            for box_dst in initial[1]:
                if box_dst != box_src:

                    # can rect can be moved?
                    collide = False
                    for rect_dst in box_dst:
                        collide = isCollision(rect_src, rect_dst)
                    if not collide:
                        moveRect(rect_src, box_src, box_dst)
                        neighbors.append(copy.deepcopy(initial))
                        moveRect(rect_src, box_dst, box_src)
                        #neighbors.append(initial)
                        #initial = sol

    # geometric operation type 2, moving a rectagle within a box
    initial = sol
    for box in initial[1]:
        box_initial = copy.deepcopy(box)

        for rect in box:
            rect_initial = copy.deepcopy(rect)

            # forward x + 1
            rect[0] = rect[0] + 1
            collide = False
            for rect2 in box_initial:
                if rect_initial != rect2:
                    collide = isCollision(rect, rect2)
            if not collide and not isOutOfBound(initial[0], rect):
                neighbors.append(copy.deepcopy(initial))

            # backward x - 1
            rect[0] = rect[0] -2
            collide = False
            for rect2 in box_initial:
                if rect_initial != rect2:
                    collide = isCollision(rect, rect2)
            if not collide and not isOutOfBound(initial[0], rect):
                neighbors.append(copy.deepcopy(initial))
            rect[0] = rect[0] + 1 # undo


            # forward y + 1
            rect[1] = rect[1] + 1
            collide = False
            for rect2 in box_initial:
                if rect_initial != rect2:
                    collide = isCollision(rect, rect2)
            if not collide and not isOutOfBound(initial[0], rect):
                neighbors.append(copy.deepcopy(initial))

            # backward y - 1
            rect[1] = rect[1] - 2
            collide = False
            for rect2 in box_initial:
                if rect_initial != rect2:
                    collide = isCollision(rect, rect2)
            if not collide and not isOutOfBound(initial[0], rect):
                neighbors.append(copy.deepcopy(initial))
            rect[1] = rect[1] + 1 # undo


    print("Neighborhood: " + str(len(neighbors)))
    return neighbors



def objective_fn(state):
    # the more empty boxes, the better
    # therefore counting empy boxes
    boxes = state[1]
    emptybox = 0
    for box in boxes:
        if len(box) == 0:
            emptybox += 1

    print("Emptybox: " + str(emptybox))


    eval  = 1/(1+emptybox)
    return eval





#print(input)
#print(trivia_sol(input))
#print("[9, [[[0, 0, 5, 6]], [[0, 0, 3, 7]], [[0, 0, 6, 4]]]]")

print(geometric_neighbor([2, [[[0, 0, 1, 1], [1, 0, 1, 1]]]]))