import os
import re
import random


headers = []
cpp_files    = []
dirs = []
filters_file_name = ""
other_files = [] # .conf makefile
def get_file_path(root_path,file_list,dir_list,start):
    #获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        #获取目录或者文件的路径
        dir_file_path = os.path.join(root_path,dir_file)
        #判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            if dir_file == ".git":
                continue
            dir_list.append(dir_file_path)
            #递归获取所有文件和目录的路径
            get_file_path(dir_file_path,file_list,dir_list,start)
        else:
            file_list.append(dir_file_path)
            project_file_name = dir_file_path[start:]
            valid_cpp_types = ["cpp","c","cc","cxx"]        # 源文件类型
            valid_header_types = ["h","hh","hpp","hxx"]     #头文件类型
            other_types = ["makefile","conf","tars"]        # 其它文件类型
            valid_ext_type = valid_cpp_types + valid_header_types
            for t in valid_ext_type:
                cmd = ".*\." + t + "$"
                pattern = re.compile(cmd)
                if pattern.match(project_file_name):
                    if t in valid_header_types:
                        headers.append(project_file_name)
                    else:
                        cpp_files.append(project_file_name)
                    vs_filter_end = str(project_file_name).rfind("\\")
                    if vs_filter_end != -1:
                        dir_name = project_file_name[0 :vs_filter_end]
                        if dir_name not in dirs:
                            dirs.append(dir_name)
            # conf 和makefileif  和 tars
            for t in other_types:
                cmd = ".*" + t + "$"
                pattern = re.compile(cmd)
                if pattern.match(project_file_name):
                    other_files.append(project_file_name)
                    vs_filter_end = str(project_file_name).rfind("\\")
                    if vs_filter_end != -1:
                        dir_name = project_file_name[0 :vs_filter_end]
                        if dir_name not in dirs:
                            dirs.append(dir_name)

def get_unique_id():
    s = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwzyx"
    _id = ""
    for i in range(0,36):
        if i == 8 or i == 13 or i == 18 or i == 23:
            _id = _id + "-"
        else:
            _id = _id + s[random.randint(0, len(s) -1)]
    print(_id)
    return _id
def create_dir(dir_names):
    msg = '<ItemGroup>\n'
    for dir_name in dir_names:
        msg += '<Filter Include="' + dir_name + '">\n'
        msg += '<UniqueIdentifier>{' + get_unique_id() + '}</UniqueIdentifier>\n'
        msg += '</Filter>\n'
    msg +='</ItemGroup>\n'
    return msg

#    <ClCompile Include="OuterFactoryImp.cpp">
#      <Filter>Source Files</Filter>
#    </ClCompile>
def create_cpp_item_group(cpp_file_names):
    msg = '<ItemGroup>\n'
    for file_name in cpp_file_names:
        idx = str(file_name).rfind('\\')
        if idx == -1:
            msg += '<ClCompile Include="' + file_name + '" />\n'
        else:
            msg += '<ClCompile Include="' + file_name + '">\n'
            msg += '<Filter>' + file_name[0:idx] + '</Filter>\n'
            msg += '</ClCompile>\n'
    msg += '</ItemGroup>\n'
    return msg

def create_header_item_group(header_file_names):
    msg = '<ItemGroup>\n'
    for file_name in header_file_names:
        idx = str(file_name).rfind('\\')
        if idx == -1:
            msg += '<ClInclude Include="' + file_name + '" />\n'
        else:
            msg += '<ClInclude Include="' + file_name + '">\n'
            msg += '<Filter>' + file_name[0:idx] + '</Filter>\n'
            msg += '</ClInclude>\n'
    msg += '</ItemGroup>\n'
    return msg

def create_other_item_group(other_file_names):
    msg = '<ItemGroup>\n'
    for file_name in other_file_names:
        idx = str(file_name).rfind('\\')
        if idx == -1:
            msg += '<None Include="' + file_name + '" />\n'
        else:
            msg += '<None Include="' + file_name + '">\n'
            msg += '<Filter>' + file_name[0:idx] + '</Filter>\n'
            msg += '</None>\n'
    msg += '</ItemGroup>\n'
    return msg

def get_filters_name(root_path):
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        #获取目录或者文件的路径
        dir_file_path = os.path.join(root_path,dir_file)
        #判断该路径为文件还是路径
        if not os.path.isdir(dir_file_path):
            pattern = re.compile(".*\.filters$")
            if pattern.match(dir_file):
                print(dir_file)
                return dir_file_path
    return None

def create_vs_filters(dirs,cpp_file_names,header_file_names):
    file = open(filters_file_name, "w", encoding="utf8")
    msg = ""
    msg +='<?xml version="1.0" encoding="utf-8"?>\n'
    msg += '<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">\n'
    msg += create_dir(dirs)
    msg += create_cpp_item_group(cpp_file_names)
    msg += create_header_item_group(header_file_names)
    msg += create_other_item_group(other_files)
    msg += '</Project>'

    file.write(msg)
    file.close()


file_list = []
dir_list = []
root_path = "."
get_file_path(root_path, file_list,dir_list,len(root_path) +1)

print("****************")
print(headers)
print(cpp_files)
print(dirs)

filters_file_name = get_filters_name(root_path)
if filters_file_name is None:
    raise NameError("Can not find filters_file!")
create_vs_filters(dirs,cpp_files, headers)