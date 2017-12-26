import xml.etree.ElementTree as ET
import json

tree = ET.parse('device_classes.xml')
root = tree.getroot()

json_data_org = []
for child in root.findall('{http://code.google.com/p/open-zwave/}Generic'):
    id1 = child.attrib['key']
    for Specific in child.findall('{http://code.google.com/p/open-zwave/}Specific'):
        #print Specific.attrib
        id2 = Specific.attrib.get('key')
        pname = Specific.attrib.get('label')
        iname = Specific.attrib.get('icon')
        if id2 and pname and iname:
            ele_map = {}
            print (id1,id2,id1+id2[2:])
            ele_map['IconId'] = (id1 + id2[2:]).rstrip('\n').rstrip(' ')
            ele_map['name'] = pname.rstrip('\n').rstrip(' ')
            ele_map['IconName'] = iname.rstrip('\n').rstrip(' ')
            print (ele_map)
            json_data_org.append(ele_map)
        else:
            print (id2 + pname)
print (json_data_org)
print (len(json_data_org))

def save_result_txt(file='res.txt', data=""):
    list_res = ""
    with open(file, 'w') as fp:
        fp.write(data)
data = json.dumps(json_data_org, sort_keys=True, indent=2)
save_result_txt("zwave_device_spec.json", data)




