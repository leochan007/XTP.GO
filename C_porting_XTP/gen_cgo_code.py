#!/usr/bin/python
#! -*- encoding=utf-8 -*-

import os
import re
import shutil
import time

class_pattern_spi = re.compile('class\s(\w+)\s')
class_pattern_api = re.compile('class\s\w+\s(\w+)\s')
method_pattern = re.compile("virtual\s(\w+)\s(\w+)\((.*)\)")

COMMON_H = 'common_macro.h'

CTP_INCLUDE_PATH = 'include/XTP'

CTP_H_Base = 'XTP'

output_api_dir = 'include/CXTPApi'

CTPCApi_H_Base = 'CXTPApi'

LC_PREFIX = 'LC'

FN = 'fn'

GoPrefix = 'Go'

LC_SUFFIX = 'Impl'

FTDC_STR = 'Ftdc'

REG_PREFIX = 'Register'

LC_CTP_API = 'LC_XTP_API'

RegisterSpi = 'RegisterSpi'

pApi_name = 'pLC_Api'

pSpi_name = 'pLC_Spi'

Con_Path = 'con_path'

bIsUsingUdp = 'bIsUsingUdp'

bIsMulticast = 'bIsMulticast'

client_id = 'client_id'
save_file_path = 'save_file_path'
log_level = 'log_level'

#Md = 'MdApi'

#Trader = 'TraderApi'

output_dir = 'src/Platform/CXTPApiImpl'

fields = dict()

VOID_PTR = '(unsigned long long int)this'

Extern_Ptr_Param = 'unsigned long long int spiPtr'

md_concern_list = []
trader_concern_list = []

md_concern_list = [ 'Go_quote_apiOnSubMarketData', 'Go_quote_apiOnMarketData', 'Go_quote_apiOnSubOrderBook', 'Go_quote_apiOnOrderBook' ]
trader_concern_list = [ 'Go_trader_apiOnOrderEvent', 'Go_trader_apiOnTradeEvent', 'Go_trader_apiOnQueryOrder', 'Go_trader_apiOnQueryTrade',
	'Go_trader_apiOnQueryPosition', 'Go_trader_apiOnQueryAsset' ]

def isInlist(func_name) :
    if len(md_concern_list) == 0 and len(trader_concern_list) == 0:
        return True
    print (func_name)
    if func_name in md_concern_list :
        return True
    if func_name in trader_concern_list :
        return True
    return False

def gen_cmakelist() :
    shutil.copyfile(os.path.join('others', 'CMakeLists.txt'), os.path.join(output_dir, 'CMakeLists.txt'))

def gen_common_h() :
    if os.path.exists(output_dir) :
        shutil.rmtree(output_dir)
    if os.path.exists(output_api_dir) :
        shutil.rmtree(output_api_dir)
    time.sleep(1)
    os.makedirs(output_dir)
    os.makedirs(output_api_dir)
    file_object = open(os.path.join(output_api_dir, COMMON_H), 'w')
    try:
        file_object.write('''#ifndef _H_COMMON_MACRO_H_
#define _H_COMMON_MACRO_H_\n
#ifdef WIN32
#ifdef DLL_EXPORT
#define %s __declspec(dllexport)
#else
#define %s __declspec(dllimport)
#endif
#else
#define %s
#endif\n

#include<stdlib.h>

#ifndef __cplusplus
typedef enum {false = 0, true = 1} bool;
#endif

#endif\n''' % (LC_CTP_API, LC_CTP_API, LC_CTP_API))
        
#define SCR_PRINT(arg, ...)     printf(arg, ##__VA_ARGS__)\n

#include<stdlib.h>

#endif\n''' % (LC_CTP_API, LC_CTP_API, LC_CTP_API))

    finally:
        file_object.close()
        
