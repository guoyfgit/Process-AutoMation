# -*- coding: utf-8 -*-
"""
author: guoyuanfei
time: 2022/4/7 16:35
remarks:

"""

import os
import time
import datetime
import zipfile
from concurrent.futures import ThreadPoolExecutor


# 定义时间格式
dateFormat = '%Y-%m-%d'
today = datetime.datetime.now()
backMove_date = datetime.timedelta(days=-5)
backMax_date = datetime.timedelta(days=-40)
move_date_Td = (today + backMove_date).strftime('%Y-%m-%d')
re_date_Td = (today + backMax_date).strftime('%Y-%m-%d')
# 定义路径参数
def backup_path():
    gw61_path = '\\\\127.0.0.1\技术组更新文件\维护组增量发布程序备份\V06.1.0\国网\服务端'
    gw61_backup_path = '\\\\127.0.0.1\gris_yfglb_db\增量服务包历史备份\维护组增量发布程序备份\V06.1.0\国网\服务端'
    nw61_path = '\\\\127.0.0.1\技术组更新文件\维护组增量发布程序备份\V06.1.0\南网\服务端'
    nw61_backup_path = '\\\\127.0.0.1\gris_yfglb_db\增量服务包历史备份\维护组增量发布程序备份\V06.1.0\南网\服务端'
    gw85_path = '\\\\127.0.0.1\技术组更新文件\维护组增量发布程序备份\V8.5\国网\服务端'
    gw85_backup_path = '\\\\127.0.0.1\gris_yfglb_db\增量服务包历史备份\维护组增量发布程序备份\V8.5\国网\服务端'
    xtgw61_path = '\\\\127.0.0.1\技术组更新文件\系统组日构建程序备份\V06.1.0\国网\服务端'
    xtgw61_backup_path = '\\\\127.0.0.1\gris_yfglb_db\增量服务包历史备份\系统组日构建程序备份\V06.1.0\国网\服务端'
    xtnw61_path = '\\127.0.0.1\技术组更新文件\系统组日构建程序备份\V06.1.0\南网\服务端'
    xtnw61_backup_path = '\\\\127.0.0.1\gris_yfglb_db\增量服务包历史备份\系统组日构建程序备份\V06.1.0\南网\服务端'
    return gw61_path , gw61_backup_path , nw61_path , nw61_backup_path, gw85_path, gw85_backup_path, xtgw61_path, xtgw61_backup_path, xtnw61_path, xtnw61_backup_path

def client_path():
    gw61_client_path = '\\\\127.0.0.1\技术组更新文件\维护组增量发布程序备份\V06.1.0\国网\客户端'
    gw61_client_backup_path = '\\\\127.0.0.1\gris_yfglb_db\增量服务包历史备份\维护组增量发布程序备份\V06.1.0\国网\客户端'
    nw61_client_path = '\\\\127.0.0.1\技术组更新文件\维护组增量发布程序备份\V06.1.0\南网\客户端'
    nw61_client_backup_path = '\\\\127.0.0.1\gris_yfglb_db\增量服务包历史备份\维护组增量发布程序备份\V06.1.0\南网\客户端'
    gw85_client_path = '\\\\127.0.0.1\技术组更新文件\维护组增量发布程序备份\V8.5\国网\客户端'
    gw85_client_backup_path = '\\\\127.0.0.1\gris_yfglb_db\增量服务包历史备份\维护组增量发布程序备份\V8.5\国网\客户端'
    xtgw61_client_path = '\\\\127.0.0.1\技术组更新文件\系统组日构建程序备份\V06.1.0\国网\客户端'
    xtgw61_client_backup_path = '\\\\127.0.0.1\gris_yfglb_db\增量服务包历史备份\系统组日构建程序备份\V06.1.0\国网\客户端'
    xtnw61_client_path = '\\127.0.0.1\技术组更新文件\系统组日构建程序备份\V06.1.0\南网\客户端'
    xtnw61_client_backup_path = '\\\\127.0.0.1\gris_yfglb_db\增量服务包历史备份\系统组日构建程序备份\V06.1.0\南网\客户端'
    return gw61_client_path, gw61_client_backup_path, nw61_client_path, nw61_client_backup_path, gw85_client_path, gw85_client_backup_path, xtgw61_client_path, xtgw61_client_backup_path, xtnw61_client_path, xtnw61_client_backup_path

# 获取创建时间超过五天的备份并迁移
def get_dir_list(path1,path2):
    dir_list = []
    for dir in os.listdir(path1):
        dir_time = datetime.datetime.fromtimestamp(os.path.getctime(path1 + '\\' + dir)).strftime('%Y-%m-%d')
        if dir_time < move_date_Td:
            dir_list.append(dir)
            print("打包压缩中...")
            #循环把dirlist里的文件夹打包压缩
            for dir_name in dir_list:
                zip_file_name = dir_name + '.zip'
                zip_file_path = path2 + '\\' + zip_file_name
                zip_file = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
                for dir_path, dir_names, file_names in os.walk(path1 + '\\' + dir_name):
                    # 将目录下的文件夹和文件都打包
                    for file_name in file_names:
                        zip_file.write(os.path.join(dir_path, file_name))
                zip_file.close()
                print("%s打包压缩完成" % zip_file_name)
                time.sleep(5)
                print("开始清理%s压缩源文件..." % dir_name)
                # 删除原文件夹
                os.system('rd /s /q %s\\%s' % (path1, dir_name))
                print("清理完成！")
                time.sleep(1)
    return dir_list

# 获取超过时间四十天的备份并清理
def get_dir_list_clean(path):
    dir_clean_list = []
    for dir in os.listdir(path):
        dir_time = datetime.datetime.fromtimestamp(os.path.getctime(path + '\\' + dir)).strftime('%Y-%m-%d')
        if dir_time < re_date_Td:
            dir_clean_list.append(dir)
            print("准备开始清理以下备份文件夹：" + dir)
            os.system('rd /s /q %s\\%s' % (path, dir))
            print("清理完成：" + dir)
            time.sleep(1)
    return dir_clean_list


if __name__ == '__main__' :
    print("devops----------##########----------")
    print("Start time :" + today.strftime('%Y-%m-%d %H:%M:%S'))
    print("devops------------------------------")
    print("本次任务为转移%s前的备份文件,且超过%s的备份文件将被清理!" % (move_date_Td, re_date_Td))
    #循环处理服务包备份
    for i in range(0,len(backup_path()),2):
        get_dir_list(backup_path()[i],backup_path()[i+1])
        get_dir_list_clean(backup_path()[i+1])
    #循环处理客户端备份
    for i in range(0,len(client_path()),2):
        get_dir_list(client_path()[i],client_path()[i+1])
        get_dir_list_clean(client_path()[i+1])
    print("devops------------------------------")
    print("End time :" + today.strftime('%Y-%m-%d %H:%M:%S'))


    # 双线程同时处理备份转移和备份清理，考虑硬盘处理速率暂时停用，相关模块未导入。
    #多线程循环处理服务包备份
    # for i in range(0,len(backup_path()),2):
    #     t1 = threading.Thread(target=get_dir_list,args=(backup_path()[i],backup_path()[i+1]))
    #     t1.start()
    #     t2 = threading.Thread(target=get_dir_list_clean,args=(backup_path()[i+1]))
    #     t2.start()
    #多线程循环处理客户端备份
    # for i in range(0,len(client_path()),2):
    #     t1 = threading.Thread(target=get_dir_list,args=(client_path()[i],client_path()[i+1]))
    #     t1.start()
    #     t2 = threading.Thread(target=get_dir_list_clean,args=(client_path()[i+1]))
