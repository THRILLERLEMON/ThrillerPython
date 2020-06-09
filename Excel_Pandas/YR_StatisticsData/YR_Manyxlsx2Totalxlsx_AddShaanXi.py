# -*- coding: utf-8 -*-
# coding: utf-8
import chardet
import xlwt
import time
import numpy as np
import pandas as pd
import os
import sys


# stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
# reload(sys)
# sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
# sys.setdefaultencoding('utf-8')

# 张老师安排，将陕西省新增的各县的数据加到之前的结果中
# 创建于2020年4月22日

# 输出print内容
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


# printpath = os.path.abspath(os.path.dirname(__file__))
printpath = os.path.abspath('C://Users//thril//Desktop')
type = sys.getfilesystemencoding()
sys.stdout = Logger('OutLog.txt')
print(printpath)

print(time.strftime('%H:%M:%S', time.localtime(time.time())))


def FindXLSfile(parstr, path):
    filenames = os.listdir(path)
    pxlsList = list()
    for i, filename in enumerate(filenames):
        # 转码
        # filename = filename.decode('gbk')
        findresult = filename.find(parstr)
        if findresult != -1:
            pxlsList.append(filename)
        else:
            continue
    return pxlsList


def Changevalue(pOldValue, pOldUnit, pNeedUnit):
    """转换单位"""
    returnmes = '单位特殊，未能转换！'
    # 不用转换
    if pOldUnit == pNeedUnit:
        return float(pOldValue), '转换成功'
    # * → 万*
    if pNeedUnit == '万' + pOldUnit:
        try:
            newValue = float(pOldValue) / 10000
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # * → 千*
    if pNeedUnit == '千' + pOldUnit:
        try:
            newValue = float(pOldValue) / 1000
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 万* → *
    if pOldUnit == '万' + pNeedUnit:
        try:
            newValue = float(pOldValue) * 10000
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 千* → *
    if pOldUnit == '千' + pNeedUnit:
        try:
            newValue = float(pOldValue) * 1000
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 千* → 万*
    if pOldUnit[0] == '千' and pNeedUnit[0] == '万':
        try:
            newValue = float(pOldValue) / 10
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 千* → 亿*
    if pOldUnit[0] == '千' and pNeedUnit[0] == '亿':
        try:
            newValue = float(pOldValue) / 100000
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 万* → 千*
    if pOldUnit[0] == '万' and pNeedUnit[0] == '千':
        try:
            newValue = float(pOldValue) * 10
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 百* → 万*
    if pOldUnit[0] == '百' and pNeedUnit[0] == '万':
        try:
            newValue = float(pOldValue) / 100
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 万* → 亿*
    if pOldUnit[0] == '万' and pNeedUnit[0] == '亿':
        try:
            newValue = float(pOldValue) / 10000
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 亿* → 万*
    if pOldUnit[0] == '亿' and pNeedUnit[0] == '万':
        try:
            newValue = float(pOldValue) * 10000
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 亩 → 公顷
    if pOldUnit == '亩' and pNeedUnit == '公顷':
        try:
            newValue = float(pOldValue) * (1 / 15)
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 亩 → 公顷
    if pOldUnit == '公顷' and pNeedUnit == '亩':
        try:
            newValue = float(pOldValue) * (15)
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 亩 → 千公顷
    if pOldUnit == '亩' and pNeedUnit == '千公顷':
        try:
            newValue = float(pOldValue) * (1 / 15000)
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 公斤 → 吨
    if pOldUnit == '公斤' and pNeedUnit == '吨':
        try:
            newValue = float(pOldValue) * 0.001
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 吨 → 公斤
    if pOldUnit == '吨' and pNeedUnit == '公斤':
        try:
            newValue = float(pOldValue) * 1000
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 万亩 → 公顷
    if pOldUnit == '万亩' and pNeedUnit == '公顷':
        try:
            newValue = float(pOldValue) * 666.7
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 万亩 → 千公顷
    if pOldUnit == '万亩' and pNeedUnit == '千公顷':
        try:
            newValue = float(pOldValue) * 0.6667
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 公顷 → 平方公里
    if pOldUnit == '公顷' and pNeedUnit == '平方公里':
        try:
            newValue = float(pOldValue) * 0.01
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 万斤 → 吨
    if pOldUnit == '万斤' and pNeedUnit == '吨':
        try:
            newValue = float(pOldValue) * 5
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 人/公顷→人/平方公里
    if pOldUnit == '人/公顷' and pNeedUnit == '人/平方公里':
        try:
            newValue = float(pOldValue) * 100
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 担→吨
    if pOldUnit == '担' and pNeedUnit == '吨':
        try:
            newValue = float(pOldValue) * 0.05
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 市担→吨
    if pOldUnit == '市担' and pNeedUnit == '吨':
        try:
            newValue = float(pOldValue) * 0.05
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    return None, returnmes


