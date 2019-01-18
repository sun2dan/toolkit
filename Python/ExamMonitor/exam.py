#!/usr/bin/env python
# coding=utf-8

import re, sys, time
# import urllib.request
# import urllib, urllib2
import requests
import codecs
from sendEmail import sendEmail

reload(sys)
sys.setdefaultencoding('utf8')

def main():
    url = 'http://bm.ruankao.org.cn/sign/welcome'
    # python3
    # page = urllib.request.urlopen(url)
    # html = page.read().decode('utf-8')
    # page.close()

    # python2 urllib2
    # req = urllib2.Request(url)
    # res = urllib2.urlopen(req)
    # code = res.code
    # html = res.read()
    # res.close()

    # python2 request
    res = requests.get(url, {})
    code = res.status_code
    html = res.content
    if code != 200:
        return

    list = get_list(html)

    # 循环查看是否有2019年的数据
    is_in_2019 = False
    for item in list:
        if re.match(r'2019', item[1]) is not None:
            is_in_2019 = True
            break
    if is_in_2019:
        print u'开始报名'
        cont = get_mail_cont(list)
        # save_file(str, './temp/test.html')
        sendEmail(cont)
        quit()
    else:
        print get_nowtime(), u'未开始'

def get_nowtime():
    date_str = time.strftime("%m-%d %H:%M:%S", time.localtime())
    return date_str


# 保存格式化好的文件
def save_file(res, path):
    with codecs.open(path, 'w+', 'utf-8') as out:
        out.write(res)


def get_mail_cont(list):
    str = '<meta charset="utf-8"><h1>软考开始报名啦</h1><div>'
    for item in list:
        str += '''<div style="line-height:24px;">
            <span style="display:inline-block; width:80px; margin-right:12px; text-align: right;">{0}:</span>
            <span style="display:inline-block;">{1}</span>
        </div>'''.format(item[0], re.sub(r'\~', '&nbsp;&nbsp;-&nbsp;&nbsp;', item[1]))
    str += '</div>'
    # print str
    return str


def get_list(html):
    html = html.decode('utf-8')
    # pattern = re.compile(u'col1">([\u4E00-\u9FFF]+)</div>\s{0,}<div[\wA-Z\s\d\"=-]+>([\d\w\-\~]+)<',re.I | re.M | re.L)
    # groups = pattern.findall(html)

    groups = re.findall(u'col1">([\u4E00-\u9FFF]+)</div>\s{0,}<div[\wA-Z\s\d\"=-]+>([\d\w\-\~]+)<', html)

    if len(groups) == 0:
        print '空'
        return None
    # for g in groups:
    #     print(g)
    return groups


if __name__ == "__main__":
    while True:
        main()
        time.sleep(60 * 60 * 6)
