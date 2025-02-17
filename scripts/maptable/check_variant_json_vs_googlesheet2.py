#!/usr/bin/env python
# -*- coding: utf-8 -*-
# check_variant_json_vs_googlesheet.py
# made by Daniel Minseok Kwon
# 2020-05-05 15:50:33
#########################
import sys
import os
SVRNAME = os.uname()[1]
if "MBI" in SVRNAME.upper():
    sys_path = "/Users/pcaso/bin/python_lib"
elif SVRNAME == "T7":
    sys_path = "/ms1/bin/python_lib"
else:
    sys_path = "/home/mk446/bin/python_lib"
sys.path.append(sys_path)

SKIP_SOURCE = ['VCF', 'MUTIALLELE', 'SAMPLEGENO', 'HGVS', 'HG19', 'COMHET']


def convert_boolean(bstr, true_value = "Y"):
    if bstr == "Y":
        flag = True
    else:
        flag = False
    return flag


def check_variant_json_vs_googlesheet(variant_json, googlesheet):
    jdata = {}
    vjson = file_util.jsonOpen(variant_json)
    for s1 in vjson['source']:
        try:
            jdata[s1['name']]
        except KeyError:
            jdata[s1['name']] = {}
        for f1 in s1['fields']:
            if 'name2' in f1.keys():
                fname = s1['name'] + '_' + f1['name2']
            else:
                fname = s1['name'] + '_' + f1['name']
            jdata[s1['name']][fname.lower()] = f1
    # print(vjson['source'][0].keys())

    h = {}
    gdata = {}
    for line in open(googlesheet):
        if line.strip() != "" and line.strip()[0] != "#":
            arr = line.split('\t')
            arr[-1] = arr[-1].strip()
            if arr[0] == "no":
                for k in range(len(arr)):
                    h[arr[k].strip()] = k
            else:
                field_name = arr[h['field_name']].strip()
                source_name = arr[h['source_name']].strip()
                field_type = arr[h['field_type']].strip()
                is_list = convert_boolean(arr[h['is_list']].strip(), "Y")

                d = {}
                d['type'] = field_type
                d['is_list'] = is_list
                
                try:
                    gdata[source_name][field_name] = d
                except KeyError:
                    gdata[source_name] = {}
                    gdata[source_name][field_name] = d

                try:
                    jdata[source_name]
                    fdata = jdata[source_name][field_name]

                    if field_type != fdata['type']:
                        print('ERROR: type mismatching:', field_name, field_type + "(googlesheet)", fdata['type'] + "(json)")

                    if 'is_list' in fdata.keys():
                        if is_list != fdata['is_list']:
                            print('ERROR: no is_list matching:', is_list, fdata['is_list'])
                    else:
                        if is_list:
                            print('ERROR: no is_list matching:', is_list, 'False')
                except KeyError:
                    if source_name in SKIP_SOURCE:
                        print('WARNING: no field in json:', source_name , ">" , field_name)
                    else:
                        print('ERROR: no field in json:', source_name, ">" , field_name)
                
                # print(fieldname, source_name)
                # break
    

    for source_name in jdata.keys():
        flag = False
        try:
            gdata[source_name]
            flag = True
        except KeyError:
            print('ERROR: no source in googlesheet', source_name)

        if flag:
            for field_name in jdata[source_name].keys():
                d = jdata[source_name][field_name]
                if ('is_available' in d.keys() and d['is_available']) or ('is_available' not in d.keys()):
                    try:
                        gdata[source_name][field_name]
                    except KeyError:
                        print('ERROR: no field in googlesheet', source_name, ">", field_name)



if __name__ == "__main__":
    import proc_util
    import file_util
    # variant_json = "/home/mk446/mutanno/SRC/tests/data/datastructure_v0.4.5ds.json"
    # googlesheet = "/home/mk446/mutanno/SRC/tests/data/datastructure_v0.4.5ds.googlesheet.txt"
    variant_json = sys.argv[1]
    googlesheet = sys.argv[2]
    check_variant_json_vs_googlesheet(variant_json, googlesheet)
