#common config

SET(HEADER_BASE ${CMAKES_ROOT}/include)
SET(LIB_BASE ${CMAKES_ROOT}/lib)

SET(THIRD_PARTY_HEADER_BASE ${THIRD_PARTY_ROOT}/include)

SET(THIRD_PARTY_LIB_BASE ${THIRD_PARTY_ROOT}/lib)

macro(rw_module_source_all)  
    file(GLOB_RECURSE rw_module_source_list . "*.c*" "*.h" "*.hpp" "*.inl")  
    aux_source_directory(. rw_module_source_list)  
endmacro(rw_module_source_all)