def get_class_info(ctp_api_file_name):
    file_object = open(os.path.join(CTP_INCLUDE_PATH, '%s.h' % ctp_api_file_name), encoding = 'utf-8')
    try:
        all_the_text = file_object.read()
        api_start = all_the_text.rfind('class')
        match = class_pattern_spi.search(all_the_text, 0, api_start)
        if match :
            spi_class_name = match.group(1)
        else :
            spi_class_name = ''
        funcs_spi = method_pattern.findall(all_the_text, 0, api_start)
        match = class_pattern_api.search(all_the_text, api_start)
        if match :
            api_class_name = match.group(1)
        else :
            api_class_name = ''
        funcs_api = method_pattern.findall(all_the_text, api_start)
        return (spi_class_name, funcs_spi, api_class_name, funcs_api)
    finally:
        file_object.close()
        
def getSpiClassName(info):
    return info[0]

def getApiClassName(info):
    return info[2]

def get_api_short_name(ctp_api_file_name):
    pos = ctp_api_file_name.find(FTDC_STR)
    return str(ctp_api_file_name)[pos + len(FTDC_STR):]
        
def get_spi_class_name(info):
    return '%s%s' % (LC_PREFIX, getSpiClassName(info))

def get_api_impl_h_name(ctp_api_file_name):
    return '%s%s%s.hpp' % (LC_PREFIX, ctp_api_file_name, LC_SUFFIX)

def get_api_impl_cpp_name(ctp_api_file_name):
    return '%s%s%s.cxx' % (LC_PREFIX, ctp_api_file_name, LC_SUFFIX)
        
def get_FN_name(ctp_api_file_name, item_name):
    return '%s%s%s' % (FN, get_api_short_name(ctp_api_file_name), item_name)
        
def get_Go_FN_name(ctp_api_file_name, item_name):
    return '%s%s%s' % (GoPrefix, get_api_short_name(ctp_api_file_name), item_name)

def get_Register_Callback_Name(ctp_api_file_name, name):
    return '%s%s%sCallback' % (REG_PREFIX, get_api_short_name(ctp_api_file_name), name)

def get_api_interface_h_name(ctp_api_file_name):
    return '%s%s.h' % (LC_PREFIX, ctp_api_file_name)

def get_api_interface_h_name_all(ctp_api_file_name):
    return '%s%s_all.h' % (LC_PREFIX, ctp_api_file_name)

def get_Api_Function_Name(ctp_api_file_name, name):
    return '%s%s' % (get_api_short_name(ctp_api_file_name), name)

def get_c_def_params(params, isExtern = False):
    param_list = str(params).split(',')
    res_list = []
    for param in param_list:
        format_param = param.strip()

        idx = format_param.find('=')
        
        if (idx >= 0):
            format_param = format_param[0:idx].strip()

        idx = format_param.find('THOST_TE_RESUME_TYPE')
        
        if (idx >= 0):
            format_param = format_param.replace('THOST_TE_RESUME_TYPE', 'int')

        idx = format_param.find('Field')
        if (idx >= 0) :
            idx2 = format_param.find(' ')
            fields[format_param[0:idx2]] = 0
            if isExtern :
                data = GoPrefix + format_param
            else:
                data = 'struct ' + format_param
            res_list.append(data)
        else :
            if isExtern :
                format_param = format_param.replace('bool bIsLast', 'int bIsLast')
            res_list.append(format_param)
    return (', ').join(res_list)

def get_params(params):
    param_list = str(params).split(',')
    res_list = []
    for param in param_list:
        format_param = param.strip()
        format_param = format_param.replace('[]', '')

        idx = format_param.find('nResumeType')
        if (idx >= 0):
            format_param = format_param.replace('nResumeType', '(THOST_TE_RESUME_TYPE)nResumeType')

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

