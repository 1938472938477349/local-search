# current_instance: the current state
# neighbor_fn: the neighborhood function which creates a list of instances
# obj_fn: the objective function which rates each state
# it: number of iterations

def local_search(start_instance, neighbor_fn, obj_fn, it):
    current_instance = start_instance
    history = [current_instance]
    for i in range(0, it):
        neighbors = neighbor_fn(current_instance,i,it)
        minimum_val = obj_fn(current_instance,i,it)
        minimum_neighbor = current_instance
        #token = 0
        for n in neighbors:
            if obj_fn(n,i,it) < minimum_val:
                minimum_neighbor = n
                minimum_val = obj_fn(n,i,it)
                #token = 0
            #else:
            #    token = token + 1

            #if token == 100:
            #    break
        if current_instance == minimum_neighbor:
            print("Iteration until minimum: " + str(i))
            break
        else:
            current_instance = minimum_neighbor
            history.append(current_instance)
    return current_instance, history



