# coding=utf-8
import urllib, json
import re, smtplib, sys, os, time
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

f = open('./config.json', 'r')
configStr = f.read()
f.close()

configData = json.loads(configStr)


# 发送邮件
def sendEmail(html):
    mail_host = configData['smtp']  # 设置服务器
    mail_user = configData['user']  # 用户名
    mail_pass = configData['pwd']  # 口令
    mail_port = configData['port']
    receivers = configData['receiver']  # 接收邮箱

    localtime = time.localtime(time.time())
    sender = mail_user

    # 发送的主题
    subject = u'[提醒] 软考报名'.format(localtime.tm_year, str(localtime.tm_mon).zfill(2),
                                  str(localtime.tm_mday).zfill(2))

    message = MIMEText(html, 'html', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = formataddr([u'软考报名', sender])
    message['To'] = ",".join(receivers)

    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, str(mail_port))  # 25 为 SMTP 端口号  outlook端口587  网易是25

    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())

    print u"邮件发送成功"
    smtpObj.quit()
