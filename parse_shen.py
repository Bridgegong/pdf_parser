# -*- coding: utf-8 -*-
# @Time    : 2018/5/29 10:38
# @Author  : Bridge
# @Email   : 13722450120@163.com
# @File    : parse_shen.py
# @Software: PyCharm
import KBoxBrConfig
import KBoxBrUtils
import requests
from bs4 import BeautifulSoup
import os
from  shenjiaosuo import pdf

def parse_url(url):
    data = {'leftid': 1,
            'lmid': 'drgg',
            'pageNo': 1,
            'startTime': '2018-04-01',
            'endTime': '2018-04-30',
            }
    # r = KBoxBrUtils.request('standard-post',{'url':url,'charset':'GBK'}, data = data)

    r = build_requests(url, data=data)
    bea = BeautifulSoup(r.text, 'lxml')
    page = bea.find('td', 'page12').find_all('td')[1].find_all('span')[1].text
    return page


def get_html(url, page):
    for i in range(1, int(page)+1):
        print('第%d页' % i)
        data = {'leftid': 1,
                'lmid': 'drgg',
                'pageNo': '{}'.format(i),
                'startTime': '2018-04-01',
                'endTime': '2018-04-30',
                }
        r = build_requests(url, data=data)
        get_pdf_link(r.text)


def get_pdf_link(link):
    soup = BeautifulSoup(link, 'lxml')
    url = soup.find_all('td', 'td2')
    for p in url:
        urls = 'http://disclosure.szse.cn/' + p.a['href']
        pdf_url = requests.get(urls,timeout=16).content
        name = p.a.text.replace('*', '')
        time = p.find('span', 'link1').text
        size = p.find('font').text.replace('(', '').replace(')', '').replace('k', '')
        print(size)
        if int(size) < 1000:
            names = name + time
            # print(names)
            print(size)
            path = os.path.join('D:\PDF_530\\')
            if not os.path.exists(path):
                os.mkdir(path)
            try:
                with open(path + '%s' % names + '.pdf', 'wb') as f:
                    f.write(pdf_url)
                pdf.get_name(urls, name, time, names)
            except Exception as e:
                with open('D:\ZhiYin_zhihui\shenjiaosuo.text', 'a+', encoding='utf-8') as f:
                    f.write('%s,%s' %(e, names) + '\n')


def build_requests(url, **kwargs):
    if kwargs.get('data'):
        res = requests.post(url, **kwargs, timeout=20)
        res.encoding = res.apparent_encoding
        return res
    else:
        res = requests.get(url, **kwargs, timeout=20)
        res.encoding = res.apparent_encoding
        return res


def main():
    url = 'http://disclosure.szse.cn/m/search0425.jsp'
    page = parse_url(url)
    html = get_html(url, page)
    get_pdf_link(html)

main()