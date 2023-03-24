import random
for i in range(50_000):
    a = random.randint(1, 1000)
    b = random.randint(1, 1000)
    c = random.randint(1, 1000)
    x, y, z = sorted([a, b, c])

    if x+y < z:
        print(f'{a},{b},{c},not')
    elif x+y>z and x*x + y*y == z*z:
        print(f'{a},{b},{c},right')
    elif x+y>z and x*x + y*y >= z*z:
        print(f'{a},{b},{c},acute')
    elif x+y>z and x*x + y*y <= z*z:
        print(f'{a},{b},{c},obtuse')
