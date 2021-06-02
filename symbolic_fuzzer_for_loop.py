from fuzzingbook.ConcolicFuzzer import ArcCoverage
from utils.ModifiedSymbolicFuzzer import *
from fuzzingbook.ControlFlow import PyCFG, CFGNode, to_graph, gen_cfg
import inspect
from graphviz import Source, Graph


#from test_function import test_function
from utils.paths_and_constraints import paths_and_constraints
from utils.fuzzer_utils import main

#main()

from examples.converted_functions import for_test_function


# initialzie Simple Symbolic Fuzzer
sym_fuzzer = AdvancedSymbolicFuzzer(
    for_test_function,
    max_tries = 10,
    max_iter = 10,
    max_depth =10
)

# Container for data
data = []

# generate data with method 'fuzz()'
# append the generated data to container
# call function that fuzzing is for
# print the results

for i in range(10):
    r = sym_fuzzer.fuzz()
    data.append((r['a'].as_long(), r['b'].as_long()))
    v = for_test_function(*data[-1])
    print(r, "Result", repr(v))

print("Num of Data:", len(data))

# we use arcCoverage as a tracer that uses data generated
# to determine how much of the paths have been taken

with ArcCoverage() as cov:
    for a, b in data:
        for_test_function(a, b)

# generate and view Control Flow Graph 
graph = Source(to_graph(gen_cfg(inspect.getsource(for_test_function)), arcs= cov.arcs()))

# insert unique filename and the desired directory to save the graph in pdf format
graph.view(filename="tf_12.gv", directory="E:\dir\graphs")

paths_and_constraints(for_test_function)


