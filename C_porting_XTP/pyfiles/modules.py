#!/usr/bin/python
#! -*- encoding=utf-8 -*-

import os

from defines import *

from utils import *

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

#endif\n''' % (LC_XTP_API, LC_XTP_API, LC_XTP_API))
        
#define SCR_PRINT(arg, ...)     printf(arg, ##__VA_ARGS__)\n

#include<stdlib.h>

#endif\n''' % (LC_XTP_API, LC_XTP_API, LC_XTP_API))

    finally:
        file_object.close()
        
def gen_convert_utils():
    file_object = open(os.path.join(XTP_INCLUDE_PATH, 'xtp_api_data_type.h'), encoding = 'utf-8')
    char_arrs = list()
    enum_arrs = list()
    
    try:
        all_the_text = file_object.read()
        #print(all_the_text)
        char_arrs = char_arr_pattern.findall(all_the_text)
        enum_arrs = enum_arr_pattern.findall(all_the_text)
    finally:
        file_object.close()
        
    print('char_arrs:', char_arrs)
    print('enum_arrs:', enum_arrs)

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
#cgo CFLAGS: -Wno-error=implicit-function-declaration -I../../C_porting_XTP/include/XTP -I../../C_porting_XTP/include/CXTPApi
#include <stdlib.h>
#include <string.h>
#include "common_macro.h"
#include "xtp_api_struct.h"
*/
import "C"
''')
            
    #    for k, _ in char_map.items() :

    #        h_output.write('''
#func %s2CharArray(orignalStr string, output *C.%s) {
#    for i := 0; i < len(orignalStr); i++ {
#        (*output)[i] = C.char(orignalStr[i])
#    }
#}
#''' % (k, k))

    except Exception as err:  
        print(err)
        return None
    finally:
        h_output.close()
        
    return enum_map

def cp_cmakelist() :
    shutil.copyfile(os.path.join(others_dir, 'CMakeLists.txt'), os.path.join(output_dir, 'CMakeLists.txt'))

def get_class_info(xtp_api_file_name):
    file_object = open(os.path.join(XTP_INCLUDE_PATH, '%s.h' % xtp_api_file_name), encoding = 'utf-8')
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

def gen_api_interface_h(info, xtp_api_file_name):
    output_filename = get_api_interface_h_name(xtp_api_file_name)

    macro_name = output_filename.upper().replace('.', '_')
    h_output = open(os.path.join(output_api_dir, output_filename), 'w')
    try:

        h_output.write('#ifndef %s\n#define %s\n\n'% (macro_name, macro_name))
        h_output.write('#include "%s"\n' % COMMON_H)
        h_output.write('''\n#include "lcdefine.h"\n\n#ifdef __cplusplus\nextern "C" {\n#endif\n''')
        
        for item in info[1]:
            func_name = get_FN_name(xtp_api_file_name, item[1])
            if item[2] == '' :
                h_output.write('typedef %s (* %s)();\n' % (item[0], func_name))
            else :
                h_output.write('typedef %s (* %s)(%s);\n' % (item[0], func_name, get_interface_params(item[2])))

        h_output.write('\n//register callbacks\n')
        h_output.write('%s void * Create%s();\n' % (LC_XTP_API, '%s%s' % (LC_PREFIX, getSpiClassName(info))))
        h_output.write('%s void Release%s(void * * %s);\n' % (LC_XTP_API, '%s%s' % (LC_PREFIX, getSpiClassName(info)), pSpi_name))
        for item in info[1]:
            h_output.write('%s void %s(void * %s, %s pCallback);\n' % (LC_XTP_API, get_Register_Callback_Name(xtp_api_file_name, item[1]), pSpi_name, get_FN_name(xtp_api_file_name, item[1])))
        
        h_output.write('\n//api method porting\n')
        
        h_output.write('%s void * Create%s(uint8_t %s, const char * %s, XTP_LOG_LEVEL %s);\n'
                           % (LC_XTP_API, '%s%s' % (LC_PREFIX, getApiClassName(info)), client_id, save_file_path, log_level))

        h_output.write('%s void Release%s(void * * %s);\n' % (LC_XTP_API, '%s%s' % (LC_PREFIX, getApiClassName(info)), pApi_name))
        for item in info[3]:
            if item[1] == RegisterSpi :
                h_output.write('%s void %s(void * %s, void * %s);\n' % (LC_XTP_API, get_Api_Function_Name(xtp_api_file_name, item[1]), pApi_name, pSpi_name))
                continue
            if item[2] == '' :
                h_output.write('%s %s %s(void * %s);\n' % (LC_XTP_API, item[0], get_Api_Function_Name(xtp_api_file_name, item[1]), pApi_name))
            else :
                h_output.write('%s %s %s(void * %s, %s);\n' % (LC_XTP_API, item[0], get_Api_Function_Name(xtp_api_file_name, item[1]), pApi_name, get_interface_params(item[2])))

        #'''
        h_output.write('\n// define extern functions\n')

        for item in info[1]:
            func_name = get_Go_FN_name(xtp_api_file_name, item[1])
            if not isInlist(func_name) :
                continue
            if item[2] == '' :
                h_output.write('extern void %s(%s);\n' % (func_name, Extern_Ptr_Param))
            else :
                h_output.write('extern void %s(%s, %s);\n' % (func_name, Extern_Ptr_Param, get_interface_params(item[2], True)))
        #'''

        h_output.write('''\n#ifdef __cplusplus\n}\n#endif\n#endif\n''')
    finally:
        h_output.close()

