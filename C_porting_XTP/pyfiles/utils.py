#!/usr/bin/python
#! -*- encoding=utf-8 -*-

from defines import *

def isInlist(func_name) :
    if len(md_concern_list) == 0 and len(trader_concern_list) == 0:
        return True
    print (func_name)
    if func_name in md_concern_list :
        return True
    if func_name in trader_concern_list :
        return True
    return False
        
def getSpiClassName(info):
    return info[0]

def getApiClassName(info):
    return info[2]

def get_api_short_name(xtp_api_file_name):
    pos = xtp_api_file_name.find(FTDC_STR)
    return str(xtp_api_file_name)[pos + len(FTDC_STR):]
        
def get_spi_class_name(info):
    return '%s%s' % (LC_PREFIX, getSpiClassName(info))

def get_api_impl_h_name(xtp_api_file_name):
    return '%s%s%s.hpp' % (LC_PREFIX, xtp_api_file_name, LC_SUFFIX)

def get_api_impl_cpp_name(xtp_api_file_name):
    return '%s%s%s.cxx' % (LC_PREFIX, xtp_api_file_name, LC_SUFFIX)
        
def get_FN_name(xtp_api_file_name, item_name):
    return '%s%s%s' % (FN, get_api_short_name(xtp_api_file_name), item_name)
        
def get_Go_FN_name(xtp_api_file_name, item_name):
    return '%s%s%s' % (GoPrefix, get_api_short_name(xtp_api_file_name), item_name)

def get_Register_Callback_Name(xtp_api_file_name, name):
    return '%s%s%sCallback' % (REG_PREFIX, get_api_short_name(xtp_api_file_name), name)

def get_api_interface_h_name(xtp_api_file_name):
    return '%s%s.h' % (LC_PREFIX, xtp_api_file_name)

def get_api_interface_h_name_all(xtp_api_file_name):
    return '%s%s_cgo.h' % (LC_PREFIX, xtp_api_file_name)

def get_Api_Function_Name(xtp_api_file_name, name):
    return '%s%s' % (get_api_short_name(xtp_api_file_name), name)

def inCheckLst(param, lst):
    for item in lst:
        if param.find(item) >= 0:
            return True
    return False

def get_interface_params(params, isExtern = False):
    param_list = str(params).split(',')
    res_list = []
    for param in param_list:
        format_param = param.strip()

        idx = format_param.find('=')
        
        if (idx >= 0):
            format_param = format_param[0:idx].strip()

        tmps = format_param.split(' ')
        
        ind = 0
        prefix = ''
        if tmps[0].strip() == 'const':
            prefix = 'const '
            ind = 1
        param_type = tmps[ind]

        for k, v in typedefedStructs.items():
            if v == param_type:
                param_type = k
                break
            
        param_name = tmps[ind + 1]

        if param_type in untypedefedStructs:
            param_type = param_type + '_'

        res_list.append(prefix + param_type + ' ' + param_name)
            
    return (', ').join(res_list)

def get_impl_params(params):
    print('params:', params)
    param_list = str(params).split(',')
    res_list = []
    for param in param_list:
        format_param = param.strip()
        format_param = format_param.replace('[]', '')

        idx = format_param.find('*')
        if (idx >= 0) :
            res_list.append(format_param[idx + 1:])
        else :
            params = format_param.split(' ')
            if len(params) == 3 and params[0].strip() == 'const' :
                res_list.append(params[2].strip())
            elif len(params) == 2 or (len(params) == 4 and params[2].strip() == '=') :
                #len == 4 and p[2] == '=' fix default params issue.
                res_list.append(params[1].strip())
            else:
                raise ValueError
            
    return (', ').join(res_list)
    
def get_msg_str(prefix, item):
    return '%s_%s' % (prefix, str(item).lstrip().rstrip().upper())
