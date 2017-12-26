# coding=utf-8
import sys,os
import sqlite3
import errno
import json

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import re
import csv
import xlrd
import xlwt
import codecs


def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)

#根据索引获取Excel表格中的数据
# 参数:file：Excel文件路径
# colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file= 'file.xls',colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    map_dict = {}
    colnames =  table.row_values(colnameindex) #某一行数据,表头

    for rownum in range(0,nrows):
        row = table.row_values(rownum)
        row_value_list = []
        for i in range(len(colnames)):
            row_value_list.append(row[i])
        map_dict[rownum] = row_value_list
    return map_dict

#根据名称获取Excel表格中的数据
# 参数:file：Excel文件路径
# colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file= 'file.xls',colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数
    colnames =  table.row_values(colnameindex) #某一行数据
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list

def save_result_txt(file='res.txt', data=""):
    list_res = ""
    with open(file, 'w') as fp:
        fp.write(data)


excel_dict = excel_table_byindex("sds13738-3_z-wave_plus_assigned_icon_types.xls", 3, 2)
json_data_org = []
for key,values in  excel_dict.items():
    ele_map = {}
    print key,values
    if values[1] != "" and values[2] != "":
        ele_map['IconId'] = values[1]
        if values[3].find('Multilevel Sensor; ') != -1:
            ele_map['name'] = values[2].replace('Multilevel Sensor; ', '').rstrip('\n').rstrip(' ')
            ele_map['IconName'] = 'Multilevel Sensor'
        elif values[3].find('Multilevel Sensor: ') != -1:
            ele_map['name'] = values[2].replace('Multilevel Sensor: ', '').rstrip('\n').rstrip(' ')
            ele_map['IconName'] = 'Multilevel Sensor'
        else:
            ele_map['name'] = values[2].rstrip('\n').rstrip(' ')
            ele_map['IconName'] = values[3].rstrip('\n').rstrip(' ')
        json_data_org.append(ele_map)

data = json.dumps(json_data_org, sort_keys=True,indent=2)
save_result_txt("zwave_icon.json", data)


