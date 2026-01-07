import numpy as np
a = np.array([1, 2, 3])
b = np.array([[4, 5, 6],[7,8,9]])
c = a + b
# print(c)  # Output: [5 7 9], [8 10 12]
# print(b.ndim)
# print(b.shape)
# print(b[1,2])
# d = b[0,:]
# print(d)
# print(b)

# e  = np.array(([1,2,3,4,5,6,7,8],[9,10,11,12,13,14,15,16]))
# print(e.reshape(4,4))
# print(e[0,1:7:2])
# f =a
# f[0]   = 100
# print(a) #a gets changed kindof like pass by referenc so f=a.copy() to avoid that
# print(np.sin(a))
g = np.ones((2,3))
print(g)
h = np.full((3,2), 2)
# print(g)
i = np.matmul(g,h)
print(i)
print(np.linalg.det(i))