#from fuzzingbook.SymbolicFuzzer import SimpleSymbolicFuzze
from fuzzingbook.SymbolicFuzzer import *
import z3
from utils.get_var_string_name import get_var_string_name


class AdvancedSymbolicFuzzer(AdvancedSymbolicFuzzer):
    def get_completed_paths(self, fenter, depth=0):
        if depth > self.max_depth:
            raise Exception('Maximum depth exceeded')
        if not fenter.children:
            return [[PNode(0, fenter)]]

        fnpaths = []
        for idx, child in enumerate(fenter.children):
            if depth + 1 > self.max_depth:
                break 
            child_paths = self.get_completed_paths(child, depth + 1)
            for path in child_paths:
                # In a conditional branch, idx is 0 for If, and 1 for Else
                fnpaths.append([PNode(idx, fenter)] + path)
        return fnpaths

    def get_all_paths_for_print(self, fenter, _depth=0):
        if _depth > self.max_depth:
            raise Exception('Maximum depth exceeded')
        if not fenter.children:
            return [[(0, fenter)]]

        fnpaths = []
        for idx, child in enumerate(fenter.children):
            if _depth + 1 > self.max_depth:
                break
            child_paths = self.get_all_paths_for_print(child, _depth + 1)
            for path in child_paths:
                # In a conditional branch, idx is 0 for If, and 1 for Else
                fnpaths.append([(idx, fenter)] + path)
        return fnpaths

def paths_and_constraints(f):
    sym_fuzzer = AdvancedSymbolicFuzzer(
        f, 
        max_tries = 10,
        max_iter = 10,
        max_depth = 10
    )

    # get_all_paths uses the graph to generate all the paths
    # whether the paths are satisfiable or not
    paths = sym_fuzzer.get_completed_paths(sym_fuzzer.fnenter)
    printables = sym_fuzzer.get_all_paths_for_print(sym_fuzzer.fnenter)

    print("Num of Completed Paths:", len(paths))
    print("Num of Printable Paths:", len(printables))

    # in the following nested loops, we print each of the paths
    # their corresponding constraints
    # the result of an attemtp at solving the constraints
    # and whether that path is satisfiable or not
    print("Result:")
    for i in range(len(paths)):
        print(" Path: ", i + 1)
        for step in printables[i]:
            print(step)
        s = z3.Solver()
        constr = sym_fuzzer.extract_constraints(paths[i])
        print("Constraints: \t:" , constr)
        for k in range(len(constr)):
            # get_var_string_name helper function takes a constraint as input
            # and generates the name of the variables to be used later for initializeing z3 symbolic variables
            names = get_var_string_name(constr[k])
            #dynamic variable initialization for z3
            for j in range(len(names)):
                exec(names[j] + " = z3.Int('" + names[j] + "')")
            # python eval takes a constraint in the form of an string as input and evaluates it
            single_constr = constr[k]
            indx = constr[k].find('Not')
            if(indx > 0):
                single_constr = constr[k][:indx + 3] + '(' + constr[k][indx + 3:] + ')'
            f = eval(single_constr)
            print(single_constr)
            # the result of the eval is added to z3.Solver initialized earlier 
            s.add(f)
        #print(s)
        print(s.check())