def gen_api_impl_h(info, ctp_api_file_name):
    output_filename = get_api_impl_h_name(ctp_api_file_name)
    macro_name = output_filename.upper().replace('.', '_')
    h_output = open(os.path.join(output_dir, output_filename), 'w')
    try:
        h_output.write('''#ifndef %s\n#define %s\n#include "%s.h"\n#include "%s"\n\nusing namespace XTP::API;\n\n'''
                       % (macro_name, macro_name, ctp_api_file_name, get_api_interface_h_name(ctp_api_file_name)))
        h_output.write('class %s : public %s\n{\nprivate:\n\n' % (get_spi_class_name(info), getSpiClassName(info)))
        for item in info[1]:
            h_output.write('\t%s m_%s;\n' % (get_FN_name(ctp_api_file_name, item[1]), get_FN_name(ctp_api_file_name, item[1])))
        h_output.write('\npublic:\n')
        for item in info[1]:
            h_output.write('\tvoid %s(%s _%s);\n' % (get_Register_Callback_Name(ctp_api_file_name, item[1]), get_FN_name(ctp_api_file_name, item[1]), get_FN_name(ctp_api_file_name, item[1])))
            
        h_output.write('\npublic:\n')
        for item in info[1]:
            h_output.write('\tvirtual %s %s(%s);\n' % (item[0], item[1], item[2]))
        
        h_output.write('\t%s();\n' % get_spi_class_name(info))
        h_output.write('\t~%s();\n' % get_spi_class_name(info))
        h_output.write('\n};\n\n')
        h_output.write('%s * Get%s(void * %s);\n\n' % (get_spi_class_name(info), get_spi_class_name(info), pSpi_name))
        h_output.write('%s * Get%s(void * %s);\n\n' % (getApiClassName(info), getApiClassName(info), pApi_name))
        h_output.write('#endif')
    finally:
        h_output.close()
    return output_filename

def gen_api_impl_cpp(info, ctp_api_file_name):
    h_output = open(os.path.join(output_dir, get_api_impl_cpp_name(ctp_api_file_name)), 'w')
    try:
        h_output.write('#include "%s"\n\n' % (get_api_impl_h_name(ctp_api_file_name)))
        h_output.write('%s * Get%s(void * %s)\n{\n' % (get_spi_class_name(info), get_spi_class_name(info), pSpi_name))
        h_output.write('\treturn (%s *)(%s);\n}\n\n' % (get_spi_class_name(info), pSpi_name))
        h_output.write('%s * Get%s(void * %s)\n{\n' % (getApiClassName(info), getApiClassName(info), pApi_name))
        h_output.write('\treturn (%s *)(%s);\n}\n\n' % (getApiClassName(info), pApi_name))
        
        h_output.write('%s::%s()\n{\n' % (get_spi_class_name(info), get_spi_class_name(info)))
        
        for item in info[1]:
            h_output.write('\t m_%s = NULL;\n' % (get_FN_name(ctp_api_file_name, item[1])))
        
        h_output.write('}\n\n')
        
        h_output.write('%s::~%s()\n{}\n\n' % (get_spi_class_name(info), get_spi_class_name(info)))
        
        for item in info[1]:
            h_output.write('void %s::%s(%s _%s)\n{\n'
                           % (get_spi_class_name(info), get_Register_Callback_Name(ctp_api_file_name, item[1]), get_FN_name(ctp_api_file_name, item[1]), get_FN_name(ctp_api_file_name, item[1])))
            h_output.write('\t m_%s = _%s;\n' % (get_FN_name(ctp_api_file_name, item[1]), get_FN_name(ctp_api_file_name, item[1])))
            h_output.write('}\n\n')
            
        for item in info[1]:
            h_output.write('%s %s::%s(%s)\n{\n' % (item[0], get_spi_class_name(info), item[1], item[2]))
            func_name = get_FN_name(ctp_api_file_name, item[1])

            ## todo list

            if (item[2] == '') :
                h_output.write('\t(*m_%s)();\n' % (func_name))
            else :
                h_output.write('\t(*m_%s)(%s);\n' % (func_name, get_params(item[2])))

            '''            
            func_name = get_Go_FN_name(ctp_api_file_name, item[1])

            if not isInlist(func_name) :
                h_output.write('}\n\n')
                continue
            if (item[2] == '') :
                h_output.write('\t %s(%s);\n' % (func_name, VOID_PTR))
            else :
                h_output.write('\t %s(%s, %s);\n' % (func_name, VOID_PTR, get_params(item[2])))
            '''

            h_output.write('}\n\n')
        
    finally:
        h_output.close()

