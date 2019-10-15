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
    return '%s%s_all.h' % (LC_PREFIX, xtp_api_file_name)

def get_Api_Function_Name(xtp_api_file_name, name):
    return '%s%s' % (get_api_short_name(xtp_api_file_name), name)

def inCheckLst(param, lst):
    for item in lst:
        if param.find(item) >= 0:
            return True
    return False

def genFields(info, isExtern = False):
    for item in info[1]:
        if item[2] != '' :
            genFieldsInternal(item[2], isExtern)

def genFieldsInternal(params, isExtern = False):
    param_list = str(params).split(',')
    for param in param_list:
        format_param = param.strip()

        idx = format_param.find('=')
        
        if (idx >= 0):
            format_param = format_param[0:idx].strip()

        idx = format_param.find('XTP_')
        if (idx >= 0) :
            fields[format_param[0: format_param.find(' ')]] = 0
        else :
            idx = format_param.find('XTP')
            if (idx >= 0) :
                fields[format_param[0:format_param.find(' ')]] = 0

def get_c_def_params(params, isExtern = False):
    param_list = str(params).split(',')
    res_list = []
    for param in param_list:
        format_param = param.strip()

        idx = format_param.find('=')
        
        if (idx >= 0):
            format_param = format_param[0:idx].strip()

        idx = format_param.find('XTP_')
        if (idx >= 0) :
            idx2 = format_param.find(' ')
            fields[format_param[0:idx2]] = 0
            if isExtern :
                data = GoPrefix + format_param
            else:
                #data = 'enum ' + format_param
                data = format_param[0:idx2] + '_' + format_param[idx2:]
            res_list.append(data)
        else :

            idx = format_param.find('XTP')
            if (idx >= 0) :
                idx2 = format_param.find(' ')
                fields[format_param[0:idx2]] = 0

                if isExtern :
                    data = GoPrefix + format_param
                else:
                    #print('...format_param', format_param, ' inLst:', inCheckLst(format_param, typedefStructLst))
                    if not inCheckLst(format_param, typedefStructLst) :
                        if format_param.find('const') >= 0:
                            data = 'const struct' + format_param[5:]
                        else:
                            data = 'struct ' + format_param
                    else:
                        data = format_param

                res_list.append(data)
            else:
                res_list.append(format_param)
            
    return (', ').join(res_list)

def get_params(params):
    param_list = str(params).split(',')
    res_list = []
    for param in param_list:
        format_param = param.strip()
        format_param = format_param.replace('[]', '')

        idx = format_param.find('*') + 1
        if (idx >= 1) :
            res_list.append(format_param[idx:])
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
