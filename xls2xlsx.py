#将xls转换为xlsx
import os
import os.path
import win32com.client as win32

## 根目录
rootdir = u'C:\\Users\\thril\\Desktop\\EXCELwork\\data'
# 三个参数：父目录；所有文件夹名（不含路径）；所有文件名
for parent, dirnames, filenames in os.walk(rootdir):
    for fn in filenames:
        filedir = os.path.join(parent, fn)
        print(filedir)

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        wb = excel.Workbooks.Open(filedir)
        # xlsx: FileFormat=51
        # xls:  FileFormat=56,
        wb.SaveAs(filedir.replace('xls', 'xlsx'), FileFormat=51)
        wb.Close()                                 
        excel.Application.Quit()