def gen_api_interface_h(info, ctp_api_file_name):
    output_filename = get_api_interface_h_name(ctp_api_file_name)

    macro_name = output_filename.upper().replace('.', '_')
    h_output = open(os.path.join(output_api_dir, output_filename), 'w')
    try:

        h_output.write('#ifndef %s\n#define %s\n\n'% (macro_name, macro_name))
        h_output.write('#include "%s"\n' % COMMON_H)
        h_output.write('''\n#include "lcdefine.h"\n\n#ifdef __cplusplus\nextern "C" {\n#endif\n''')
        
        for item in info[1]:
            func_name = get_FN_name(ctp_api_file_name, item[1])
            if item[2] == '' :
                h_output.write('typedef %s (* %s)();\n' % (item[0], func_name))
            else :
                h_output.write('typedef %s (* %s)(%s);\n' % (item[0], func_name, get_c_def_params(item[2])))

        h_output.write('\n//register callbacks\n')
        h_output.write('%s void * Create%s();\n' % (LC_CTP_API, '%s%s' % (LC_PREFIX, getSpiClassName(info))))
        h_output.write('%s void Release%s(void * * %s);\n' % (LC_CTP_API, '%s%s' % (LC_PREFIX, getSpiClassName(info)), pSpi_name))
        for item in info[1]:
            h_output.write('%s void %s(void * %s, %s pCallback);\n' % (LC_CTP_API, get_Register_Callback_Name(ctp_api_file_name, item[1]), pSpi_name, get_FN_name(ctp_api_file_name, item[1])))
        
        h_output.write('\n//api method porting\n')
        
        h_output.write('%s void * Create%s(uint8_t %s, const char * %s, XTP_LOG_LEVEL_ %s);\n'
                           % (LC_CTP_API, '%s%s' % (LC_PREFIX, getApiClassName(info)), client_id, save_file_path, log_level))

        h_output.write('%s void Release%s(void * * %s);\n' % (LC_CTP_API, '%s%s' % (LC_PREFIX, getApiClassName(info)), pApi_name))
        for item in info[3]:
            if item[1] == RegisterSpi :
                h_output.write('%s void %s(void * %s, void * %s);\n' % (LC_CTP_API, get_Api_Function_Name(ctp_api_file_name, item[1]), pApi_name, pSpi_name))
                continue
            if item[2] == '' :
                h_output.write('%s %s %s(void * %s);\n' % (LC_CTP_API, item[0], get_Api_Function_Name(ctp_api_file_name, item[1]), pApi_name))
            else :
                h_output.write('%s %s %s(void * %s, %s);\n' % (LC_CTP_API, item[0], get_Api_Function_Name(ctp_api_file_name, item[1]), pApi_name, get_c_def_params(item[2])))
        
        h_output.write('''\n#ifdef __cplusplus\n}\n#endif\n#endif\n''')
    finally:
        h_output.close()

def gen_api_interface_h_all(info, ctp_api_file_name):
    output_filename = get_api_interface_h_name(ctp_api_file_name)
    output_filename_all = get_api_interface_h_name_all(ctp_api_file_name)

    macro_name = output_filename.upper().replace('.', '_')
    h_output_all = open(os.path.join(output_api_dir, output_filename_all), 'w')
    try:

        h_output_all.write('#ifndef %s\n#define %s\n\n'% (macro_name, macro_name))
        h_output_all.write('#include "%s"\n' % COMMON_H)
        h_output_all.write('''\n#include "lcdefine.h"\n#include "%s"\n#ifdef __cplusplus\nextern "C" {\n#endif\n''' % (output_filename))

        h_output_all.write('\n// define extern functions\n')

        for item in info[1]:
            func_name = get_Go_FN_name(ctp_api_file_name, item[1])
            if not isInlist(func_name) :
                continue
            if item[2] == '' :
                h_output_all.write('extern void %s(%s);\n' % (func_name, Extern_Ptr_Param))
            else :
                h_output_all.write('extern void %s(%s, %s);\n' % (func_name, Extern_Ptr_Param, get_c_def_params(item[2], True)))
        h_output_all.write('''\n#ifdef __cplusplus\n}\n#endif\n#endif\n''')
    finally:
        h_output_all.close()

