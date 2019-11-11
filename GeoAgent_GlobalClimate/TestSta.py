import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st


rv_unif = st.uniform.rvs(size=10)
print(rv_unif)

rv_norm=st.norm.rvs(loc = 5,scale = 1,size =(2,2))
print(rv_norm)

rv_beta=st.beta.rvs(size=10,a=4,b=2)
print(rv_beta)

x=st.norm.pdf(0,loc=0,scale=1)
y=st.norm.pdf(np.arange(3),loc=0,scale=1)
print(x)
print(y)

a=st.norm.cdf(0,loc=0,scale=1)
print(a)

x=st.norm.cdf(1.65,loc=0,scale=1)
y=st.norm.cdf(1.96,loc=0,scale=1)
z=st.norm.cdf(2.58,loc=0,scale=1)
print(x,y,z)

inv_z05=st.norm.ppf(0.05)
print(inv_z05)

z05=st.norm.cdf(inv_z05) 
print(z05)