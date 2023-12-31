from abc import ABC, abstractmethod
import threading

import graph
from debug import debug


class Algorithm(ABC):
    name = ""
    description = ""
    barrier = threading.Barrier(2)
    finished = False
    window = None

    def __init__(self, name, description, window):
        self.name = name
        self.description = description
        self.window = window

    # call this method to start the algorithm
    def start(self, graph):
        debug("Starting algorithm: " + self.name)
        self.finished = False
        self.barrier.reset() # reset barrier
        thread = threading.Thread(target=self.run, args=(graph,)) # create thread to execute algorithm
        thread.start() # start thread

    # the algorithm should be implemented in this method, and should wait with self.pause() before each step
    # it should also check whether self.pause() returns True, and if so, return from the method
    @abstractmethod
    def run(self, graph):
        pass

    # call this method to execute the next step in the algorithm, releasing the barrier
    def step(self):
        if not self.finished:
            debug("Executing next step in algorithm: " + self.name)
            self.barrier.wait()

    # call this method to pause the algorithm, returns True if algorithm is being killed
    def pause(self):
        self.window.root.event_generate("<<UpdateGraph>>") # trigger update of graph in main thread
        try:
            self.barrier.wait()
        except threading.BrokenBarrierError:
            debug("Barrier broken, algorithm finished: " + self.name)
            return True
        return False

    def kill(self):
        debug("Killing algorithm: " + self.name)
        self.barrier.abort()


class TestAlgorithm(Algorithm):
    def __init__(self, window):
        super().__init__("Test Algorithm", "This is a test algorithm that colors all nodes", window)

    def run(self, graph):
        if self.pause(): # check if algorithm is being killed
            return
        for node in graph.nodes:
            node.color = "red"
            if self.pause():
                return
        self.finished = True
        debug("Algorithm finished: " + self.name)