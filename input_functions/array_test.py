def test_function(a: int, b: list) -> int:
    if a == b[0]:
        return "Equal"
    else:
        if a > b[1]:
            return "First"
        else: 
            return "Second"
    