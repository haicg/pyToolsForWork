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

def parseTable(table, colnameindex):
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    map_dict = {}
    colnames = table.row_values(colnameindex)  # 某一行数据,表头

    for rownum in range(0, nrows):
        row = table.row_values(rownum)
        row_value_list = []
        for i in range(len(colnames)):
            row_value_list.append(row[i])
        map_dict[rownum] = row_value_list
    return map_dict

#根据索引获取Excel表格中的数据
# 参数:file：Excel文件路径
# colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file= 'file.xls',colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    return parseTable(table, colnameindex)


# colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file= 'file.xls',colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    return parseTable(table, colnameindex)


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
    try:
        int(s,16)
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

def getUintStr(devUnitVal, devUnit):
    if is_number(devUnitVal):
        #print "Unit val"
        if (devUnit == "Reserved"):
            return None

        pattern1 = re.compile('\((.+?)\)')
        unit_list = pattern1.findall(devUnit)
        if (unit_list):
            return unit_list[0]
        else:
            if len(devUnit) < 10:
                return devUnit
            else:
                return None
    else :
        #print "Not Unit Val"
        return None
def save_result_txt(file='res.txt', data=""):
    list_res = ""
    with open(file, 'w') as fp:
        fp.write(data)


sensor_dict = excel_table_byname("sds13812-2_multilevel_sensor_command_class_list_of_assigned_multilevel_sensor_types_and_scales.xls", 4, "Multilevel Sensor")

devName = ""
devType = None
devUnit = None
devUnitVal = None
resDict = {}
devObj = []
devDict = {}
unit_list = []
devList = []

for (i, value) in sensor_dict.items():
    newDevFlag = 0
    unit_name = None
    #print value
    if (i < 5):
        continue
    devUnit = value[4]
    devUnitVal = value[5]
    unit_name = getUintStr(devUnitVal, devUnit)
    if value[0] != None and value[0] != '' and value[1] != None and value[1] != '':
        print "new Device"
        devName = value[0]
        devType = value[1]
        newDevFlag = 1
    else :
        print "Last Device "

    if devUnit and devName and devType:
        if newDevFlag == 1:
            devDict = {}
            devObj = []
            unit_list = []
            unit_obj = {}
            devDict["type"] = devType
            devDict["name"] = devName
            devDict['unit'] = unit_list

            if (devUnitVal and unit_name):
                unit_obj['type'] = devUnitVal
                unit_obj['name'] = unit_name
                unit_list.append(unit_obj)
            devList.append(devDict)
        else:
            unit_obj = {}
            if (devUnitVal and unit_name):
                unit_obj['type'] = devUnitVal
                unit_obj['name'] = unit_name
                unit_list.append(unit_obj)
#print devList
data = json.dumps(devList, sort_keys=True,indent=2)
save_result_txt("zwave_multilevel_xls.json", data)