def gen_api_interface_h_all(info, xtp_api_file_name):
    output_filename = get_api_interface_h_name(xtp_api_file_name)
    output_filename_all = get_api_interface_h_name_all(xtp_api_file_name)

    macro_name = output_filename.upper().replace('.', '_')
    h_output_all = open(os.path.join(output_api_dir, output_filename_all), 'w')
    try:

        h_output_all.write('#ifndef %s\n#define %s\n\n'% (macro_name, macro_name))
        h_output_all.write('#include "%s"\n' % COMMON_H)
        h_output_all.write('''\n#include "lcdefine.h"\n#include "%s"\n#ifdef __cplusplus\nextern "C" {\n#endif\n''' % (output_filename))

        h_output_all.write('\n// define extern functions\n')

        for item in info[1]:
            func_name = get_Go_FN_name(xtp_api_file_name, item[1])
            if not isInlist(func_name) :
                continue
            if item[2] == '' :
                h_output_all.write('extern void %s(%s);\n' % (func_name, Extern_Ptr_Param))
            else :
                h_output_all.write('extern void %s(%s, %s);\n' % (func_name, Extern_Ptr_Param, get_interface_params(item[2], True)))
        h_output_all.write('''\n#ifdef __cplusplus\n}\n#endif\n#endif\n''')
    finally:
        h_output_all.close()

def gen_api_interface_cpp(info, xtp_api_file_name):
    print ('\n---gen_api_interface_cpp xtp_api_file_name=', xtp_api_file_name, '\n')
    output_filename = '%s%s.cxx' % (LC_PREFIX, xtp_api_file_name)
    h_output = open(os.path.join(output_dir, output_filename), 'w')
    try:
        h_output.write('''#include "%s"\n''' % (get_api_interface_h_name(xtp_api_file_name)))
        h_output.write('''#include "%s"\n\n''' % get_api_impl_h_name(xtp_api_file_name))
        
        #spi
        h_output.write('\n// --- gen_api_interface_cpp spi ---\n')

        h_output.write('%s void * Create%s()\n{\n\treturn (void *)(new %s);\n}\n\n'
                       % (LC_XTP_API, '%s%s' % (LC_PREFIX, getSpiClassName(info)), get_spi_class_name(info)))
        h_output.write('%s void Release%s(void * * %s)\n{\n\tif (*%s != NULL)\n\t{\n\t\tdelete *%s;\n\t\t*%s = NULL;\n\t}\n}\n\n'
                       % (LC_XTP_API, '%s%s' % (LC_PREFIX, getSpiClassName(info)), pSpi_name, pSpi_name, pSpi_name, pSpi_name))

        for item in info[1]:
            h_output.write('void %s(void * %s, %s pCallback)\n' % (get_Register_Callback_Name(xtp_api_file_name, item[1]), pSpi_name, 
                get_FN_name(xtp_api_file_name, item[1])))
            h_output.write('{\n\tif (%s != NULL)\n\t{\n\t\t(Get%s(%s))->%s(pCallback);\n\t}\n}\n'
                % (pSpi_name, get_spi_class_name(info), pSpi_name, get_Register_Callback_Name(xtp_api_file_name, item[1])))
        
        #api
        h_output.write('\n// --- gen_api_interface_cpp api ---\n')

        h_output.write('''%s void * Create%s(uint8_t %s, const char * %s, XTP_LOG_LEVEL %s)
            \n{\n\treturn (void *)(%s::Create%s(%s, %s, %s));\n}\n\n'''
            % (LC_XTP_API, '%s%s' % (LC_PREFIX, getApiClassName(info)), client_id, save_file_path, log_level,
            getApiClassName(info), getApiClassName(info), client_id, save_file_path, log_level))
        
        h_output.write('void Release%s(void * * %s)\n{\n\tif (*%s != NULL)\n\t{\n\t\tdelete *%s;\n\t\t*%s = NULL;\n\t}\n}\n\n'
            % ('%s%s' % (LC_PREFIX, getApiClassName(info)), pApi_name, pApi_name, pApi_name, pApi_name))

        for item in info[3]:
            if item[1] == RegisterSpi :
                h_output.write('%s void %s(void * %s, void * %s)\n' % (LC_XTP_API, get_Api_Function_Name(xtp_api_file_name, item[1]), pApi_name, pSpi_name))
                h_output.write('{\n\tif (%s != NULL)\n\t{\n\t\t(Get%s(%s))->%s(Get%s(%s));\n\t}\n}\n\n'
                    %(pApi_name, getApiClassName(info), pApi_name, RegisterSpi, get_spi_class_name(info), pSpi_name))
                continue
            
            attach_1 = ''
            attach_2 = ''

            if item[0] != 'void' :
                attach_1 = 'return '
                attach_2 = '\n\treturn -1;'
                
            #if ( get_Api_Function_Name(xtp_api_file_name, item[1]) == '_quote_apiSubscribeAllOptionMarketData') :
                #print('spi item:', item)
                #print('--> get_Api_Function_Name:', get_Api_Function_Name(xtp_api_file_name, item[1]))
                #print('get_interface_params:', get_interface_params(item[2]))

            if item[2] == '' :
                h_output.write('%s %s %s(void* %s)\n' % (LC_XTP_API, item[0], get_Api_Function_Name(xtp_api_file_name, item[1]), pApi_name))
                h_output.write('{\n\tif (%s != NULL)\n\t{\n\t\t%s(Get%s(%s))->%s();\n\t}%s\n}\n\n'
                           % (pApi_name, attach_1, getApiClassName(info), pApi_name, item[1], attach_2))
            else :
                h_output.write('%s %s %s(void* %s, %s)\n' % (LC_XTP_API, item[0], get_Api_Function_Name(xtp_api_file_name, item[1]), pApi_name, get_interface_params(item[2])))
                h_output.write('{\n\tif (%s != NULL)\n\t{\n\t\t%s(Get%s(%s))->%s(%s);\n\t}%s\n}\n\n'
                           % (pApi_name, attach_1, getApiClassName(info), pApi_name, item[1], get_impl_params(item[2]), attach_2))        
    finally:
        h_output.close()
    return output_filename