def FindValue(parstr, pFileList, pCountryCode, pYear):
    for file in pFileList:
        # print("查找 " + str(pCountryCode) + "县" +
        #       str(pYear) + " 年" + parstr + " in " + str(file))
        thisSheet = pd.read_excel((path + "/" + file).encode('gbk'))
        verifyStr = thisSheet.iloc[0, 10]
        if parstr == verifyStr:
            findresult = thisSheet[
                (thisSheet["county_code"] == int(pCountryCode))
                & (thisSheet["temporal_period"] == pYear)
                ].copy()
            if findresult.empty is True:
                continue
            else:
                # print(findresult.iloc[0])
                # print(findresult.iloc[0, 10])
                if not pd.isnull(findresult.iloc[0, 10]):
                    return findresult.iloc[0, 10]
                # else:
                # print("find one it is " + str(findresult.iloc[0, 10]))
                # print ("find a empty")
        else:
            includOrNot = file.find(parstr)
            if includOrNot == -1:
                print(file + " has something wrong")


def getNewpart(newfile):
    samepart = newfile.iloc[:, 0:12]
    newpart = newfile.drop(samepart, axis=1)
    return newpart


def getJINGcol(plistCol):
    pFalseColList = list()
    for col in plistCol:
        if str(col).find('#') == 0:
            pFalseColList.append(str(col))
    return pFalseColList


# # path='/home/JiQiulei/EXCELwork201908/data'
# path = '/home/JiQiulei/EXCELwork_V2/Data'
# allCountryData = pd.read_excel(
#     '/home/JiQiulei/EXCELwork_V2/YR_All.xlsx', sheet_name="Sheet1")
# onetoN_Code = pd.read_excel(
#     '/home/JiQiulei/EXCELwork_V2/OnetoN_Code.xlsx', sheet_name="Code")


# 参量_年份
parszhang = ["城镇人口", "乡村人口", "国内生产总值", "第一产业生产总值", "第二产业生产总值",
             "第三产业生产总值", "工业生产总值", "大牲畜年末存栏", "年末生猪存栏", "羊年末存栏只数", "有效灌溉面积"]
pars1 = ['乡(镇)个数', '建制镇个数', '村民委员会个数', '自来水受益村', '通电话村数',
         '年末总人口', '女性人口', '男性人口', '当年出生人口', '当年死亡人口']
pars2 = ['常住人口', '年末总户数', '乡村户数', '第二产业从业人员数', '第三产业从业人员',
         '年末单位从业人员数', '国有单位从业人员', '城镇集体单位从业人员数', '其他单位从业人员数', '乡村从业人员数']
pars3 = ['农林牧渔业从业人员数', '城镇登记失业人员数', '工业总产值', '人均国内生产总值',
         '地方财政一般预算收入', '各项税收', '地方财政一般预算支出', '一般性公共服务支出', '农林水事务支出']
pars4 = ['科学技术支出', '医疗卫生支出', '教育支出', '年末金融机构各项存款余额', '居民储蓄存款余额',
         '年末金融机构各项贷款余额', '农林牧渔业总产值', '农业产值', '林业产值', '牧业产值', '渔业产值']
pars5 = ['农林牧渔服务业总产值', '农业机械总动力',
         '化肥使用量(折纯量)', '农药使用量', '农用塑料薄膜使用量', '农村用电量', '旱涝保收面积', '机耕面积', '机电排灌面积', '农作物播种面积']
