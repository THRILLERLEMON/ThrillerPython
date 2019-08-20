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

# shanxi
path = 'D:\OneDrive\SharedFile\EXCEL 数据处理\EXCELwork201908_linux_3RD\Data_Shanxi'
allCountryData = pd.read_excel(
    'D:\OneDrive\SharedFile\EXCEL 数据处理\EXCELwork201908_linux_3RD\YR_All_3RD.xlsx', sheet_name="Sheet1")
onetoN_Code = pd.read_excel(
    'D:\OneDrive\SharedFile\EXCEL 数据处理\EXCELwork201908_linux_3RD\OnetoN_Code_3RD.xlsx', sheet_name="Code")

#以山西省晋城市为例提取的参数
#1 能找到的对应参数，key是2000之前的参数名称，value是2000年后的参数名称
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
    '化学肥料': '化肥使用量(折纯量)',
    '公路长度': '公路里程',
    '社会消费品零售总额': '社会消费品零售总额',
    '普通中学在校学生数': '普通中学在校学生数',
    '小学在校学生数': '小学在校学生数',
    '规模以上工业企业数': '工业企业数',
    '规模以上工业总产值': '工业总产值',
    '工业增加值（现价）': '工业生产总值',
    '床位数': '医院、卫生院床位数',
    '总人口': '年末总人口',
    '乡村从业人员数': '乡村从业人员数',
    '农业机械总动力': '农业机械总动力',
    '家禽年末存栏数': '家禽存栏',
    '果园面积': '果园面积'
}

#2 参数对应单位
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
    '#乡村人口数': '人',
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
    '化学肥料': '吨',
    '公路长度': '公里',
    '社会消费品零售总额': '万元',
    '普通中学在校学生数': '人',
    '小学在校学生数': '人',
    '规模以上工业企业数': '个',
    '规模以上工业总产值': '万元',
    '工业增加值（现价）': '万元',
    '床位数': '张',
    '总人口': '万人',
    '乡村从业人员数': '人',
    '农业机械总动力': '万千瓦',
    '家禽年末存栏数': '万只',
    '果园面积': '公顷'
}



#2 2000年之前特有的参数
unknowpars = {
    '社会从业人数': '',
    '在岗职工平均工资': '',
    '单位GDP能耗': '',
    '单位工业增加值能耗': '',
    '#非农业人口': '',
    '# 水田水浇地': '',
    '受灾面积': '',
    '成灾面积': '',
    '封山育林面积': '',
    '工业销售产值': '',
    '主要工业产品产量': '',
    '#原煤': '',
    '#发电量': '',
    '#水泥': '',
    '#焦炭': '',
    '#高中': '',
    '企业数': ''
}
