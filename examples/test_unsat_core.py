def test_unsat_core(a: int, b: int) -> int:
    if a == b:
        return "Equal"
    else:
        if a != b:
            return "Not Equal"
        else:
            return "This line will never run!"