pars6 = ['粮食作物播种面积', '稻谷播种面积', '小麦播种面积', '玉米播种面积', '豆类作物播种面积',
         '大豆播种面积', '薯类作物播种面积', '油料播种面积', '棉花播种面积', '蔬菜播种面积']
pars7 = ['瓜果种植面积', '果园面积', '粮食产量', '小麦产量', '玉米产量', '豆类产量', '大豆产量', '薯类产量', '油料产量', '棉花产量',
         '蔬菜产量', '园林水果产量', '苹果产量', '肉类总产量', '牛肉产量', '羊肉产量', '猪肉产量', '牛年末存栏头数', '奶类产量', '禽蛋产量']
pars8 = ['公路里程', '年末邮电局(所)数', '电信业务总量', '固定电话用户', '农村电话用户', '移动电话用户',
         '互联网宽带接入用户', '社会消费品零售总额', '城镇社会消费品零售总额', '乡村社会消费品零售总额']
pars9 = ['迁入人口合计', '省内迁入人口', '省外迁入人口', '迁出人口合计', '迁往省内人口',
         '迁往省外人口', '农林牧渔业增加值', '农业增加值', '林业增加值', '牧业增加值']
pars10 = ['水产品产量', '工业企业数', '工业总产值(现价)', '从业人员年平均数', '主营业务收入',
          '本年应交增值税', '利润总额', '建筑业企业个数', '期末从业人员数', '建筑业总产值']
pars11 = ['商品房屋销售额', '普通中学数', '小学数', '普通中学专任教师数', '小学专任教师数', '普通中学在校学生数',
          '小学在校学生数', '剧场、影剧院数', '公共图书馆图书总藏量', '医院、卫生院数', '医院、卫生院床位数']
pars12 = ['全社会固定资产投资', '新增固定资产投资', '建成区面积', '环境污染治理本年完成投资总额',
          '全社会用电量', '城镇固定资产投资', '房地产开发投资', '住宅开发投资', '商品房屋销售面积']
pars13 = ['城镇基本养老保险参保人数', '城镇基本医疗保险参保人数', '失业保险参保人数', '城镇居民最低生活保障人数',
          '农村居民最低生活保障人数', '新型农村合作医疗参保人数', '新型农村社会养老保险参保人数', '行政区域土地面积', '森林面积', '当年造林面积']
pars14 = ['医院、卫生院卫生技术人员数', '执业(助理)医师', '城镇在岗职工平均人数', '城镇在岗职工工资总额', '城镇居民人均可支配收入',
          '农村居民人均纯收入', '农村居民人均生活消费支出', '农民人均住房面积', '各种社会福利收养性单位数', '各种社会福利收养性单位床位数']
pars15 = ['耕地面积', '水田面积', '水浇地面积', '基建占地面积', '年内减少耕地面积',
          '家禽存栏', '在岗职工数', '工业二氧化硫排放量', '烟(粉)尘排放量', '氮氧化物排放量']
pars16 = ['年末耕地总资源', '退耕还林还草面积', '邮政业务总量', '邮电业务总量',
          '高等级公路里程', '农用地膜使用量', '城镇生活污水处理率', '污水处理厂数', '垃圾处理站数']
pars17 = ['全社会从业人员数', '第一产业从业人员数', '内资企业', '港、澳、台商投资企业', '外商投资企业',
          '流动资产合计', '出口总额', '当年实际使用外资金额', '小学学龄儿童净入学率', '油菜播种面积']
pars18 = ['稻谷产量', '茶叶产量', '蚕茧产量', '固定资产净值', '主营业务税金及附加',
          '工业用电量', '居民生活用电量', '进口总额', '新增固定资产', '体育场馆数']
pars19 = ['5岁以下儿童死亡率', '婴儿死亡率', '产妇住院分娩比例', '渔业增加值', '农林牧渔服务业增加值', '通有线电视村数']

