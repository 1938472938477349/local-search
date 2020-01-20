
import time
import instance_gen
import algorithm
import local_search

def test(n_instance, L, box_n, box_l_min, box_l_max, box_w_min, box_w_max):

    print("Starting tests...")
    print("# of Instances: " + str(n_instance) + "| Box Length: " + str(box_n) + "| # of Boxes: " + str(box_n))

    start = time.process_time()
    for i in range(0, n_instance):
        instance = instance_gen.generate_instance(L, box_n, box_l_min, box_l_max, box_w_min, box_w_max)
        trivia = algorithm.trivia_sol(instance)
        result, history = local_search.local_search(trivia, algorithm.geometric_neighbor, algorithm.objective_fn, 1000)
    end = time.process_time()
    print("Geometric Test Time... " + str(end - start))


    start = time.process_time()
    for i in range(0, n_instance):
        instance = instance_gen.generate_instance(L, box_n, box_l_min, box_l_max, box_w_min, box_w_max)
        trivia = algorithm.trivia_sol(instance)
        result, history = local_search.local_search(trivia, algorithm.overlay_neighbor, algorithm.objective_fn_overlay, 1000)
    end = time.process_time()
    print("Overlay Test Time... " + str(end - start))


    start = time.process_time()
    for i in range(0, n_instance):
        instance = instance_gen.generate_instance(L, box_n, box_l_min, box_l_max, box_w_min, box_w_max)
        trivia = algorithm.trivia_sol(instance)
        result, history = local_search.local_search(trivia, algorithm.rule_neighbor, algorithm.objective_fn_rule, 1000)
    end = time.process_time()
    print("Rule-Based Test Time... " + str(end - start))



test(1, 30, 5, 5, 30, 5, 30)

test(5, 30, 5, 5, 30, 5, 30)

test(100, 30, 5, 5, 30, 5, 30)

test(1000, 30, 5, 5, 30, 5, 30)