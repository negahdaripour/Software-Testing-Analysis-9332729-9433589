from fuzzingbook.ConcolicFuzzer import ArcCoverage
from fuzzingbook.SymbolicFuzzer import AdvancedSymbolicFuzzer
from fuzzingbook.ControlFlow import PyCFG, CFGNode, to_graph, gen_cfg
import inspect
from graphviz import Source, Graph


#from test_function import test_function
from test_reassign import test_function_reassign
from paths_and_constraints import paths_and_constraints
from test_while import test_function_loop
from gcd import gcd_f

# initialzie Simple Symbolic Fuzzer
sym_fuzzer = AdvancedSymbolicFuzzer(
   gcd_f,
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
    v = gcd_f(*data[-1])
    print(r, "Result", repr(v))

print("Num of Data:", len(data))

# we use arcCoverage as a tracer that uses data generated
# to determine how much of the paths have been taken

with ArcCoverage() as cov:
    for a, b in data:
        gcd_f(a, b)

# generate and view Control Flow Graph 
graph = Source(to_graph(gen_cfg(inspect.getsource(gcd_f)), arcs= cov.arcs()))

# insert unique filename and the desired directory to save the graph in pdf format
#graph.view(filename="tf_8.gv", directory="E:\dir\graphs")

paths_and_constraints(gcd_f)



