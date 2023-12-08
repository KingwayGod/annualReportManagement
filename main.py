#!/usr/bin/env python
# coding: utf-8


import requests
from bs4 import BeautifulSoup
import re
import os




# 定义获取文件的函数

# TODO：可以设置文件的类型
def download_file(url, directory = ".", filename = None):
    """
    从给定的url下载文件，保存到指定目录，保存为指定文件名

    :param url: 文件url
    :param directory: 保存的地址
    :param filename: 保存的文件名
    """
    # 如果没有传文件名，则取url最后一段文字作为文件名
    if filename is None:
        filename = url.split('/')[-1]
        
    # 构建完整的文件路径
    save_path = os.path.join(directory, f'{filename}.pdf')

    try:
        os.makedirs(directory, exist_ok = True)
        
        # 发送GET请求
        response = requests.get(url)

        # 检查请求是否成功
        if response.status_code == 200:
            # 以二进制写入模式打开文件
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded successfully and saved as {save_path}")
        else:
            print(f"Failed to download file: status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Error occurred: {e}")


# # 下载年度报告

def download_annual_reports(stockid, directory):
    """
    下载年度报告
    """
    # 一、定义相关变量

    # 1. 文件的下载地址
    download_base_url = 'https://file.finance.sina.com.cn/211.154.219.97:9494/MRGG/CNSESZ_STOCK/'
    # 2. 获取相关必要信息的地址
    url = f'https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/{stockid}/page_type/ndbg.phtml'

    # 二、 获取信息

    # 1. 拿到HTMl内容
    # TODO：异常处理一下 没有获取到会。。。
    response = requests.get(url)
    html = response.content

    # 2. 解析html内容
    soup = BeautifulSoup(html, "html.parser")

    # 3. 分析网页的元素 发现内容是包含在 class=datelist下的ul
    father_elements = soup.select_one('.datelist ul')

    #所需要的数据在br的前面
    children = father_elements.find_all('br')

    annual_reports = []

    for child in children:
        if child:
            annual_report_name = ""
            annual_report_id = ""
            annual_report_date = ""

            # 通过兄弟节点找到a标签 包含 名字 以及 id
            sibling_ele = child.previous_sibling

            # 获取年报 名字
            annual_report_name = sibling_ele.text

            # 通过正则获取id
            id_pattern = r'&id=(\d+)'  # id后多个数字，括号表示捕获组
            id_match = re.search(id_pattern, sibling_ele['href'])
            if id_match:
                annual_report_id = id_match.group(1)  # 提取括号中的内容

            #处理时间信息

            # 时间信息在这个节点的前面
            date_raw = sibling_ele.previous_sibling.text

            # 通过正则提取想要的yyyy-mm-dd的形式
            date_pattern = r'\d{4}-\d{2}-\d{2}'  # 定义正则
            date_match = re.search(date_pattern, date_raw)  # 寻找符合的字符串
            if date_match:
                annual_report_date = date_match.group()

            annual_reports.append({
                'name': annual_report_name,
                'id': annual_report_id,
                'date': annual_report_date
            })

    # 三、正式下载文件
    for report_info in annual_reports:
        date = report_info['date']
        ids = report_info['id']
        year = date[:4]
        month = int(date[5:7])
        params = f'{year}/{year}-{month}/{date}/{ids}.PDF'
        download_url = download_base_url + params
        download_file(download_url, directory, report_info['name'])


# # 使用

user_input_stockid = input("请输入一些内容: ")
directory = '/Users/kingwayliu/PycharmProjects/pythonProject/outputfile'
download_annual_reports(user_input_stockid ,directory)




