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


printpath = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
sys.stdout = Logger('OutLog.txt')
print(printpath)


def Findfilename(path, findstr):
    """寻找特定文件名"""
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


def is_number(s):
    """是否是数字"""
    if s == '.':
        return True
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def GetValueandUnit(pStrVandU):
    """拆分出数值和单位"""
    try:
        filterResult = filter(is_number, pStrVandU)
        number = ''.join(list(filterResult))
        unit = pStrVandU.replace(number, '')
        return float(number), unit.strip()
    except:
        return None, None


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
    # 亿* → 万*
    if pOldUnit[0] == '亿' and pNeedUnit[0] == '万':
        try:
            newValue = float(pOldValue)*10000
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 亩 → 公顷
    if pOldUnit == '亩' and pNeedUnit == '公顷':
        try:
            newValue = float(pOldValue)*(1/15)
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 亩 → 千公顷
    if pOldUnit == '亩' and pNeedUnit == '千公顷':
        try:
            newValue = float(pOldValue)*(1/15000)
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 公斤 → 吨
    if pOldUnit == '公斤' and pNeedUnit == '吨':
        try:
            newValue = float(pOldValue)*0.001
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 万亩 → 公顷
    if pOldUnit == '万亩' and pNeedUnit == '公顷':
        try:
            newValue = float(pOldValue)*666.7
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 公顷 → 平方公里
    if pOldUnit == '公顷' and pNeedUnit == '平方公里':
        try:
            newValue = float(pOldValue)*0.01
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 万斤 → 吨
    if pOldUnit == '万斤' and pNeedUnit == '吨':
        try:
            newValue = float(pOldValue)*5
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    # 人/公顷→人/平方公里
    if pOldUnit == '人/公顷' and pNeedUnit == '人/平方公里':
        try:
            newValue = float(pOldValue)*100
            return newValue, '转换成功'
        except:
            return None, '数值转换失败，可能不是个数字，未能转换！'
    return None, returnmes


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
    '年末总户数': '年末总户数',
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
    '农用化肥施用量': '化肥使用量(折纯量)',
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
    '大牲畜年末头数': '大牲畜年末存栏',
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
    '#水田': '水田面积',
    '#非农业人口': '城镇人口',
    '#水浇地': '水浇地面积',
    '社会福利院数(个)': '各种社会福利收养性单位数',
    '旱涝保收面积': '旱涝保收面积',
    '#内资企业': '内资企业',
    '内资企业': '内资企业',
    '#港澳台商投资企业': '港、澳、台商投资企业',
    '港澳台商投资企业': '港、澳、台商投资企业',
    '#外商投资企业': '外商投资企业',
    '外商投资企业': '外商投资企业',
    '农林牧渔业从业人数': '农林牧渔业从业人员数',
    '#农林牧渔业从业人数': '农林牧渔业从业人员数',
    '#农林牧渔业从业人': '农林牧渔业从业人员数',
    '森林面积': '森林面积',
    '瓜类面积': '瓜果种植面积',
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
    '#旱地': '',
    '核桃产量': '',
    '进出口总额': '',
    '外贸出口额': '',
    '人口密度': '',
    '常住人口密度': '',
    '#农业人口数': '',
    '单位GDP电耗': '',
    '建成区绿地覆盖率': '',
    '建成区绿化覆盖率': '',
    '企业数': '',
    '花椒产量': '',
    '工业企业产品销售收入': '',
    '中药材面积': '',
    '中药材产量': '',
    '#退耕造林面积': '',
    '森林覆盖率': '',
    '瓜类总产量': '',
    '人均公共绿地面积': '',
    '#国有经济': '',
    '#国有': '',
    '#集体经济': '',
    '#集体': '',
    '#其他经济类型': '',
    '#其他': '',
    '#原油': '',
    '#原油加工量': '',
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
    '年末总户数': '户',
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
    '农用化肥施用量': '吨',
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
    '大牲畜年末头数': '头',
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
    '#水田': '公顷',
    '#非农业人口': '万人',
    '#水浇地': '公顷',
    '社会福利院数(个)': '个',
    '旱涝保收面积': '公顷',
    '#内资企业': '万元',
    '内资企业': '万元',
    '#港澳台商投资企业': '万元',
    '港澳台商投资企业': '万元',
    '#外商投资企业': '万元',
    '外商投资企业': '万元',
    '农林牧渔业从业人数': '人',
    '#农林牧渔业从业人数': '人',
    '#农林牧渔业从业人': '人',
    '森林面积': '公顷',
    '瓜类面积': '公顷',
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
    '#发电量': '万千瓦时',
    '#水泥': '万吨',
    '#焦炭': '吨',
    '#高中': '人',
    '人口自然增长率': '‰',
    '旱地': '千公顷',
    '#旱地': '千公顷',
    '核桃产量': '吨',
    '进出口总额': '万美元',
    '外贸出口额': '万美元',
    '人口密度': '人/平方公里',
    '常住人口密度': '人/平方公里',
    '#农业人口数': '人',
    '单位GDP电耗': '千瓦时/万元',
    '建成区绿地覆盖率': '%',
    '建成区绿化覆盖率': '%',
    '企业数': '个',
    '花椒产量': '吨',
    '工业企业产品销售收入': '万元',
    '中药材面积': '亩',
    '中药材产量': '公斤',
    '#退耕造林面积': '亩',
    '森林覆盖率': '%',
    '瓜类总产量': '吨',
    '人均公共绿地面积': '平方米',
    '#国有经济': '亿元',
    '#国有': '万元',
    '#集体经济': '亿元',
    '#集体': '万元',
    '#其他经济类型': '亿元',
    '#其他': '万元',
    '#原油': '万吨',
    '#原油加工量': '吨',
}


