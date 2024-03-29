import tkinter as tk
import random
import local_search, instance_gen, algorithm
import ast

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.resizable(False, False)
        self.width = 800
        self.height = 600
        self.canvas_width = self.width
        self.canvas_height = self.height
        self.canvas1 = tk.Canvas(window, width = self.canvas_width, height = self.canvas_height, background='black')
        self.canvas1.pack(side=tk.LEFT)
        self.l_label = tk.Label(window, text="Box Length L")
        self.l_label.pack()
        self.l = tk.Entry(window)
        self.l.insert(0,"10")
        self.l.pack()
        self.n_label = tk.Label(window, text="Number of Rectangles N")
        self.n_label.pack()
        self.n = tk.Entry(window)
        self.n.insert(0,"3")
        self.n.pack()
        self.minw_label = tk.Label(window, text="Min Width")
        self.minw_label.pack()
        self.minw = tk.Entry(window)
        self.minw.insert(0,"1")
        self.minw.pack()
        self.maxw_label = tk.Label(window, text="Max Width")
        self.maxw_label.pack()
        self.maxw = tk.Entry(window)
        self.maxw.insert(0,"10")
        self.maxw.pack()
        self.minh_label = tk.Label(window, text="Min Height")
        self.minh_label.pack()
        self.minh = tk.Entry(window)
        self.minh.insert(0,"1")
        self.minh.pack()
        self.maxh_label = tk.Label(window, text="Max Height")
        self.maxh_label.pack()
        self.maxh = tk.Entry(window)
        self.maxh.insert(0,"10")
        self.maxh.pack()
        self.scaleR = tk.Scale(window, from_=10, to=10000, orient=tk.HORIZONTAL, label="Iterations", width= 10, sliderlength= 15)
        self.scaleR.set(1000)
        self.scaleR.pack()
        self.btn_save1= tk.Button(window, text="Rule-Based", width=15, command=self.visualize_rule)
        self.btn_save1.pack(side=tk.BOTTOM)
        self.btn_save2= tk.Button(window, text="Overlap", width=15, command=self.visualize_overlap)
        self.btn_save2.pack(side=tk.BOTTOM)
        self.btn_save3= tk.Button(window, text="Geometric", width=15, command=self.visualize_geometric)
        self.btn_save3.pack(side=tk.BOTTOM)
        self.btn_browse1= tk.Button(window, text="Trivial Solution", width=15, command=self.visualize_trivial)
        self.btn_browse1.pack(side=tk.BOTTOM)
        self.btn_random= tk.Button(window, text="Random Value", width=15, command=self.random)
        self.btn_random.pack(side=tk.BOTTOM)
        self.listbox_label = tk.Label(window, text="History")
        self.listbox_label.pack()
        self.listbox = tk.Listbox(window)
        self.listbox.bind("<Double-Button-1>", self.visualize_history)
        self.listbox.pack()
        self.input = []
        self.window.mainloop()

    def visualize_history(self, val):
        if len(self.listbox.curselection()) != 0:
            selection = self.listbox.get(self.listbox.curselection())
            state = ast.literal_eval(selection)
            self.visualize(state)

    # set random value to the entry boxes
    def random(self):
        l = random.randint(1, 100)
        n = random.randint(1, 50)
        minw = random.randint(1, l)
        maxw = random.randint(minw, l)
        minh = random.randint(1, l)
        maxh = random.randint(minh, l)
        self.l.delete(0,tk.END)
        self.l.insert(0,l)
        self.n.delete(0,tk.END)
        self.n.insert(0, n)
        self.minw.delete(0,tk.END)
        self.minw.insert(0, minw)
        self.maxw.delete(0,tk.END)
        self.maxw.insert(0, maxw)
        self.minh.delete(0,tk.END)
        self.minh.insert(0, minh)
        self.maxh.delete(0,tk.END)
        self.maxh.insert(0, maxh)

    # visualize the trivial solution
    def visualize_trivial(self):
        L = int(self.l.get())
        N = int(self.n.get())
        minw = int(self.minw.get())
        maxw = int(self.maxw.get())
        minh = int(self.minh.get())
        maxh = int(self.maxh.get())
        self.input = algorithm.trivia_sol(instance_gen.generate_instance(L, N, minh, maxh, minw, maxw))
        self.listbox.insert(tk.END, str(self.input))
        self.visualize(self.input)

    # visualize a state
    # a state can be:
    # [9, [[[0, 0, 5, 6]], [[0, 0, 3, 7]], [[0, 0, 6, 4]]]]
    def visualize(self, state):
        self.canvas1.delete("all")
        state[1].sort(key=lambda item: (-len(item), item))
        L = state[0]
        boxes = state[1]
        index_x = L/2
        index_y = L/2
        for box in boxes:
            self.canvas1.create_rectangle(index_x, index_y, index_x+L, index_y + L, fill="#888888")
            self.canvas1.pack()
            for rect in box:
                self.canvas1.create_rectangle(index_x+ rect[0], index_y+rect[1], index_x+ rect[0] + rect[2], index_y+rect[1] + rect[3], fill="#ffffff")
                self.canvas1.pack()
            index_x = index_x + L + L / 2
            if index_x+L > self.width:
                index_x = L / 2
                index_y = index_y + L +L / 2

    # visualize solution via geometric neighbor
    def visualize_geometric(self):
        if self.input != []:
            # start with trivia solution
            start_state = self.input
            result, history = local_search.local_search(start_state, algorithm.geometric_neighbor, algorithm.objective_fn, int(self.scaleR.get()))
            for h in history:
                self.listbox.insert(tk.END, str(h))
            self.listbox.insert(tk.END, str(result))
            self.visualize(result)

    # visualize solution via overlap neighbor
    def visualize_overlap(self):
        if self.input != []:
            start_state = self.input
            result, history = local_search.local_search(start_state, algorithm.overlay_neighbor, algorithm.objective_fn_overlay, int(self.scaleR.get())+1)
            for h in history:
                self.listbox.insert(tk.END, str(h))
            self.listbox.insert(tk.END, str(result))
            self.visualize(result)

    # visualize solution via rule-based neighbor
    def visualize_rule(self):
        if self.input != []:
            start_state = self.input
            result, history = local_search.local_search(start_state, algorithm.rule_neighbor, algorithm.objective_fn_rule, int(self.scaleR.get())+1)
            for h in history:
                self.listbox.insert(tk.END, str(h))
            self.listbox.insert(tk.END, str(result))
            self.visualize(result)

App(tk.Tk(), "Local Search")