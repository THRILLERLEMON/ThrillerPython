# -*- coding: utf-8 -*-
# coding: utf-8
import chardet
import xlwt
import numpy as np
import pandas as pd
import os
import sys
# stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
# reload(sys)
# sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
# sys.setdefaultencoding('utf-8')

# 张老师安排，将黄河流域各县的数据整理到一个表格中
# 第三阶段，添加2000年之前的数据


def Findfilename(path, findstr):
    filenames = os.listdir(path)
    pxlsList = list()
    for i, filename in enumerate(filenames):
        # # 转码
        # filename = filename.decode('gbk')
        findresult = filename.find(findstr)
        if findresult != -1:
            pxlsList.append(filename)
        else:
            continue
    return pxlsList


# 以山西省晋城市为例提取的参数
# 1 能找到的对应参数，key是2000之前的参数名称，value是2000年后的参数名称
parsDic = {
    '乡镇及街道办': '乡(镇)个数',
    '村民委员会/社区居委会': '村民委员会个数',
    '土地总面积': '行政区域土地面积',
    '生产总值': '国内生产总值',
    '第一产业': '第一产业生产总值',
    '第二产业': '第二产业生产总值',
    '#工业': '工业生产总值',
    '第三产业': '第三产业生产总值',
    '人均地区生产总值': '人均国内生产总值',
    '总户数': '年末总户数',
    '单位从业人员': '年末单位从业人员数',
    '在岗职工数': '在岗职工数',
    '全社会固定资产投资': '全社会固定资产投资',
    '#城镇固定资产投资': '城镇固定资产投资',
    '一般预算收入': '地方财政一般预算收入',
    '一般预算支出': '地方财政一般预算支出',
    '城乡居民储蓄存款余额': '居民储蓄存款余额',
    '#乡村户数': '乡村户数',
    '#乡村人口数': '乡村人口',
    '乡村人口': '乡村人口',
    '#乡村人口': '乡村人口',
    '#农林牧渔业': '农林牧渔业从业人员数',
    '农林牧渔及服务业总产值': '农林牧渔服务业总产值',
    '#农业总产值': '农业产值',
    '#林业总产值': '林业产值',
    '#牧业总产值': '牧业产值',
    '#渔业总产值': '渔业产值',
    '#农林牧渔服务业': '农林牧渔服务业总产值',
    '耕地面积': '耕地面积',
    '有效灌溉面积': '有效灌溉面积',
    '农村用电量': '农村用电量',
    '农用化肥施用折纯量': '化肥使用量(折纯量)',
    '农用塑料薄膜使用量': '农用塑料薄膜使用量',
    '#地膜': '农用地膜使用量',
    '农药使用量': '农药使用量',
    '总播种面积': '农作物播种面积',
    '粮食作物播种面积': '粮食作物播种面积',
    '粮食总产量': '粮食产量',
    '油料播种面积': '油料播种面积',
    '油料总产量': '油料产量',
    '棉花播种面积': '棉花播种面积',
    '棉花总产量': '棉花产量',
    '蔬菜种植面积': '蔬菜播种面积',
    '蔬菜总产量': '蔬菜产量',
    '大牲畜年末存栏': '大牲畜年末存栏',
    '肉类总产量': '肉类总产量',
    '奶类总产量': '奶类产量',
    '禽蛋总产量': '禽蛋产量',
    '水产品产量': '水产品产量',
    '水果总产量': '园林水果产量',
    '当年造林面积': '当年造林面积',
    '城镇居民人均可支配收入': '城镇居民人均可支配收入',
    '农村居民人均纯收入': '农村居民人均纯收入',
    '#化学肥料': '化肥使用量(折纯量)',
    '公路长度': '公路里程',
    '社会消费品零售总额': '社会消费品零售总额',
    '普通中学在校学生数': '普通中学在校学生数',
    '小学在校学生数': '小学在校学生数',
    '规模以上工业企业数': '工业企业数',
    '工业企业数': '工业企业数',
    '规模以上工业总产值': '工业总产值',
    '工业总产值': '工业总产值',
    '工业增加值（现价）': '工业生产总值',
    '工业增加值': '工业生产总值',
    '工业增加值(生产法)': '工业生产总值',
    '床位数': '医院、卫生院床位数',
    '社会福利院床位数(床)': '医院、卫生院床位数',
    '总人口': '年末总人口',
    '乡村从业人员数': '乡村从业人员数',
    '农业机械总动力': '农业机械总动力',
    '家禽年末存栏数': '家禽存栏',
    '果园面积': '果园面积',
    '水田': '水田面积',
    '#非农业人口': '城镇人口',
    '#水浇地': '水浇地面积',
    '社会福利院数(个)': '各种社会福利收养性单位数',
    '旱涝保收面积': '旱涝保收面积',
    '#内资企业': '内资企业',
    '#港澳台商投资企业': '港、澳、台商投资企业',
    '#外商投资企业': '外商投资企业',
    '社会从业人数': '',
    '在岗职工平均工资': '',
    '单位GDP能耗': '',
    '单位工业增加值能耗': '',
    '#水田水浇地': '',
    '# 水田水浇地': '',
    '受灾面积': '',
    '成灾面积': '',
    '封山育林面积': '',
    '工业销售产值': '',
    '工业销售产值(当年价)': '',
    '#原煤': '',
    '#发电量': '',
    '#水泥': '',
    '#焦炭': '',
    '#高中': '',
    '人口自然增长率': '',
    '旱地': '',
    '核桃产量': '',
    '进出口总额': '',
    '外贸出口额': '',
    '人口密度': '',
    '#农业人口数': '',
    '单位GDP电耗': '',
    '建成区绿地覆盖率': '',
    '企业数': ''
}

