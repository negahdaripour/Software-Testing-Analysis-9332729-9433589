def gcd_f(a: int, b: int) -> int:
    if a < 2:
        c: int = a
        a = b
        b = c

    while b != 0:
        c: int = a
        a = b
        b = c % b
    return a