def gen_api_interface_cpp(info, ctp_api_file_name):
    print ('\n---gen_api_interface_cpp xtp_api_file_name=', ctp_api_file_name, '\n')
    output_filename = '%s%s.cxx' % (LC_PREFIX, ctp_api_file_name)
    h_output = open(os.path.join(output_dir, output_filename), 'w')
    try:
        h_output.write('''#include "%s"\n''' % (get_api_interface_h_name(ctp_api_file_name)))
        h_output.write('''#include "%s"\n\n''' % get_api_impl_h_name(ctp_api_file_name))
        
        #spi
        h_output.write('\n// --- gen_api_interface_cpp spi ---\n')

        h_output.write('%s void * Create%s()\n{\n\treturn (void *)(new %s);\n}\n\n'
                       % (LC_CTP_API, '%s%s' % (LC_PREFIX, getSpiClassName(info)), get_spi_class_name(info)))
        h_output.write('%s void Release%s(void * * %s)\n{\n\tif (*%s != NULL)\n\t{\n\t\tdelete *%s;\n\t\t*%s = NULL;\n\t}\n}\n\n'
                       % (LC_CTP_API, '%s%s' % (LC_PREFIX, getSpiClassName(info)), pSpi_name, pSpi_name, pSpi_name, pSpi_name))

        for item in info[1]:
            h_output.write('void %s(void * %s, %s pCallback)\n' % (get_Register_Callback_Name(ctp_api_file_name, item[1]), pSpi_name, 
                get_FN_name(ctp_api_file_name, item[1])))
            h_output.write('{\n\tif (%s != NULL)\n\t{\n\t\t(Get%s(%s))->%s(pCallback);\n\t}\n}\n'
                % (pSpi_name, get_spi_class_name(info), pSpi_name, get_Register_Callback_Name(ctp_api_file_name, item[1])))
        
        #api
        h_output.write('\n// --- gen_api_interface_cpp api ---\n')

        h_output.write('''%s void * Create%s(uint8_t %s, const char * %s, XTP_LOG_LEVEL_ %s)
            \n{\n\treturn (void *)(%s::Create%s(%s, %s, %s));\n}\n\n'''
            % (LC_CTP_API, '%s%s' % (LC_PREFIX, getApiClassName(info)), client_id, save_file_path, log_level,
            getApiClassName(info), getApiClassName(info), client_id, save_file_path, log_level))
        
        h_output.write('void Release%s(void * * %s)\n{\n\tif (*%s != NULL)\n\t{\n\t\tdelete *%s;\n\t\t*%s = NULL;\n\t}\n}\n\n'
            % ('%s%s' % (LC_PREFIX, getApiClassName(info)), pApi_name, pApi_name, pApi_name, pApi_name))

        for item in info[3]:
            if item[1] == RegisterSpi :
                h_output.write('%s void %s(void * %s, void * %s)\n' % (LC_CTP_API, get_Api_Function_Name(ctp_api_file_name, item[1]), pApi_name, pSpi_name))
                h_output.write('{\n\tif (%s != NULL)\n\t{\n\t\t(Get%s(%s))->%s(Get%s(%s));\n\t}\n}\n\n'
                    %(pApi_name, getApiClassName(info), pApi_name, RegisterSpi, get_spi_class_name(info), pSpi_name))
                continue
            
            attach_1 = ''
            attach_2 = ''

            if item[0] != 'void' :
                attach_1 = 'return '
                attach_2 = '\n\treturn -1;'
                
            if ( get_Api_Function_Name(ctp_api_file_name, item[1]) == '_quote_apiSubscribeAllOptionMarketData') :
                print('spi item:', item)
                print('--> get_Api_Function_Name:', get_Api_Function_Name(ctp_api_file_name, item[1]))
                print('get_c_def_params:', get_c_def_params(item[2]))

            if item[2] == '' :
                h_output.write('%s %s %s(void* %s)\n' % (LC_CTP_API, item[0], get_Api_Function_Name(ctp_api_file_name, item[1]), pApi_name))
                h_output.write('{\n\tif (%s != NULL)\n\t{\n\t\t%s(Get%s(%s))->%s();\n\t}%s\n}\n\n'
                           % (pApi_name, attach_1, getApiClassName(info), pApi_name, item[1], attach_2))
            else :
                h_output.write('%s %s %s(void* %s, %s)\n' % (LC_CTP_API, item[0], get_Api_Function_Name(ctp_api_file_name, item[1]), pApi_name, get_c_def_params(item[2])))
                h_output.write('{\n\tif (%s != NULL)\n\t{\n\t\t%s(Get%s(%s))->%s(%s);\n\t}%s\n}\n\n'
                           % (pApi_name, attach_1, getApiClassName(info), pApi_name, item[1], get_params(item[2]), attach_2))        
    finally:
        h_output.close()
    return output_filename