pars20 = ['氮氧化物排放量', '通宽带村数', '农业人口', '非农业人口', '人口密度', '城镇化率', '人口出生率', '人口死亡率', '人口自然增长率',
          '在岗职工年末人员数', '国有单位在岗职工人员数', '城镇集体单位在岗职工人员数', '其他单位在岗职工人员数',
          '单位从业人员工资总额', '单位从业人员平均工资', '城镇在岗职工平均工资', '农村家庭工业从业人员数',
          '农村家庭建筑业从业人员数', '建筑业生产总值', '农林牧渔业增加值', '农林牧渔服务业增加值',
          '柴油机动力', '汽油机动力', '电动机动力', '大中型农用拖拉机数', '大中型农用拖拉机动力', '小型农用拖拉机数',
          '小型农用拖拉机数动力', '大中型拖拉机配套农具数', '小型拖拉机配套农具数', '氮肥施用折纯量',
          '磷肥施用折纯量', '钾肥施用折纯量', '复合肥施用折纯量', '化肥施用量(实物量)', '氮肥施用实物量',
          '磷肥施用实物量', '钾肥施用实物量', '复合肥施用实物量', '地膜覆盖面积', '机械播种面积',
          '机械收获面积', '苹果面积', '马铃薯播种面积', '中药材面积', '油菜籽产量', '马铃薯产量', '中药材产量', '奶牛年末存栏数',
          '牛奶产量', '蜂蜜产量', '羊毛产量', '羊绒产量', '水产养殖面积', '工业增加值', '工业销售产值(现价)',
          '资产合计', '利税总额', '职业中学数', '职业中学在校学生数', '职业中学专任教师数', '幼儿园数',
          '在园幼儿数', '幼儿园专任教师数', '卫生机构数', '卫生机构床位数', '卫生机构卫生技术人员',
          '卫生机构执业(助理)医师', '卫生机构注册护师、护士', '村级卫生室数', '乡村医生和卫生员数', '旱地面积']

# allCountryData = pd.read_excel('E:\\OFFICE\\EXCEL 数据处理\\新增陕西全省\\主数据体1.5addShaanXi.xlsx', sheet_name="Sheet1")
# falseCollist=getJINGcol(list(allCountryData.columns))
# for col in falseCollist:
#     corColName=col[1:len(col)]
#     allCountryData.rename(columns={col: corColName}, inplace=True)
#
# # 生成表头
# for i, pars in enumerate([pars1,pars2,pars3,pars4,pars5,pars6,pars7,pars8,pars9,pars10,pars11,pars12,pars13,pars14,pars15,pars16,pars17,pars18,pars19,pars20]):
#     for i, par in enumerate(pars):
#         for yearn in np.arange(1990, 2019, 1):
#             filedname = par + "_" + str(yearn)
#             a=list(allCountryData.columns)
#             if filedname in list(allCountryData.columns):
#                 continue
#             else:
#                 allCountryData[filedname] = None
#
# firstpart = allCountryData.iloc[:, 0:12]
# newpart = getNewpart(allCountryData)
#
# newpartsort = newpart.sort_index(axis=1)
# newtable = pd.concat([firstpart, newpartsort], axis=1)
# # # 删除值全部为空的列
# # # 返回一个bool型数组
# # col = newtable.count() == 0
# # for i in range(len(col)):
# #     if col[i]:
# #         newtable.drop(labels=col.index[i], axis=1, inplace=True)
# # countnumber = newtable.count()
# # baifenbi = countnumber / 379
# # newtable = newtable.append(countnumber, ignore_index=True).append(
# #     baifenbi, ignore_index=True)
# # print(newtable)
# for i, par in enumerate(parszhang):
#     for yearn in np.arange(1990, 2019, 1):
#         filedname = par + "_" + str(yearn)
#         a=list(newtable.columns)
#         if filedname in list(newtable.columns):
#             continue
#         else:
#             newtable[filedname] = None
# newtable.to_excel('C:/Users/thril/Desktop/NEWShaanXi_Ordered.xlsx')
# print('ok')


