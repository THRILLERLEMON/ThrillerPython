# -*- coding: utf-8 -*-
# coding: utf-8
import chardet
import xlwt
import numpy as np
import pandas as pd
import os
import sys
stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
reload(sys)
sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
sys.setdefaultencoding('utf-8')

# 张老师安排，将黄河流域各县的数据整理到一个表格中
# 创建于2019年8月10日


def Findfilenames(path, parstr):
    filenames = os.listdir(path)
    pxlsList = list()
    for i, filename in enumerate(filenames):
        # 转码
        filename = filename.decode('gbk')
        findresult = filename.find(parstr)
        if findresult != -1:
            pxlsList.append(filename)
        else:
            continue
    return pxlsList


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
                print(file+" has something wrong")


# path='/home/JiQiulei/EXCELwork201908/data'
path = '/home/JiQiulei/EXCELwork_V2/Data'
allCountryData = pd.read_excel(
    '/home/JiQiulei/EXCELwork_V2/YR_All.xlsx', sheet_name="Sheet1")
onetoN_Code = pd.read_excel(
    '/home/JiQiulei/EXCELwork_V2/OnetoN_Code.xlsx', sheet_name="Code")


# 参量_年份
parszhang = ["城镇人口", "乡村人口", "国内生产总值", "第一产业生产总值", "第二产业生产总值",
             "第三产业生产总值", "工业生产总值", "大牲畜年末存栏", "年末生猪存栏", "羊年末存栏只数", "有效灌溉面积"]
pars1 = ['乡(镇)个数', '建制镇个数', '村民委员会个数', '自来水受益村', '通电话村数',
         '年末总人口', '女性人口', '男性人口', '当年出生人口', '当年死亡人口']
pars2 = ['常住人口', '年末总户数', '乡村户数', '第二产业从业人员数', '第三产业从业人员',
         '年末单位从业人员数', '国有单位从业人员', '城镇集体单位从业人员数', '其他单位从业人员数', '乡村从业人员数']
pars3 = ['农林牧渔业从业人员数', '城镇登记失业人员数', '工业总产值',  '人均国内生产总值',
         '地方财政一般预算收入', '各项税收', '地方财政一般预算支出', '一般性公共服务支出', '农林水事务支出']
pars4 = ['科学技术支出', '医疗卫生支出', '教育支出', '年末金融机构各项存款余额', '居民储蓄存款余额',
         '年末金融机构各项贷款余额', '农林牧渔业总产值', '农业产值', '林业产值', '牧业产值', '渔业产值']
pars5 = ['农林牧渔服务业总产值', '农业机械总动力',
         '化肥使用量(折纯量)', '农药使用量', '农用塑料薄膜使用量', '农村用电量',  '旱涝保收面积', '机耕面积', '机电排灌面积', '农作物播种面积']
pars6 = ['粮食作物播种面积', '稻谷播种面积', '小麦播种面积', '玉米播种面积', '豆类作物播种面积',
         '大豆播种面积', '薯类作物播种面积', '油料播种面积', '棉花播种面积', '蔬菜播种面积']
pars7 = ['瓜果种植面积', '果园面积', '粮食产量', '小麦产量', '玉米产量', '豆类产量', '大豆产量', '薯类产量', '油料产量', '棉花产量',
         '蔬菜产量', '园林水果产量', '苹果产量', '肉类总产量', '牛肉产量', '羊肉产量', '猪肉产量', '牛年末存栏头数',  '奶类产量', '禽蛋产量']
pars8 = ['公路里程', '年末邮电局(所)数', '电信业务总量', '固定电话用户', '农村电话用户', '移动电话用户',
         '互联网宽带接入用户', '社会消费品零售总额', '城镇社会消费品零售总额', '乡村社会消费品零售总额']
pars9 = ['迁入人口合计', '省内迁入人口', '省外迁入人口', '迁出人口合计', '迁往省内人口',
         '迁往省外人口', '农林牧渔业增加值', '农业增加值', '林业增加值', '牧业增加值']
pars10 = ['水产品产量', '工业企业数', '工业总产值(现价)',  '从业人员年平均数', '主营业务收入',
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


# 循环每一个参数
for i, par in enumerate(parszhang):
    xlsList = Findfilenames(path, par)
    # 循环每一个县
    for c, oneCountryCode in enumerate(allCountryData.loc[:, "County_code_N"]):
        if pd.isnull(oneCountryCode):
            break
        # 循环每一年
        for yearn in np.arange(2000, 2017, 1):
            newfiledname = par + "_" + str(yearn)
            # 第一次要新键表头，后面的不需要
            if c == 0:
                allCountryData[newfiledname] = None
            # 对城区的代码进行加和处理
            if int(oneCountryCode) in onetoN_Code.columns:
                thisCityNCode = onetoN_Code.loc[:, oneCountryCode]
                urbanValue = 0
                for nCode in thisCityNCode:
                    if pd.isnull(nCode):
                        break
                    thisCountryValue = FindValue(par, xlsList, nCode, yearn)
                    if pd.isnull(thisCountryValue):
                        thisCountryValue = 0
                    if str(thisCountryValue).isspace():
                        thisCountryValue = 0
                    try:
                        urbanValue = urbanValue + thisCountryValue
                    except:
                        try:
                            input_num = float(thisCountryValue)
                            urbanValue = urbanValue + input_num
                        except:
                            print('在计算'+str(oneCountryCode)+'城区的_'+par +
                                  '_时，出现问题，寻找到的'+str(nCode)+'区县'+str(yearn)+'年的值不是一个数字，忽略这个值，请检查！')
                if urbanValue == 0:
                    continue
                allCountryData.loc[c, newfiledname] = urbanValue
                # print(allCountryData.loc[c, newfiledname])
                # print("get a one2N")
            # 正常的区县
            else:
                findedvalue = FindValue(par, xlsList, oneCountryCode, yearn)
                if pd.isnull(findedvalue):
                    continue
                try:
                    allCountryData.loc[c, newfiledname] = findedvalue
                except:
                    print('在计算'+str(oneCountryCode)+'普通县'+str(yearn)+'年的_'+par +
                          '_时，出现问题，请检查！')
            #         print(allCountryData[newfiledname].iloc[c])
                    # print("ok find a normal value")
            # print('完成 ' + str(oneCountryCode) +
            #       '县的' + str(yearn) + '年' + par + '的值')
    print('完成 '+par+'所有值的寻找')
# wb = xlwt.Workbook(encoding='utf-8')
# LST_test = wb.add_sheet('test', 'cell_overwrite_ok=True')
# LST_test.write(allCountryData)
# wb.save('/home/JiQiulei/EXCELwork_V2/newXlsx.xlsx')
allCountryData.to_csv(
    '/home/JiQiulei/EXCELwork_V2/newXlsx_zhang.csv', encoding='gbk')
print('already finish test! Good!')
