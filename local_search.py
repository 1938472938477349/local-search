



# current_instance: the current state
# neighbor_fn: the neighborhood function which creates a list of instances
# obj_fn: the objective function which rates each state
# it: number of iterations

def local_search(current_instance, neighbor_fn, obj_fn, it):
    for i in range(0, it):
        initial = current_instance

        # in every iterations, the neighborhhod is calculated and the best neighbor is reassigned to the current state
        neighbors = neighbor_fn(current_instance)
        for n in neighbors:
            if obj_fn(n) <= obj_fn(current_instance):
                current_instance = n

        # if the current instance doesn't change, abort the algorithm
        if current_instance == initial:
            break

    return current_instance



