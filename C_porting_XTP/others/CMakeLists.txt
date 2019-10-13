CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

SET(LIBRARY_OUTPUT_PATH ${XTP_CAPI_LIB_BASE})

SET(build_target "CXTPApi")

INCLUDE_DIRECTORIES (
    ${XTP_H_BASE}
    ${XTP_CAPI_H_BASE}
)

LINK_DIRECTORIES (
    ${XTP_LIB_BASE}
)

# generate project
#rw_module_source_list
rw_module_source_all()

message(STATUS "XTP_H_BASE="${XTP_H_BASE})
message(STATUS "XTP_CAPI_H_BASE="${XTP_CAPI_H_BASE})

FILE(GLOB_RECURSE interface_files ${XTP_H_BASE}/*.h)

FILE(GLOB_RECURSE interface_files_2 ${XTP_CAPI_H_BASE}/*.h)

source_group(implmentation FILES ${rw_module_source_list})

source_group(xtp_api FILES ${interface_files})

source_group(xtp_capi FILES ${interface_files_2})

add_library(
    ${build_target}

    SHARED

    ${rw_module_source_list}
    ${interface_files}
    ${interface_files_2}
)

IF (MSVC)

ADD_DEFINITIONS(-DWIN32)
ADD_DEFINITIONS(-DDLL_EXPORT)

target_link_libraries (
    ${build_target}
    
    xtpquoteapi.lib
    xtptraderapi.lib
)

ELSE (MSVC)

target_link_libraries ( 
    ${build_target}
    
    xtpquoteapi
    xtptraderapi
)

ENDIF (MSVC)

set_source_files_properties(${build_target} PROPERTIES
       COMPILE_FLAGS  "${EXTRA_OPTIONS}")

get_target_property(target_file_name ${build_target} LOCATION)

add_custom_command(TARGET ${build_target} POST_BUILD 
                   COMMAND ${CMAKE_COMMAND} -E copy ${target_file_name} ${BIN_PATH}/$(Configuration)
                   )

set_target_properties( ${build_target} PROPERTIES LINKER_LANGUAGE "CXX")
