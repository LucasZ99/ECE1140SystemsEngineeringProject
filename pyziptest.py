blocks = [1, 2, 3, 4, 5]

print(blocks)
for a, b in zip(blocks[:-1], blocks[1:]):
    print(a, b)
