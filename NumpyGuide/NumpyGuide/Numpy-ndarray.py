import numpy as np

b = np.arange(24).reshape(2,3,4)
print b[0,::-1,-1]
b = np.ravel(b)
print b
b.shape = (6,4)
print b
print b.transpose()