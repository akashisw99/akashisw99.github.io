import numpy as np
import requests
import re
import csv

import scipy.special.cython_special
import matplotlib.pyplot as plt

url = 'https://jenyay.net/uploads/Student/Modelling/task_02_01.txt'

r = requests.get(url = url)

with open('index.html', 'w' , encoding="utf-8") as file:
    file.write(r.text)

with open('index.html', 'r' , encoding="utf-8") as file:
    data = file.readlines()

s = re.sub("D|=|fmin|fmax|;|", "", data[12])
s1 = s.split()

D = float(s1[1])
Fmin = float(s1[2])
Fmax = float(s1[3])

c = 3*10**8
r = D/2

f = np.linspace(Fmin, Fmax, 10**4)

la = np.zeros(f.size)
k = np.zeros(f.size)
for i in range(f.size):
    la[i] = c/f[i]
    k[i] = (2*np.pi) / la[i]

# Ф-ция Бесселя первого рода
def Bess_1(i, x):
    return scipy.special.spherical_jn(i, x)
# Ф-ция Бесселя второго рода
def Bess_2(i, x):
    return scipy.special.spherical_yn(i, x)
# Ф-ция Бесселя третьего рода
def Bess_3(i, x):
    return Bess_1(i, x) + Bess_2(i, x) * 1.0j

def a_n(i, x):
    return Bess_1(i, x) / Bess_3(i, x)

def b_n(i, x):
    return (x * Bess_1(i-1, x) - i * Bess_1(i, x)) / (x * Bess_3(i-1, x) - i * Bess_3(i, x))

sigma = np.zeros(f.size)
sum = np.zeros(f.size, dtype=complex)
for i in range(f.size):
    for n in range(1, 20):
        sum[i] += (-1)**n * (n + 0.5) * (b_n(n, k[i]*r) - a_n(n, k[i]*r))
        sigma[i] = la[i]**2/np.pi * np.abs(sum[i])**2

with open("2.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, lineterminator="\r")
    file_writer.writerow(["Number", "frequency", "EPR"])
    for i in range(1, len(f)+1):
        file_writer.writerow([str(i), str(f[i-1]), str(sigma[i-1])])
plt.grid()
plt.plot(f*10**-9, sigma)
plt.show()
print(data)