'''
Description:使用Pandas拼接多个CSV文件到一个文件（即合并）
'''
import re

import pandas as pd
import os

Folder_Path = r'C:\Users\92994\PycharmProjects\COVID-19\rawData'# 要拼接的文件夹及其完整路径
SaveFile_Path = r'C:\Users\92994\PycharmProjects\COVID-19\rawData'  # 拼接后要保存的文件路径
SaveFile_Name = r'all.csv'  # 合并后要保存的文件名

def combine():

    # 修改当前工作目录
    os.chdir(Folder_Path)
    # 将该文件夹下的所有文件名存入一个列表
    file_list = os.listdir()
    if 'all.csv' in file_list:
        file_list.remove('all.csv')


    # 读取第一个CSV文件并包含表头
    df = pd.read_csv(Folder_Path + '\\' + file_list[0],encoding='gbk')  # 编码默认UTF-8，若乱码自行更改
    col_name=df.columns.tolist()                   # 将数据框的列名全部提取出来存放在列表里


    col_name.insert(0,'date')                      # 在列索引为2的位置插入一列,列名为:city，刚插入时不会有值，整列都是NaN
    df=df.reindex(columns=col_name)              # DataFrame.reindex() 对原行/列索引重新构建索引值
    print(col_name)
    df['date']=[file_list[0].split('.')[0] for i in range(len(df))]   # 给date列赋值


    # 将读取的第一个CSV文件写入合并后的文件保存
    df.to_csv(SaveFile_Path + '\\' + SaveFile_Name,encoding='gbk', index=False)

    # 循环遍历列表中各个CSV文件名，并追加到合并后的文件
    for i in range(1, len(file_list)):
        df = pd.read_csv(Folder_Path + '\\' + file_list[i],encoding='gbk')
        # print(col_name)
        df=df.reindex(columns=col_name)
        df['date'] = [file_list[i].split('.')[0] for j in range(len(df))]  # 给city列赋值
        df.to_csv(SaveFile_Path + '\\' + SaveFile_Name, encoding='gbk', index=False, header=False, mode='a+')

def clean():
    df = pd.read_csv(Folder_Path + '\\' + 'all.csv', encoding='gbk')
    for i in range(len(df['totalPopulation'])):
        e=df['totalPopulation'][i]
        e=str(e)
        e= re.sub("\D", "", e)
        if e != '':
            e = int(e)
        df['totalPopulation'][i]=e
    df.to_csv(SaveFile_Path + '\\' + SaveFile_Name, encoding='gbk', index=False, header=True, mode='w')

if __name__ == '__main__':
    # combine();
    # clean();
    df = pd.read_csv(Folder_Path + '\\' + 'all.csv', encoding='gbk')
    print(df)
    world=df[df.name=='全球']
    print(world)
