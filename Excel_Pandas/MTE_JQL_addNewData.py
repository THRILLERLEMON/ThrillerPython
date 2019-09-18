# MTE work;add new train data to xlsx
# Windows 10 1903
# 2019.9.16
# JiQiulei thrillerlemon@outlook.com

import pandas as pd


oldtable = pd.read_excel(
    'E:\\OFFICE\\MTE_NEE_DATA\\GRA_Train_NEE_5.xlsx', sheet_name="All", encoding='gbk')

gsocMon = pd.read_excel(
    'E:\\OFFICE\\MTE_NEE_DATA\\addNewData.xlsx', sheet_name="GSOC")
maMon = pd.read_excel(
    'E:\\OFFICE\\MTE_NEE_DATA\\addNewData.xlsx', sheet_name="Manure_Application")
nfaMon = pd.read_excel(
    'E:\\OFFICE\\MTE_NEE_DATA\\addNewData.xlsx', sheet_name="Nfertilizer_Application")
nhxMon = pd.read_excel(
    'E:\\OFFICE\\MTE_NEE_DATA\\addNewData.xlsx', sheet_name="NHx_N_Deposition")
noyMon = pd.read_excel(
    'E:\\OFFICE\\MTE_NEE_DATA\\addNewData.xlsx', sheet_name="NOy_N_Deposition")

print(gsocMon)