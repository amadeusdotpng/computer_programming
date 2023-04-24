import os

directory = '.'

for filename in os.listdir(directory):
    with open(filename, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        s = ''.join(lines)

    with open(f'../processed/{filename}', 'w+') as f:
        f.write(s)
    print(filename)

