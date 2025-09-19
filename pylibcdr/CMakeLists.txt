cmake_minimum_required(VERSION 3.0.0)
project(CDR_interface VERSION 0.1.0)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

# Правильное обнаружение Python
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

find_package(libcdr REQUIRED)
find_package(librevenge REQUIRED)

include_directories(
    ${LIBCDR_INCLUDE_DIRS} 
    ${LIBREVENGE_INCLUDE_DIRS} 
    ${Python3_INCLUDE_DIRS}
)

add_library(cdr_interface SHARED libcdr_interface.cpp core/parser.cxx)

# Правильная линковка с Python и другими библиотеками
target_link_libraries(cdr_interface 
    ${LIBCDR_LIBRARY} 
    ${LIBREVENGE_LIBRARIES}
    ${Python3_LIBRARIES}
)

# Установка флагов для Termux
set_target_properties(cdr_interface PROPERTIES
    POSITION_INDEPENDENT_CODE ON
    CXX_STANDARD 11
    CXX_STANDARD_REQUIRED YES
)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
