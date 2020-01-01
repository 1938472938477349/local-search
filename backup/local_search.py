



# current_instance: the current state
# neighbor_fn: the neighborhood function which creates a list of instances
# obj_fn: the objective function which rates each state
# it: number of iterations

def local_search(start_instance, neighbor_fn, obj_fn, it):
    current_instance = start_instance

    for i in range(0, it):
        #print(i)
        # in every iterations, the neighborhhod is calculated and the best neighbor is reassigned to the current state
        neighbors = neighbor_fn(current_instance)

        minimum_val = obj_fn(current_instance)
        minimum_neighbor = current_instance

        for n in neighbors:
            # search all neighbors for the best neighbor
            if obj_fn(n) < minimum_val:
                minimum_neighbor = n
                minimum_val = obj_fn(n)


        # if the current instance doesn't change, abort the algorithm
        if current_instance == minimum_neighbor:
            print("Iteration until minimum: " + str(i))
            break
        else:
            current_instance = minimum_neighbor


    return current_instance