def gen_api_impl_h(info, xtp_api_file_name):
    output_filename = get_api_impl_h_name(xtp_api_file_name)
    macro_name = output_filename.upper().replace('.', '_')
    h_output = open(os.path.join(output_dir, output_filename), 'w')
    try:
        h_output.write('''#ifndef %s\n#define %s\n#include "%s.h"\n#include "%s"\n\nusing namespace XTP::API;\n\n'''
                       % (macro_name, macro_name, xtp_api_file_name, get_api_interface_h_name(xtp_api_file_name)))
        h_output.write('class %s : public %s\n{\nprivate:\n\n' % (get_spi_class_name(info), getSpiClassName(info)))
        for item in info[1]:
            h_output.write('\t%s m_%s;\n' % (get_FN_name(xtp_api_file_name, item[1]), get_FN_name(xtp_api_file_name, item[1])))
        h_output.write('\npublic:\n')
        for item in info[1]:
            h_output.write('\tvoid %s(%s _%s);\n' % (get_Register_Callback_Name(xtp_api_file_name, item[1]), get_FN_name(xtp_api_file_name, item[1]), get_FN_name(xtp_api_file_name, item[1])))
            
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

def gen_api_impl_cpp(info, xtp_api_file_name):
    h_output = open(os.path.join(output_dir, get_api_impl_cpp_name(xtp_api_file_name)), 'w')
    try:
        
        h_output.write('#include <cstdio>\n')
        h_output.write('#include "%s"\n\n' % (get_api_impl_h_name(xtp_api_file_name)))
        h_output.write('%s * Get%s(void * %s)\n{\n' % (get_spi_class_name(info), get_spi_class_name(info), pSpi_name))
        h_output.write('\treturn (%s *)(%s);\n}\n\n' % (get_spi_class_name(info), pSpi_name))
        h_output.write('%s * Get%s(void * %s)\n{\n' % (getApiClassName(info), getApiClassName(info), pApi_name))
        h_output.write('\treturn (%s *)(%s);\n}\n\n' % (getApiClassName(info), pApi_name))
        
        h_output.write('%s::%s()\n{\n' % (get_spi_class_name(info), get_spi_class_name(info)))
        
        for item in info[1]:
            h_output.write('\t m_%s = NULL;\n' % (get_FN_name(xtp_api_file_name, item[1])))
        
        h_output.write('}\n\n')
        
        h_output.write('%s::~%s()\n{}\n\n' % (get_spi_class_name(info), get_spi_class_name(info)))
        
        for item in info[1]:
            h_output.write('void %s::%s(%s _%s)\n{\n'
                           % (get_spi_class_name(info), get_Register_Callback_Name(xtp_api_file_name, item[1]), get_FN_name(xtp_api_file_name, item[1]), get_FN_name(xtp_api_file_name, item[1])))
            h_output.write('\t m_%s = _%s;\n' % (get_FN_name(xtp_api_file_name, item[1]), get_FN_name(xtp_api_file_name, item[1])))
            h_output.write('}\n\n')
            
        for item in info[1]:
            h_output.write('%s %s::%s(%s)\n{\n' % (item[0], get_spi_class_name(info), item[1], item[2]))
            func_name = get_FN_name(xtp_api_file_name, item[1])

            ## todo list
            '''
            if (item[2] == '') :
                h_output.write('\t(*m_%s)();\n' % (func_name))
            else :
                h_output.write('\t(*m_%s)(%s);\n' % (func_name, get_impl_params(item[2])))
            '''            
            func_name = get_Go_FN_name(xtp_api_file_name, item[1])

            print(func_name, ' ', isInlist(func_name))

            if not isInlist(func_name) :
                h_output.write('}\n\n')
                continue
            
            h_output.write('\t printf("%s--%%s", "%s");\n' % (func_name, func_name))
            if (item[2] == '') :
                h_output.write('\t %s(%s);\n' % (func_name, VOID_PTR))
                h_output.write('\t// \t(*m_%s)();\n' % (func_name))
            else :
                h_output.write('\t %s(%s, %s);\n' % (func_name, VOID_PTR, get_impl_params(item[2])))
                h_output.write('\t// \t(*m_%s)(%s);\n' % (func_name, get_impl_params(item[2])))
            #'''

            h_output.write('}\n\n')
        
    finally:
        h_output.close()
    
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
        
        #h_output.write('''\t%s\n\t//Other User New Added Messages...\n\n''' % 'MAX_XTP_CMESSAGE')
        #....
        
        h_output.write('''};\n\nenum {\n''')
        
        count = 0
        for item in md_info[3] :
            if count == 0 :
                h_output.write('''\t%s = %d,\n\n''' % (get_msg_str("MD", item[1]), start_message + 1000))
            else:
                h_output.write('''\t%s,\n\n''' % get_msg_str("MD", item[1]))
            count += 1
            
        for item in trader_info[3] :
            h_output.write('''\t%s,\n\n''' % get_msg_str("TRADER", item[1]))
        
        h_output.write('''\t%s\n\t//Other User New Added Messages...\n\n''' % 'MAX_XTP_CMESSAGE')
        #....
        h_output.write('''};\n\n#endif''')
            
    finally:
        h_output.close()

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
                h_output.write('''\t%s EventType = %d + iota\n\n''' % (get_msg_str("MD", item[1]), start_message + 1000))
            else:
                h_output.write('''\t%s // %d\n\n''' % (get_msg_str("MD", item[1]), start_message + 1000 + count))
            count += 1
            
        for item in trader_info[3] :
            h_output.write('''\t%s // %d\n\n''' % (get_msg_str("TRADER", item[1]), start_message + 1000 + count))
            count += 1

        h_output.write(''')\n''')
    except Exception as err:  
        print(err)
    finally:
        h_output.close()

def gen_define_h(enum_map) :
    h_output = open(os.path.join(output_api_dir, 'lcdefine.h'), 'w')
    try:
        h_output.write('''#ifndef LCDEFINE_H
#define LCDEFINE_H

#include "xtp_api_struct.h"
''')
            
        h_output.write('''      
#ifdef __cplusplus
extern "C" {
#endif\n''')

        for k, _ in untypedefedStructs.items() :
            h_output.write('''\ntypedef struct %s %s_;\n''' % (k, k))
        
        for k, _ in untypedefedEnums.items() :
            h_output.write("typedef enum %s %s%s;\n" % (k, GoPrefix, k))

        h_output.write('''\n#ifdef __cplusplus
}
#endif

#endif\n''')

    finally:
        h_output.close()

def gen_xtp_api(xtp_api_file_name):
    info = get_class_info(xtp_api_file_name)
    gen_api_interface_h(info, xtp_api_file_name)
    #gen_api_interface_h_all(info, xtp_api_file_name)
    gen_api_interface_cpp(info, xtp_api_file_name)
    gen_api_impl_h(info, xtp_api_file_name)
    gen_api_impl_cpp(info, xtp_api_file_name)
    return info
