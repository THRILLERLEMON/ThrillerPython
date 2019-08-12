import os
import pandas as pd
import numpy as np
onetoN_Code=pd.read_excel('C:\\Users\\thril\\Desktop\\EXCELwork201908\\OnetoN_Code.xlsx', sheet_name='Code')
#0-17
# print(onetoN_Code.columns)
result=onetoN_Code.loc[:,620102]
print(result)
# for cn,codeOne in enumerate(onetoN_Code.columns):
#     print(onetoN_Code.loc[:,str(codeOne)])
#     print(cn)
# if 620102 in onetoN_Code.columns:
    
# print(onetoN_Code.iloc[:,0].name)
print('test ok')