import pandas as pd
df = pd.DataFrame({'ID': [1, 2, 3], 'name': ['one', 'two', 'three']})
df.to_excel('C:/Users/thril/Desktop/output.xlsx')
print(df.shape)
print(df.columns)
print(df.head())
print('Done')
