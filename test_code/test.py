def generate_test () :
    yield 1
    yield 2
    yield 3


gt = generate_test()

print(next(gt))
print(next(gt))
print(next(gt))