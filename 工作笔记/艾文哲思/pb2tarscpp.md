# 编译步骤

```shell
cd
cd /root/Tars/cpp/tools/pb2tarscpp
mkdir build
cd ./build
cmake ../
make -j4
cp ./bin/pb2tarscpp /usr/local/app/tars/
cd
```



CMakeList.txt

```cmake
set(MODULE "pb2tarscpp")

set(EXECUTABLE_OUTPUT_PATH "${PROJECT_BINARY_DIR}/bin")
    
include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
CHECK_CXX_COMPILER_FLAG("-std=c++0x" COMPILER_SUPPORTS_CXX0X)

# 使用变量设置编译标志
if(COMPILER_SUPPORTS_CXX11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
elseif(COMPILER_SUPPORTS_CXX0X)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
else()
message(STATUS "The compiler ${CMAKE_CXX_COMPILER} has no C++11 support. Please use a different C++ compiler.")
endif()

aux_source_directory(. DIR_SRCS)
    
link_libraries(protobuf;protoc;pthread)
    
add_executable("pb2tarscpp"  ${DIR_SRCS})

install(TARGETS "pb2tarscpp"
        RUNTIME DESTINATION tools)
```

