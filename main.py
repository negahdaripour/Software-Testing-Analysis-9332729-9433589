""" Symbolic Fuzzer In Action

This script allows the user to view the result of the sample programs in the '/examples'
directory and view the capabilities of the fuzzer.

Usage Example:
    symbolic_fuzzer()
"""

from examples.symbolic_fuzzer import symbolic_fuzzer
from examples.symbolic_fuzzer_array import symbolic_fuzzer_array
from examples.symbolic_fuzzer_for_loop import symbolic_fuzzer_for_loop
from examples.symbolic_fuzzer_unsat_core import symbolic_fuzzer_unsat_core
from examples.symbolic_fuzzer_abs import symbolic_fuzzer_abs

if __name__ == "__main__":
    #symbolic_fuzzer()
    symbolic_fuzzer_array()
    #symbolic_fuzzer_for_loop()
    #symbolic_fuzzer_unsat_core()
    #symbolic_fuzzer_abs()