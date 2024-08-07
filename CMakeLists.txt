cmake_minimum_required(VERSION 3.13)
project(radicon_arrow CXX)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib)

add_library(blue_control STATIC ${CMAKE_SOURCE_DIR}/src/blue_control.cpp)
add_library(key_input STATIC ${CMAKE_SOURCE_DIR}/src/key_input.cpp)
add_library(motor STATIC ${CMAKE_SOURCE_DIR}/src/motor.cpp)

add_executable(${PROJECT_NAME} ${CMAKE_SOURCE_DIR}/src/radicon_arrow.cpp)

target_link_libraries(${PROJECT_NAME} blue_control)
target_link_libraries(${PROJECT_NAME} key_input)
target_link_libraries(${PROJECT_NAME} motor)

include_directories(${CMAKE_SOURCE_DIR}/include)
