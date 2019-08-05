print('123')
print([(x,y) for x in range(10) if x % 2 if x>3 for y in range(10) if y>7 if y!=8])
