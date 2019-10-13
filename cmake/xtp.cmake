#xtp common config

SET(XTP_H_BASE ${HEADER_BASE}/XTP)

if(WIN32)

SET(XTP_LIB_BASE ${LIB_BASE}/XTP/win64)

elseif(UNIX)

SET(XTP_LIB_BASE ${LIB_BASE}/XTP/linux)

endif()
