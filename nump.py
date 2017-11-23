from numpy import linalg, array, hsplit
from numpy import loadtxt, savetxt
import re

#help(linalg.det)


savetxt("mat.data", [[1,2],[3,4]])
mat = loadtxt("mat.data")
print(mat)
print(linalg.det(mat))
print(linalg.inv(mat))

savetxt("mat.coeffs", [[3,1], [1,2], [9,8]])
coe = loadtxt("mat.coeffs")
print(coe)
a = [coe[0], coe[1]]
b = coe[2]
x = linalg.solve(a, b)
print(x)

print('*'*30)

# some simple parsing. like. very simple.
# also this whole thing is inefficient & ugly AF (:

str1 = "2 x + 3y -1 = 5"
str2 = "x-y =     0"

m = re.findall('(-*\+*=*\d*[a-z]?)', str1.replace(' ', ''))
n = re.findall('(-*\+*=*\d*[a-z]?)', str2.replace(' ', ''))
print(m)
res = [[],[]]
coeffs = []
for item in m:
    if not item or item == '':
        continue
    elif item[0] == '=':  # vysledok
        res[0].append(item[1:])
        coeffs.append('=')
    elif not item[-1].isalpha():
        res[0].append(item)
        coeffs.append('.')  # absolutny clen
    else:
        res[0].append(item[0:-1])
        coeffs.append(item[-1])

res[1] = [''] * len(coeffs)

has_abs = False  # search for constant term
for i in range(len(coeffs)):
    c = coeffs[i]
    if c.isalpha():
        for item in n:
            if item.endswith(c):
                res[1][i] = item[0:-1]
    elif c == '=':
        for item in n:
            if item and item[0] == '=':
                res[1][i] = item[1:]
    elif c == '.':
        for item in n:
            if item and not item[0] == '=' and not item[-1].isalpha():
                has_abs = True
                res[1][i] = item
        if not has_abs:
            res[1][i] = '0'

res[1] = [x.replace('-','-1').replace('+','1') for x in res[1]]
res[1] = [(lambda x: '1' if x == '' else x)(x) for x in res[1]]

# move constants to result
for i in range(len(coeffs)):
    if coeffs[i] == '.':
        coeffs = [c for c in coeffs if not c == '.']

        for r in res:
            r[-1] = int(r[-1])
            r[-1] -= int(r[i])
        res = [r[0:i] + r[i + 1:] for r in res]

        break


print(res)

a = [[int(c) for c in coe[0:-1]] for coe in res]
print(a)
b = [int(coe[-1]) for coe in res]
print(b)
x = linalg.solve(a, b)
ret = 'solution: '
for i in range(len(x)):
    str = '%c = %f  ' % (coeffs[i], x[i])
    ret += str
print(ret)

#numpy.hsplit
