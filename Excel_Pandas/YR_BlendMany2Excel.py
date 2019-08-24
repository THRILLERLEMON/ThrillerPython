# -*- coding: utf-8 -*-
import pandas as pd


def getNewpart(filename):
    newfile = pd.read_csv(filename, encoding='gbk')
    samepart = newfile.iloc[:, 0:11]
    newpart = newfile.drop(samepart, axis=1)
    return newpart


newXlsx_parszhang = pd.read_csv(
    'C:\\Users\\thril\\Desktop\\TEST\\newXlsx_parszhang.csv', encoding='gbk')
newpart1 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars1.csv')
newpart2 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars2.csv')
newpart3 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars3.csv')
newpart4 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars4.csv')
newpart5 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars5.csv')
newpart6 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars6.csv')
newpart7 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars7.csv')
newpart8 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars8.csv')
newpart9 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars9.csv')
newpart10 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars10.csv')
newpart11 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars11.csv')
newpart12 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars12.csv')
newpart13 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars13.csv')
newpart14 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars14.csv')
newpart15 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars15.csv')
newpart16 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars16.csv')
newpart17 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars17.csv')
newpart18 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars18.csv')
newpart19 = getNewpart('C:\\Users\\thril\\Desktop\\TEST\\newXlsx_pars19.csv')

out = pd.concat([newXlsx_parszhang, newpart1, newpart2, newpart3, newpart4, newpart5, newpart6, newpart7, newpart8,
                 newpart9, newpart10, newpart11, newpart12, newpart13, newpart14, newpart15, newpart16, newpart17, newpart18, newpart19], axis=1, sort=False)

out.to_excel('C:/Users/thril/Desktop/OutputAll.xlsx')
print('ok')
