
# coding: utf-8

# In[10]:


import math
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.stats


# We first produce a sample:

# In[19]:


TRUE_LAMBDA = 6
X = np.random.poisson(TRUE_LAMBDA, 10000)


# For our sample, we estimate a value for $\lambda$ using MLE:

# In[24]:


def poisson_lambda_MLE(X):
    sum = 0
    for i in range(len(X)):
        sum = sum + X[i]
    value = sum / len(X)
    return value

lambda_mle = poisson_lambda_MLE(X)


# We finally plot the sample and the resulting distribution:

# In[29]:


# TODO
count, bins, ignored = plt.hist(X, 20, normed=True)
plt.show()
print("Calculated Lambda: " + str(lambda_mle))