# shaanxi
path = 'D:\\OneDrive\\SharedFile\\EXCEL 数据处理\\EXCELwork201908_linux_2ED\\Data_Shaanxi'
allCountryData = pd.read_excel(
    'D:\\OneDrive\\SharedFile\\EXCEL 数据处理\\EXCELwork201908_linux_2ED\\AfterSX.xlsx', sheet_name="Sheet1")
onetoN_Code = pd.read_excel(
    'D:\\OneDrive\\SharedFile\\EXCEL 数据处理\\EXCELwork201908_linux_2ED\\OnetoN_Code_2ED.xlsx', sheet_name="Code")


findresultSP = allCountryData[allCountryData["Province_name"] == '陕西省']


# 循环每个县
for tIndex, tRow in findresultSP.iterrows():
    countryName = tRow["County_name"]
    thisCountryshortName = countryName[0:len(countryName) - 1]
    thisCountryCity = tRow["City_name"]
    thisCountryCityshortName = thisCountryCity[0:len(thisCountryCity) - 1]
    getCityFilename = Findfilename(path, thisCountryCityshortName)
    if len(getCityFilename) == 0:
        continue
    # 找到文件
    print('#region 开始整理：'+thisCountryCity+'_'+countryName)
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
                        pUnit = str(countryParsUnit[num]).strip()
                        findresultSP = pUnit.find('为')
                        if findresultSP != -1:
                            print('Warning! '+thisCountryCity+'的参数：' + pParStr +
                                  '的单位是：'+pUnit+'；处理数据时CELL中没有标明单位的已经按照括号之前的单位处理,使用前请注意！')
                        pValue = thisSheet.loc[oIndex, pParIndex]
                        if pd.isnull(pValue):
                            continue
                        if pValue == '':
                            continue
                        if pValue == ' ':
                            continue
                        if pValue == '-':
                            continue
                        if pValue is None:
                            continue
                        # 2000年前特有的参数
                        if parsDic[pParStr] == '':
                            realParField = pParStr + '_' + timeYear
                        # 需要新建表头
                        if realParField not in allCountryData.columns:
                            allCountryData[realParField] = None
                        # ---------------
                        # 对城区代码进行处理
                        if thisCountryCity in onetoN_Code.columns and ocountryName == onetoN_Code.loc[0, thisCountryCity]:
                            thisCityNName = onetoN_Code.loc[1:,
                                                            thisCountryCity]
                            urbanValue = 0
                            for nName in thisCityNName:
                                nChangeValue = None
                                nChangeMes = None
                                if pd.isnull(nName):
                                    continue
                                nfindresult = thisSheet[(thisSheet["Name-of-District-and-County"] == nName) & (
                                    thisSheet["Temporal_Period_Begin"] == oRow['Temporal_Period_Begin'])]
                                if nfindresult.empty:
                                    continue
                                nValue = nfindresult[countryPars.index[num]].values[0]
                                # 单位时间段内不统一，是数字的特殊处理（直接跳出循环），不是数字的交给下文一样处理（不用跳出循环）
                                if findresultSP != -1:
                                    if is_number(str(nValue)):
                                        # 例子：公顷（1992年及以前为万亩）
                                        # 元数据描述不一定可信，此处的处理方式为，得到的值为数字，则直接按照括号前的单位处理，如果是“值+单位”的形式，则正常处理
                                        # pbeforeYear1st = pUnit.split('年')[0]
                                        # pbeforeYear=pbeforeYear1st[len(pbeforeYear1st)-4:len(pbeforeYear1st)]
                                        # pbeforeUnit1st = pUnit.split('及以前为')[1]
                                        # pbeforeUnit = pbeforeUnit1st.split('）')[0]
                                        # if pbeforeUnit == pbeforeUnit1st:
                                        #     pbeforeUnit=pbeforeUnit1st.split(')')[0]
                                        pUnitshort = pUnit.split('（')[0]
                                        if pUnitshort == pUnit:
                                            pUnitshort = pUnit.split('(')[0]
                                        if pUnitshort == pUnit:
                                            print('Error！在计算'+thisCountryCity+ocountryName+'【城区】的_'+pParStr + '_时，出现问题，寻找到的' + str(
                                                nName) + '区县' + timeYear + '年的单位有误! 忽略这个值，请检查！')
                                            print('-------------------------')
                                        else:
                                            nChangeValue, nChangeMes = Changevalue(
                                                nValue, pUnitshort, realParUnit)
                                            if nChangeMes == '转换成功':
                                                try:
                                                    urbanValue = urbanValue + nChangeValue
                                                except:
                                                    print('Error！在计算'+thisCountryCity+ocountryName+'【城区】的_'+pParStr + '_时，出现问题，寻找到的' + str(
                                                        nName) + '区县' + timeYear + '年的值有误! 忽略这个值，请检查！')
                                                    print(
                                                        '-------------------------')
                                            else:
                                                print('Error！在计算'+thisCountryCity+ocountryName+'【城区】的_'+pParStr +
                                                      '_时，出现问题，寻找到的' + str(nName) + '区县' + timeYear + '年的值有误！')
                                                print('单位未能转换，请手动转换!具体信息如下：')
                                                print(nChangeMes)
                                                print('得到的单位:'+pUnitshort)
                                                print(
                                                    '应该的单位:' + str(realParUnit))
                                                print(
                                                    '+++++++++++++++++++++++++')
                                            continue
                                # 不是数字，拆分，不需要考虑原本单位
                                if not is_number(str(nValue)):
                                    # 拆分开值和单位
                                    nsplitValue, nsplitUnit = GetValueandUnit(
                                        str(nValue))
                                    if pd.isnull(nsplitValue):
                                        continue
                                    # 转换单位
                                    nChangeValue, nChangeMes = Changevalue(
                                        nsplitValue, nsplitUnit, realParUnit)
                                    if nChangeMes == '转换成功':
                                        try:
                                            urbanValue = urbanValue + nChangeValue
                                        except:
                                            print('Error！在计算'+thisCountryCity+ocountryName+'【城区】的_'+pParStr + '_时，出现问题，寻找到的' + str(
                                                nName) + '区县' + timeYear + '年的值有误! 忽略这个值，请检查！')
                                            print('-------------------------')
                                    else:
                                        print('Error！在计算'+thisCountryCity+ocountryName+'【城区】的_'+pParStr +
                                              '_时，出现问题，寻找到的' + str(nName) + '区县' + timeYear + '年的值有误！')
                                        print('单位未能转换，请手动转换!具体信息如下：')
                                        print(nChangeMes)
                                        print('得到的单位:'+nsplitUnit)
                                        print('应该的单位:' + str(realParUnit))
                                        print('+++++++++++++++++++++++++')
                                # 是数字，再判断要不要转换单位
                                else:
                                    # 不用转换单位
                                    if realParUnit == pUnit:
                                        try:
                                            urbanValue = urbanValue + \
                                                float(nValue)
                                        except:
                                            print('Error！在计算'+thisCountryCity+ocountryName+'【城区】的_'+pParStr + '_时，出现问题，寻找到的' + str(
                                                nName) + '区县' + timeYear + '年的值有误! 忽略这个值，请检查！')
                                            print('-------------------------')
                                    # 转换单位
                                    else:
                                        nChangeValue, nChangeMes = Changevalue(
                                            nValue, pUnit, realParUnit)
                                        if nChangeMes == '转换成功':
                                            try:
                                                urbanValue = urbanValue + nChangeValue
                                            except:
                                                print('Error！在计算'+thisCountryCity+ocountryName+'【城区】的_'+pParStr + '_时，出现问题，寻找到的' + str(
                                                    nName) + '区县' + timeYear + '年的值有误，忽略这个值，请检查！')
                                                print(
                                                    '-------------------------')
                                        else:
                                            print('Error！在计算'+thisCountryCity+ocountryName+'【城区】的_'+pParStr +
                                                  '_时，出现问题，寻找到的' + str(nName) + '区县' + timeYear + '年的值有误！')
                                            print('单位未能转换，请手动转换!具体信息如下：')
                                            print(nChangeMes)
                                            print(
                                                '得到的单位:'+pUnit)
                                            print('应该的单位:' + str(realParUnit))
                                            print('+++++++++++++++++++++++++')
                            if urbanValue != 0 and pd.isnull(allCountryData.loc[tIndex, realParField]):
                                allCountryData.loc[tIndex,
                                                   realParField] = urbanValue
                            continue
                        # ---------------
                        # 处理普通区县
                        pChangeValue = None
                        pChangeMes = None
                        # 单位时间段内不统一，是数字的特殊处理（直接跳出循环），不是数字的交给下文一样处理（不用跳出循环）
                        if findresultSP != -1:
                            if is_number(str(pValue)):
                                # 例子：公顷（1992年及以前为万亩）
                                # 元数据描述不一定可信，此处的处理方式为，得到的值为数字，则直接按照括号前的单位处理，如果是“值+单位”的形式，则正常处理
                                # pbeforeYear1st = pUnit.split('年')[0]
                                # pbeforeYear=pbeforeYear1st[len(pbeforeYear1st)-4:len(pbeforeYear1st)]
                                # pbeforeUnit1st = pUnit.split('以前为')[1]
                                # pbeforeUnit = pbeforeUnit1st.split('）')[0]
                                # if pbeforeUnit == pbeforeUnit1st:
                                #     pbeforeUnit=pbeforeUnit1st.split(')')[0]
                                pUnitshort = pUnit.split('（')[0]
                                if pUnitshort == pUnit:
                                    pUnitshort = pUnit.split('(')[0]
                                if pUnitshort == pUnit:
                                    print('Error！在计算' + thisCountryCity + ocountryName + '的_' +
                                          pParStr + '_时，出现问题，寻找到的' + timeYear + '年的单位有误，忽略这个值，请检查！')
                                    print('-------------------------')
                                else:
                                    pChangeValue, pChangeMes = Changevalue(
                                        pValue, pUnitshort, realParUnit)
                                    if pChangeMes == '转换成功':
                                        try:
                                            if pd.isnull(allCountryData.loc[tIndex,realParField]):
                                                allCountryData.loc[tIndex,realParField] = pChangeValue
                                        except:
                                            print('Error！在计算'+thisCountryCity+ocountryName+'的_'+pParStr +
                                                  '_时，出现问题，寻找到的' + timeYear + '年的值有误，忽略这个值，请检查！')
                                            print('-------------------------')
                                    else:
                                        print('Error！在计算'+thisCountryCity+ocountryName+'的_' +
                                              pParStr + '_时，出现问题，寻找到的' + timeYear + '年的值有误！')
                                        print('单位未能转换，请手动转换!具体信息如下：')
                                        print(pChangeMes)
                                        print('得到的单位:'+pUnitshort)
                                        print('应该的单位:' + str(realParUnit))
                                        print('+++++++++++++++++++++++++')
                                    continue
                        # 不是数字，拆分，不需要考虑原本单位
                        if not is_number(str(pValue)):
                            # 拆分开值和单位
                            nsplitValue, nsplitUnit = GetValueandUnit(
                                str(pValue))
                            if pd.isnull(nsplitValue):
                                continue
                            # 转换单位
                            pChangeValue, pChangeMes = Changevalue(
                                nsplitValue, nsplitUnit, realParUnit)
                            if pChangeMes == '转换成功':
                                try:
                                    if pd.isnull(allCountryData.loc[tIndex,realParField]):
                                        allCountryData.loc[tIndex,realParField] = pChangeValue
                                except:
                                    print('Error！在计算'+thisCountryCity+ocountryName+'的_'+pParStr +
                                          '_时，出现问题，寻找到的' + timeYear + '年的值有误，忽略这个值，请检查！')
                                    print('-------------------------')
                            else:
                                print('Error！在计算'+thisCountryCity+ocountryName+'的_' +
                                      pParStr + '_时，出现问题，寻找到的' + timeYear + '年的值有误！')
                                print('单位未能转换，请手动转换!具体信息如下：')
                                print(pChangeMes)
                                print('得到的单位:'+nsplitUnit)
                                print('应该的单位:' + str(realParUnit))
                                print('+++++++++++++++++++++++++')
                        # 是数字，再判断要不要转换单位
                        else:
                            # 不用转换单位
                            if realParUnit == pUnit:
                                try:
                                    if pd.isnull(allCountryData.loc[tIndex,realParField]):
                                        allCountryData.loc[tIndex,realParField] = pChangeValue
                                except:
                                    print('Error！在计算'+thisCountryCity+ocountryName+'的_'+pParStr +
                                          '_时，出现问题，寻找到的' + timeYear + '年的值有误，忽略这个值，请检查！')
                                    print('-------------------------')
                            # 转换单位
                            else:
                                pChangeValue, pChangeMes = Changevalue(
                                    pValue, pUnit, realParUnit)
                                if pChangeMes == '转换成功':
                                    try:
                                        if pd.isnull(allCountryData.loc[tIndex,realParField]):
                                            allCountryData.loc[tIndex,realParField] = pChangeValue
                                    except:
                                        print('在计算'+thisCountryCity+ocountryName+'的_'+pParStr +
                                              '_时，出现问题，寻找到的' + timeYear + '年的值有误，忽略这个值，请检查！')
                                        print('-------------------------')
                                else:
                                    print('Error！在计算'+thisCountryCity+ocountryName+'的_' +
                                          pParStr + '_时，出现问题，寻找到的' + timeYear + '年的值有误！')
                                    print('单位未能转换，请手动转换!具体信息如下：')
                                    print(pChangeMes)
                                    print('得到的单位:'+pUnit)
                                    print('应该的单位:' + str(realParUnit))
                                    print('+++++++++++++++++++++++++')
    print('##################################################')
    print('#endregion')
allCountryData.to_excel(
    'D:\\OneDrive\\SharedFile\\EXCEL 数据处理\\EXCELwork201908_linux_2ED\\AfterSX_SaX.xlsx', encoding='gbk')
print('Already Finish Work! Good! THRILLER柠檬！')
