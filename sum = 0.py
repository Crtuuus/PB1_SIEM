def fakulteta(n):
    if n == 0:
        return 1
    elif n > 0:
        return n*fakulteta(n-1)
print(fakulteta(10))