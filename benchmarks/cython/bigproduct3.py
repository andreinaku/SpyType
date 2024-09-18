def bigproduct(digits, n=13):
    best = 0
    for i in range(len(digits) - (n-1)):
        product = 1
        for j in range(n):
            digit = digits[i + j]
            product *= digit
        if product > best:
            best = product
    return best
