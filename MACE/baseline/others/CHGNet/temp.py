import matplotlib.pyplot as plt

T = []

with open('./test/md.log', 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if not line.startswith('Time'):
            # 读取这一行第五个数据，即温度
            temperature = float(line.split()[4])
            T.append(temperature)

plt.plot(T)
plt.xlabel('Time step')
plt.ylabel('Temperature (K)')
plt.title('Temperature')
plt.savefig("./temperature.png")