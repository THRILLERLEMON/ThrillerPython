def GetValueandUnit(pStrVandU):
    """拆分出数值和单位"""
    filterResult = filter(str.isdigit, pStrVandU)
    number = ''.join(list(filterResult))
    unit = pStrVandU.replace(number, '')
    return float(number), unit

a,b=GetValueandUnit('/')
print(a)
print(b)