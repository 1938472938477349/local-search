import instance_gen


# HOW A SOLUTION IS ENCODED
# [boxsize, boxes]
# boxes = [box1, box2, ...]
# box1 = [rect1, rect2, ...]
# rect1 = [index, (w, h)]



input = instance_gen.generate_instance(9, 3, 0, 9, 0, 9)


# the trivial solution would be to put each rectangle into its own box
def trivia_sol(input):
    boxes = []
    sol = [input[0], boxes]

    for i in input[1]:
        sol[1].append([[0, i]])

    return sol


print(input)
print(trivia_sol(input))