def gen_ctp_api(ctp_api_file_name, enum_map):
    info = get_class_info(ctp_api_file_name)
    gen_api_interface_h(info, ctp_api_file_name)
    #gen_api_interface_h_all(info, ctp_api_file_name)
    gen_api_interface_cpp(info, ctp_api_file_name)
    gen_api_impl_h(info, ctp_api_file_name)
    gen_api_impl_cpp(info, ctp_api_file_name)
    return info
    
def get_msg_str(prefix, item):
    return '%s_%s' % (prefix, str(item).lstrip().rstrip().upper())#.lstrip('ON'))
    
def get_msg_str2(prefix, item):
    return '%s_%s' % (prefix, str(item).lstrip().rstrip().upper())
    
def gen_message_h(md_info, trader_info, start_message):
    h_output = open(os.path.join(output_api_dir, 'xtp_cmessage.h'), 'w')
    try:
        macro_name = '_XTP_CMESSAGE_'
        h_output.write('''#ifndef %s\n#define %s\n\n//XTP CMessageDef\n\nenum {\n''' % (macro_name, macro_name))
        
        count = 0
        for item in md_info[1] :
            if count == 0 :
                h_output.write('''\t%s = %d,\n\n''' % (get_msg_str("MD", item[1]), start_message))
            else:
                h_output.write('''\t%s,\n\n''' % get_msg_str("MD", item[1]))
            count += 1
            
        for item in trader_info[1] :
            h_output.write('''\t%s,\n\n''' % get_msg_str("TRADER", item[1]))
        
        #h_output.write('''\t%s\n\t//Other User New Added Messages...\n\n''' % 'MAX_CTP_CMESSAGE')
        
        #....
        
        h_output.write('''};\n\nenum {\n''')
        
        count = 0
        for item in md_info[3] :
            if count == 0 :
                h_output.write('''\t%s = %d,\n\n''' % (get_msg_str2("MD", item[1]), start_message + 1000))
            else:
                h_output.write('''\t%s,\n\n''' % get_msg_str2("MD", item[1]))
            count += 1
            
        for item in trader_info[3] :
            h_output.write('''\t%s,\n\n''' % get_msg_str2("TRADER", item[1]))
        
        h_output.write('''\t%s\n\t//Other User New Added Messages...\n\n''' % 'MAX_XTP_CMESSAGE')
        #....
        h_output.write('''};\n\n#endif''')
            
    finally:
        h_output.close()

output_go_package = 'queue'

output_queues_go_dir = '../go_src/' + output_go_package

output_def_go_file = 'xtp_message.go'

