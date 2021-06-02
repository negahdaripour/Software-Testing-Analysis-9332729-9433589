""" Utility Functions and Classes

Additional Functions are defined for the AdvancedSymbolicFuzzer to be able to get 
completed paths using dfs and to print the results, because the advanced fuzzer 
generates executable paths.

    Typical Usage Example:
        paths_and_constraints(function)
"""

from utils.ModifiedSymbolicFuzzer import *
import z3


class AdvancedSymbolicFuzzer(AdvancedSymbolicFuzzer):
    """ 
    A class used to add functions to the original AdvancedSymbolicFuzzer class

    Methods:
        get_completed_paths(self, fenter, depth-0)
            returns all paths from 'enter' to 'exit' for extracting constraints

        get_all_paths_for_print(self, fenter, depth=0)
            returns all paths from 'enter' to 'exit' in a readable format
    """

    def get_completed_paths(self, fenter, depth=0):
        """ Returns all paths from 'enter' to 'exit using DFS

        If the argument 'depth' isn't passed in, the default is 0

        Args:
            fenter : graph node 
                function entry point
            depth : int, optional
                the depth of recursion

        Returns:
            A list of nodes that build up the path

        Raises:
            Maximum depth exceeded
                If maxmimum depth specified is exceeded
        """

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
                fnpaths.append([PNode(idx, fenter, order = idx)] + path)
        return fnpaths

    def get_all_paths_for_print(self, fenter, _depth=0):
        """ Returns all paths from 'enter' to 'exit using DFS

        If the argument 'depth' isn't passed in, the default is 0

        Ars:
            fenter : 
                function entry point
            depth : int, optional
                the depth of recursion

        Returns:
            A list of nodes of represent the path

        Raises:
            Maximum depth exceeded
                If maxmimum depth specified is exceeded
        """

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
    """ Prints all paths from 'enter' to 'exit', constraints of each path, whether path is sat or unsat

    Parameters
    ----------
    f : function object
        The function we want to explose

    """

    sym_fuzzer = AdvancedSymbolicFuzzer(
        f, 
        max_tries = 10,
        max_iter = 10,
        max_depth = 10
    )

    paths = sym_fuzzer.get_completed_paths(sym_fuzzer.fnenter)
    printables = sym_fuzzer.get_all_paths_for_print(sym_fuzzer.fnenter)

    print("Num of Completed Paths:", len(paths))
    print("Num of Printable Paths:", len(printables))

    print("Result:")
    for i in range(len(paths)):
        print(" Path: ", i + 1)
        for step in printables[i]:
            print(step)
        s = z3.Solver()
        constr = sym_fuzzer.extract_constraints(paths[i])
        print("Constraints: \t:" , constr)
        for k in range(len(constr)):
            names = used_identifiers(constr[k])
            
            for j in range(len(names)):
                exec(names[j] + " = z3.Int('" + names[j] + "')")
            
            single_constr = constr[k]
            indx = constr[k].find('Not')
            if(indx > 0):
                single_constr = constr[k][:indx + 3] + '(' + constr[k][indx + 3:] + ')'

            if '[' in single_constr:
                single_constr = single_constr.replace('[','___')
                single_constr = single_constr.replace(']', '')
                
            f = eval(single_constr)
            s.add(f)
        print(s.check())