# 2 参数对应单位
parsUni = {
    '乡镇及街道办': '个',
    '村民委员会/社区居委会': '个',
    '土地总面积': '平方公里',
    '生产总值': '万元',
    '第一产业': '万元',
    '第二产业': '万元',
    '#工业': '万元',
    '第三产业': '万元',
    '人均地区生产总值': '元/人',
    '总户数': '户',
    '单位从业人员': '人',
    '在岗职工数': '人',
    '全社会固定资产投资': '万元',
    '#城镇固定资产投资': '万元',
    '一般预算收入': '万元',
    '一般预算支出': '万元',
    '城乡居民储蓄存款余额': '万元',
    '#乡村户数': '户',
    '#乡村人口数': '万人',
    '乡村人口': '万人',
    '#乡村人口': '万人',
    '#农林牧渔业': '人',
    '农林牧渔及服务业总产值': '万元',
    '#农业总产值': '万元',
    '#林业总产值': '万元',
    '#牧业总产值': '万元',
    '#渔业总产值': '万元',
    '#农林牧渔服务业': '万元',
    '耕地面积': '公顷',
    '有效灌溉面积': '公顷',
    '农村用电量': '万千瓦时',
    '农用化肥施用折纯量': '吨',
    '农用塑料薄膜使用量': '吨',
    '#地膜': '吨',
    '农药使用量': '吨',
    '总播种面积': '公顷',
    '粮食作物播种面积': '公顷',
    '粮食总产量': '吨',
    '油料播种面积': '公顷',
    '油料总产量': '吨',
    '棉花播种面积': '公顷',
    '棉花总产量': '吨',
    '蔬菜种植面积': '公顷',
    '蔬菜总产量': '吨',
    '大牲畜年末存栏': '头',
    '肉类总产量': '吨',
    '奶类总产量': '吨',
    '禽蛋总产量': '吨',
    '水产品产量': '吨',
    '水果总产量': '吨',
    '当年造林面积': '公顷',
    '城镇居民人均可支配收入': '元',
    '农村居民人均纯收入': '元',
    '#化学肥料': '吨',
    '公路长度': '公里',
    '社会消费品零售总额': '万元',
    '普通中学在校学生数': '人',
    '小学在校学生数': '人',
    '规模以上工业企业数': '个',
    '工业企业数': '个',
    '规模以上工业总产值': '万元',
    '工业总产值': '万元',
    '工业增加值（现价）': '万元',
    '工业增加值': '万元',
    '工业增加值(生产法)': '万元',
    '床位数': '张',
    '社会福利院床位数(床)': '张',
    '总人口': '万人',
    '乡村从业人员数': '人',
    '农业机械总动力': '万千瓦',
    '家禽年末存栏数': '万只',
    '果园面积': '公顷',
    '水田': '公顷',
    '#非农业人口': '万人',
    '#水浇地': '公顷',
    '社会福利院数(个)': '个',
    '旱涝保收面积': '公顷',
    '#内资企业': '万元',
    '#港澳台商投资企业': '万元',
    '#外商投资企业': '万元',
    '社会从业人数': '万人',
    '在岗职工平均工资': '元',
    '单位GDP能耗': '吨标准煤/万元',
    '单位工业增加值能耗': '吨标准煤/万元',
    '#水田水浇地': '千公顷',
    '# 水田水浇地': '千公顷',
    '受灾面积': '公顷',
    '成灾面积': '公顷',
    '封山育林面积': '公顷',
    '工业销售产值': '万元',
    '工业销售产值(当年价)': '万元',
    '#原煤': '万吨',
    '#发电量': '万千瓦小时',
    '#水泥': '万吨',
    '#焦炭': '吨',
    '#高中': '人',
    '人口自然增长率': '‰',
    '旱地': '公顷',
    '核桃产量': '吨',
    '进出口总额': '万美元',
    '外贸出口额': '万美元',
    '人口密度': '人/平方公里',
    '#农业人口数': '人',
    '单位GDP电耗': '千瓦时/万元',
    '建成区绿地覆盖率': '%',
    '企业数': '个'
}


