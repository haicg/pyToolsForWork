# coding=utf-8
import sys,os
import sqlite3
import errno


import sys

sys.setdefaultencoding('utf8')

import re
import csv
import xlrd
import codecs

def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print (e)

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