# path='E:\\OFFICE\\EXCEL 数据处理\\新增陕西全省\\ShaanXiALLexcel'
# dfOut = pd.DataFrame(columns=['字段', '单位'])
# for i, par in enumerate(pars20):
#     sheetList = FindXLSfile(par, path)
#     for n,sheetName in enumerate(sheetList):
#         thisSheet=pd.read_excel(path+'\\'+sheetList[n])
#         verifyStr = thisSheet.iloc[0, 10]
#         if (par == verifyStr) | (par+'数' == verifyStr):
#             dic = {'字段': verifyStr,
#                    '单位': thisSheet.iloc[2, 10],
#                    }
#             dfOut = dfOut.append(dic, ignore_index=True)
#             continue
#         else:
#              if n==0:
#                  print(par + "maybe has something wrong,please chexk it")
#                  continue
#              else:
#                  print(par + "maybe has 2 excel can use,you can check it")
#                  continue
# dfOut.to_excel('C:/Users/thril/Desktop/Units.xlsx')
# print('already output Units')


# 2 参数对应单位
parsUni = {
    '中药材面积': '亩',
    '中药材产量': '公斤',
    '大牲畜年末存栏': '万头',
    '年末生猪存栏': '万头',
    '羊年末存栏只数': '万只',
}

path = 'E:\\OFFICE\\EXCEL 数据处理\\新增陕西全省\\ShaanXiALLexcel'
allCountryData = pd.read_excel('E:\\OFFICE\\EXCEL 数据处理\\新增陕西全省\\NEWShaanXi_Ordered.xlsx', sheet_name="Sheet1")
shaanXiAllCountryData = allCountryData[(allCountryData["ShaanXiNeed"] == 1)].copy()
shaanXiAllCountryData = shaanXiAllCountryData.reset_index(drop=True)
otherAllCountryData = allCountryData[(allCountryData["ShaanXiNeed"] == 0)].copy()
for i, pars in enumerate(
        [parszhang, pars1, pars2, pars3, pars4, pars5, pars6, pars7, pars8, pars9, pars10, pars11, pars12, pars13,
         pars14, pars15, pars16, pars17, pars18, pars19, pars20]):
    for i, par in enumerate(pars):
        sheetList = FindXLSfile(par, path)
        for n, sheetName in enumerate(sheetList):
            thisSheet = pd.read_excel(path + '\\' + sheetList[n])
            verifyStr = thisSheet.iloc[0, 10]
            if (par == verifyStr) | (par + '数' == verifyStr):
                for c, oneCountryCode in enumerate(shaanXiAllCountryData.loc[:, "County_code_N"]):
                    for yearn in np.arange(2001, 2017, 1):
                        filedname = par + "_" + str(yearn)
                        if pd.isnull(shaanXiAllCountryData.loc[c, filedname]):
                            findresult = thisSheet[
                                (thisSheet["county_code"] == int(oneCountryCode))
                                & (thisSheet["temporal_period"] == yearn)
                                ].copy()
                            if findresult.empty is True:
                                continue
                            else:
                                findValue = findresult.iloc[0, 10]
                                if not pd.isnull(findValue):
                                    try:
                                        if verifyStr in list(parsUni.keys()):
                                            nChangeValue, nChangeMes = Changevalue(
                                                findValue, str(thisSheet.iloc[2, 10]), parsUni[verifyStr])
                                            if nChangeMes == '转换成功':
                                                shaanXiAllCountryData.loc[c, filedname] = nChangeValue
                                            else:
                                                print('单位未能转换，请手动转换!具体信息如下：')
                                                print(findValue, str(thisSheet.iloc[2, 10]), parsUni[verifyStr])
                                        else:
                                            shaanXiAllCountryData.loc[c, filedname] = findValue
                                    except:
                                        print('在获取' + str(oneCountryCode) + '_' + str(yearn) + '年的_' + par +
                                              '_时，出现问题，请检查！')
                        else:
                            continue
                continue
            else:
                if n == 0:
                    print(par + "maybe has something wrong,please chexk it")
                    continue
                else:
                    print(par + "maybe has 2 excel can use,you can check it")
                    continue
        print('finish ' + par)
        print(time.strftime('%H:%M:%S', time.localtime(time.time())))
newData = pd.concat([shaanXiAllCountryData, otherAllCountryData], axis=0, ignore_index=True)
newData.to_excel('C:/Users/thril/Desktop/result.xlsx')
print('Already Finish Work! Good! THRILLER柠檬！')
