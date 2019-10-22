import os
# usage
# 把需要更新的服务名加入即可
projs = ["chatserver",
         "configserver",
         "dataproxyserver",
         "dbagentserver",
         "dz",
         "friendsserver",
         "loginserver",
         "mailserver",
         "rankserver",
         "roomserver",
         "routerserver",
         "userinfoserver"]

for server in projs:
    work_dir = "..\\" + server
    os.chdir(work_dir) # 改变工作目录
    os.system("python C:\\Users\\user\\dzProject\\src\\all_proj\\gen_filters.py")
    os.system("python C:\\Users\\user\\dzProject\\src\\all_proj\\gen_vcsproj.py")

print("已经全部重新生成vs项目!")

