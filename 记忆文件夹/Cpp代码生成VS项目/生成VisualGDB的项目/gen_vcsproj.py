import re
import os
headers = []
cpp_files    = []
dirs = []
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
            valid_cpp_types = ["cpp","c","cc","cxx"]
            valid_header_types = ["h","hh","hpp","hxx"]
            other_types = ["makefile","conf","tars","vgdbsettings"]        # 其它文件类型
            valid_ext_type = valid_cpp_types + valid_header_types
            for t in valid_ext_type:
                cmd = ".*\." + t + "$"
                pattern = re.compile(cmd)
                # print("cmd:" + cmd)
                if pattern.match(project_file_name):
                    if t in valid_header_types:
                        headers.append(project_file_name)
                    else:
                        cpp_files.append(project_file_name)
                # if t in project_file_name:
                #     print(project_file_name)
                #
                #     if ".cpp" in project_file_name:
                #         cpp_files.append(project_file_name)
                #     else:
                #         headers.append(project_file_name)
                    vs_filter_end = str(project_file_name).rfind("\\")
                    if vs_filter_end != -1:
                        dir_name = project_file_name[0 :vs_filter_end]
                        if dir_name not in dirs:
                            dirs.append(dir_name)
                        # print(project_file_name[0 :vs_filter_end])
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


def create_cpp_item_group(cpp_file_names):
    msg = '<ItemGroup>\n'
    for file_name in cpp_file_names:
        msg += '\t<ClCompile Include="' + file_name + '" />\n'
    msg += '</ItemGroup>\n'
    return msg

def create_header_item_group(header_file_names):
    msg = '<ItemGroup>\n'
    for file_name in header_file_names:
        msg += '\t<ClInclude Include="' + file_name + '" />\n'
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

def get_vcxproj_name(root_path,postfix):
    dir_or_files = os.listdir(root_path)
    target_files = []
    for dir_file in dir_or_files:
        #获取目录或者文件的路径
        dir_file_path = os.path.join(root_path,dir_file)
        #判断该路径为文件还是路径
        if not os.path.isdir(dir_file_path):
            pattern = re.compile(".*\.{0}$".format(postfix))
            if pattern.match(dir_file):
                print(dir_file)
                target_files.append(dir_file)
                #return dir_file_path
    return target_files

file_list = []
dir_list = []
root_path = "."
get_file_path(root_path, file_list,dir_list,len(root_path)+1)

vcsproj_file_name = get_vcxproj_name(root_path,"vcxproj")[0]

vgdbsetting_files = get_vcxproj_name(root_path,"vgdbsettings")

if vcsproj_file_name is None:
    raise NameError("Can not find vcsproj_file!")

file = open(vcsproj_file_name, "r", encoding="utf8")

lines = file.readlines()

file.close()
start = False

item_group_start = -1
item_group_end   = -1
for i in range(len(lines)):
    line = lines[i]
    line = str(line).strip()
    if line == '<ItemGroup>' and item_group_start == -1:
        item_group_start = i
        continue
    if line == '</ItemGroup>':
        item_group_end = i
        if item_group_end == item_group_start + 1:  # 有个无内容的ItemGroup 元素
            item_group_start = -1
        


cpp_items = create_cpp_item_group(cpp_files)
headers_items = create_header_item_group(headers)
other_items = create_other_item_group(other_files)
lines = lines[0:item_group_start] + [cpp_items,headers_items, other_items] + lines[item_group_end+1:]
print(''.join(lines).encode('GBK', 'ignore').decode())  # UTF8-BOM 打印出错,忽略不可打印的字符

# 写入文件
file = open(vcsproj_file_name, "w", encoding="utf8")
for line in lines:
    file.write(line)
file.close()


