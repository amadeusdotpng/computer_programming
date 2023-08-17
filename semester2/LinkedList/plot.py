import matplotlib.pyplot as plt
plt.rc('font', size=7.5)

gen = iter(tuple(line.strip().split()) for line in open('insert_pop.txt', 'r+').readlines())

for i in range(2):
    index = 0
    label = ()
    X = []
    y = []
    while True:
        line = next(gen, None)

        if line == None or not line:
            break

        if index == 0:
            label = line
            print(label)
        else:
            X.append(float(line[0]))
            y.append(float(line[1])*1000)
        index += 1
    plt.xscale('log', base=2)
    plt.xticks([X[i] for i in range(0, len(X), 2)])
    plt.yscale('log', base=2)
    plt.xlabel('Number of elements')
    plt.ylabel('Time (milliseconds)')
    plt.title('Insert Pop')
    plt.plot(X, y)
plt.legend(['Python Insert Left', 'Linked List Pop Right'])
plt.savefig('insert_pop.png', format='png', dpi=1200)

