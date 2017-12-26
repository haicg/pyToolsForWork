# coding=utf-8
from ConvertExcelToJson import DealExcel
import json

excel_dict = DealExcel.excel_table_byindex("sds13738-3_z-wave_plus_assigned_icon_types.xls", 3, 2)
json_data_org = []
for key,values in  excel_dict.items():
    ele_map = {}
    print (key,values)
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
DealExcel.save_result_txt("zwave_icon.json", data)