def gen_def_go_file(md_info, trader_info, start_message) :
    h_output = open(os.path.join(output_queues_go_dir, output_def_go_file), 'w')
    try:
        h_output.write('''package %s\n\ntype EventType int32 \n\nconst (\n''' % output_go_package)

        count = 0
        for item in md_info[1] :
            if count == 0 :
                h_output.write('''\t%s EventType = %d + iota\n\n''' % (get_msg_str("MD", item[1]), start_message))
            else:
                h_output.write('''\t%s // %d\n\n''' % (get_msg_str("MD", item[1]), start_message + count))
            count += 1
            
        for item in trader_info[1] :
            h_output.write('''\t%s // %d\n\n''' % (get_msg_str("TRADER", item[1]), start_message + count))
            count += 1
        
        h_output.write(''')\n\nconst (\n''')
        
        count = 0
        for item in md_info[3] :
            if count == 0 :
                h_output.write('''\t%s EventType = %d + iota\n\n''' % (get_msg_str2("MD", item[1]), start_message + 1000))
            else:
                h_output.write('''\t%s // %d\n\n''' % (get_msg_str2("MD", item[1]), start_message + 1000 + count))
            count += 1
            
        for item in trader_info[3] :
            h_output.write('''\t%s // %d\n\n''' % (get_msg_str2("TRADER", item[1]), start_message + 1000 + count))
            count += 1

        h_output.write(''')\n''')
    except Exception as err:  
        print(err)
    finally:
        h_output.close()

char_arr_pattern = re.compile('typedef\schar\s([A-Za-z]{1,}Type)\[\d{1,2}\];')

enum_arr_pattern = re.compile('enum\s([A-Za-z_]{1,})\s{0,}')

output_wrapper_go_dir = '../go_src/xtp_wrapper'

output_util_go_file = 'xtp_convert_util.go'

def gen_convert_utils():
    file_object = open(os.path.join(CTP_INCLUDE_PATH, 'xtp_api_data_type.h'), encoding = 'utf-8')
    char_arrs = list()
    enum_arrs = list()
    
    try:
        all_the_text = file_object.read()
        #print all_the_text
        char_arrs = char_arr_pattern.findall(all_the_text)
        enum_arrs = enum_arr_pattern.findall(all_the_text)
    finally:
        file_object.close()
        
    #print('enum_arrs:', enum_arrs)

    enum_map = dict()
    for item in enum_arrs :
        enum_map[item] = item

    char_map = dict()
    for item in char_arrs :
        char_map[item] = item

    h_output = open(os.path.join(output_wrapper_go_dir, output_util_go_file), 'w')
    try:
        h_output.write('''package xtp_wrapper

/*
#cgo CFLAGS: -I../../C_porting_XTP/include/XTP
#include "xtp_api_data_type.h"
#include <stdlib.h>
#include <string.h>
*/
import "C"
''')
            
        count = 0
        for k, v in char_map.items() :

            h_output.write('''
func %s2CharArray(orignalStr string, output *C.%s) {
    for i := 0; i < len(orignalStr); i++ {
        (*output)[i] = C.char(orignalStr[i])
    }
}
''' % (k, k))

    except Exception as err:  
        print(err)
        return None
    finally:
        h_output.close()
        
    return enum_map

def gen_define_h(enum_map) :
    h_output = open(os.path.join(output_api_dir, 'lcdefine.h'), 'w')
    try:
        h_output.write('''#ifndef LCDEFINE_H
#define LCDEFINE_H

#include "xtp_api_struct.h"
#include "xtp_api_data_type.h"
''')

        for k, v in enum_map.items() :
            h_output.write('''\ntypedef enum %s %s_;\n''' % (k, k))
            
        h_output.write('''      
#ifdef __cplusplus
extern "C" {
#endif
\n''')
        
        for (k, v) in fields.items() :
            h_output.write("typedef struct %s %s%s;\n" % (k, GoPrefix, k))

        h_output.write('''\n#ifdef __cplusplus
}
#endif

#endif\n''')

    finally:
        h_output.close()

if __name__ == '__main__':
    gen_common_h()
    enum_map = gen_convert_utils()
    gen_define_h(enum_map)
    info1 = gen_ctp_api('xtp_quote_api', enum_map)
    info2 = gen_ctp_api('xtp_trader_api', enum_map)
    start_message = 3000
    gen_message_h(info1, info2, start_message)
    gen_def_go_file(info1, info2, start_message)
    gen_cmakelist()
