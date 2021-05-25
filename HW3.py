import numpy as np
import math
import matplotlib.pyplot as plt


l = 8
t0 = 1.6
step = 0.1
tmax = 3.3

def spin_matrix(l):
    s = np.random.randint(1, 4, (l, l))
    s = np.array(s)
    return s


def temperature(t0, l):
    t = t0
    u = []
    c = []
    etpers = []
    while t < tmax:
        print(t)
        s = spin_matrix(l)
        w = 1 - math.exp(-2/t)
        q = 0
        # to equilibrium
        k = 0
        while k < 10 * t:
            # print(k)
            a = cluster(s, w, l)
            s = flip_spin(s, a)
            k += 1
        m = []
        e = 0
        etot = 0
        etot2 = 0
        while q < 100 * t:
            # print(q)

            # hidden circle
            h = 0
            while h < l ** 2:
                a = cluster(s, w, l)
                s = flip_spin(s, a)
                h += 1

            a = cluster(s, w, l)
            s = flip_spin(s, a)
            p = np.random.sample()
            if p >= 0.5:
                s = flip_spin(s, a)
            # вывод данных для итерации

            en = 0
            for i in range(l-1):
                for j in range(l-1):
                    if s[i][j] == s[i+1][j]:
                        en += 1
                    else:
                        en -= 1
            for i in range(l-1):
                en += [s[l-1][i] * s[l-1][i+1]]
                en += [s[i][l-1] * s[i+1][l-1]]

            m += [sum(sum(s))/(l**2)]
            etot += en
            etot2 += en**2
            e += en/(l ** 2)
            q += 1

        # вывод данных для температуры
        m = np.array(m)
        etot = np.array(etot)
        e = np.array(e)
        etot2 = etot2/q
        etot1 = etot/q

        m2 = sum(m**2)/len(m)
        m4 = sum(m**4)/len(m)

        c += [(etot2 - etot1**2) / (t**2 * l**2)]
        u += [1 - m4 / (3 * (m2**2))]
        etpers += [e/q]
        t += step
    return c, u, etpers







def cluster(s, w, l):
    a = []
    row = np.random.randint(0, l)
    col = np.random.randint(0, l)
    a = np.array([[row, col]])
    n = 0
    chek = np.ones((l, l))
    chek[row][col] = 0
    while n < len(a):
        # print(n)
        if n == 0 or len(a) == 1:
            i = row
            j = col
        else:
            i = int(a[n][0])
            j = int(a[n][1])
        n += 1
        for di in range(-1, 2):
            for dj in range(-1, 2):
                pc = np.random.sample()
                ai = i + di
                aj = j + dj

                if 0 <= ai <= l-1 and 0 <= aj <= l-1:

                    if s[i][j] == s[ai][aj] and pc < w and chek[ai][aj] != 0:
                        a = np.vstack([a, [ai, aj]])
                        chek[ai][aj] = 0
    return a

def flip_spin(s,a):
    for i in range(len(a)):
        si = a[i][0]
        sj = a[i][1]
        s[si][sj] = -s[si][sj]
    return s

[c , u, etpers] = temperature(t0, l)
# print(c, u, etpers)


x = np.arange(t0, tmax, step)
x = np.array(x)
xinv = x**(-1)
plt.figure(1)
plt.plot(x, u)
plt.figure(2)
plt.plot(xinv, c)
plt.figure(3)
plt.plot(xinv, etpers)
plt.show()
