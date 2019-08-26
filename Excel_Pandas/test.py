
def is_number(s):
    """是否是数字"""
    if s=='.':
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
        return float(number), unit
    except:
        return None, None

saasas='.'
print(is_number(saasas))
print(GetValueandUnit(saasas))