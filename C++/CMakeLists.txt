cmake_minimum_required(VERSION 3.25)
project(PAS)

set(CMAKE_CXX_STANDARD 23)

add_executable(PAS main.cpp Headers/bitmap.h Headers/nds.h Headers/MurmurHash3.h Sources/MurmurHash3.cpp Headers/sketch.h Sources/nds.cpp Headers/pas.h Headers/register.h Sources/pas.cpp Headers/CSE.h Sources/CSE.cpp Headers/tools.h Headers/vHLL.h Sources/vHLL.cpp)
