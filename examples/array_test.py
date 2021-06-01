def test_function(a: int, b: list) -> int:
    if a == [0]:
        return "Equal"
    else:
        if a > b[1]:
            return "First"
        else: 
            return "Second"
    