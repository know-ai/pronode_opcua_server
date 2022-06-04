# Python code demonstrate creating
# DataFrame from dict narray / lists
# By default addresses.
 
import pandas as pd
import random
 
# initialize data of lists.
n = 20
data = {'PT_01': [random.uniform(0.0, 10.0)for i in range(n)],
        'PT_02': [random.uniform(0.0, 10.0)for i in range(n)],
        'FT_01': [random.uniform(0.0, 10.0)for i in range(n)],
        'FT_02': [random.uniform(0.0, 10.0)for i in range(n)]}
 
# Create DataFrame
df = pd.DataFrame(data)
df.to_pickle('data.pkl')