# shanxi
path = 'D:\\OneDrive\\SharedFile\\EXCEL 数据处理\\EXCELwork201908_linux_3RD\\Data_Shanxi'
allCountryData = pd.read_excel(
    'D:\\OneDrive\\SharedFile\\EXCEL 数据处理\\EXCELwork201908_linux_3RD\\YR_All_3RD.xlsx', sheet_name="Sheet1")
onetoN_Code = pd.read_excel(
    'D:\\OneDrive\\SharedFile\\EXCEL 数据处理\\EXCELwork201908_linux_3RD\\OnetoN_Code_3RD.xlsx', sheet_name="Code")


findresult = allCountryData[allCountryData["Province_name"] == '山西省']


# 循环每个县
for tIndex, tRow in findresult.iterrows():
    countryName = tRow["County_name"]
    thisCountryshortName = countryName[0:len(countryName) - 1]
    thisCountryCity = tRow["City_name"]
    thisCountryCityshortName = thisCountryCity[0:len(countryName) - 1]
    getCityFilename = Findfilename(path, thisCountryCityshortName)
    # 找到文件
    if not pd.isnull(getCityFilename[0]):
        # thisSheet = pd.read_excel((path + "\\" + getCityFilename[0]).encode('gbk'))
        thisSheet = pd.read_excel((path + "\\" + getCityFilename[0]))
        countryPars = thisSheet.iloc[0][5:thisSheet.columns.size]
        countryParsUnit = thisSheet.iloc[2][5:thisSheet.columns.size]
        # 循环这个市的每一个行（很多县）
        for oIndex, oRow in thisSheet.iterrows():
            ocountryName = oRow['Name-of-District-and-County']
            # 筛选出目标县的行数据
            if oIndex > 4 and thisCountryshortName == ocountryName[0:len(thisCountryshortName)]:
                timeYear = str(oRow['Temporal_Period_Begin'])[0:4]
                # 循环每个参数
                for num in range(0, countryPars.size):
                    pParStr = countryPars[num]
                    # 是需要的参数
                    if pParStr in parsDic.keys():
                        pParIndex = countryPars.index[num]
                        realParField = parsDic[pParStr] + '_' + timeYear
                        realParUnit = parsUni[pParStr]
                        pValue = thisSheet.loc[oIndex, pParIndex]
                        if pd.isnull(pValue):
                            continue
                        # 2000年之前特有的参数需要新建表头
                        if parsDic[pParStr] == '':
                            allCountryData[realParField] = None
                        # ---------------
                        # 对城区代码进行处理
                        if thisCountryCity in onetoN_Code.columns and ocountryName == thisCityNName[0]:
                            thisCityNName = onetoN_Code.loc[1:,
                                                            thisCountryCity]
                            urbanValue = 0
                            for nName in thisCityNName:
                                nfindresult = thisSheet[(thisSheet["Name-of-District-and-County"] == nName) & (
                                    thisSheet["temporal_period"] == oRow['Temporal_Period_Begin'])]
                                nValue = nfindresult[countryPars.index[num]]
                                if pd.isnull(nValue):
                                    nValue = 0
                                if str(nValue).isspace():
                                    nValue = 0
                                try:
                                    urbanValue = urbanValue+nValue
                                except:
                                    try:
                                        urbanValue = urbanValue+float(nValue)
                                    except:
                                        print('在计算'+thisCountryCity+ocountryName+'(城区)的_'+pParStr +
                                              '_时，出现问题，寻找到的'+str(nName)+'区县'+timeYear+'年的值不是一个数字，忽略这个值，请检查！')
                            if urbanValue == 0:
                                allCountryData.loc[tIndex,
                                                   realParField] = urbanValue
                        # ---------------

                        try:
                            allCountryData.loc[tIndex,
                                               realParField] = pValue
                        except:
                            print('error in set value:'+ocountryName +
                                  timeYear + '年的' + pParStr + '的值出现错误')
                        # 单位不同的参数
                        if realParUnit != countryParsUnit[num]:
                            print('得到的参数名称'+pParStr)
                            print('应该的字段名称'+realParField)
                            print('得到的单位'+str(countryParsUnit[num]))
                            print('应该的单位'+str(realParUnit))
                            print('-----------------------------------------')

    print('test')
