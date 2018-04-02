# coding=utf-8
import urllib, json
import re, smtplib, sys, os, time
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# 变量
# http://stock.finance.sina.com.cn/usstock/quotes/{0}.html
# http://hq.sinajs.cn/?_=0.871642249293068&list=gb_jd,gb_baba
_prefixPath = 'http://hq.sinajs.cn/etag.php?_={0}&list={1}'

f = open('./config.json', 'r')
configStr = f.read()
f.close()

configData = json.loads(configStr)
_dict = configData['stockData']


# 获取价格
def getPrice():
    ts = long(time.time() * 1000)
    codeList = []
    for key in _dict:
        codeList.append('gb_{0}'.format(key))

    path = _prefixPath.format(ts, re.sub(r'\s+', '', ",".join(codeList)))

    # var hq_str_gb_jd="京东,46.1300,0.07,2018-01-10 21:41:58,0.0300, # 现价、增率、时间、增幅
    # 46.4900,46.8000,45.7900,48.9900, # 开高低、52周最高
    # 26.4800,12380892,11039714,65440087195,-0.40,--,0.00,0.00,0.00,0.00,1418601500,57.00,45.2400,-1.93,-0.89,Jan 10 08:35AM EST,Jan 09 04:00PM EST,46.1000,114951.00";
    # 结果
    res = {}
    f = urllib.urlopen(path)
    for line in f:
        # print(line)
        arr = line.split(',')
        if (len(arr) > 1):
            matches = re.search('gb_([\w]+)', arr[0])
            res[matches.group(1)] = {
                'cur': formatFloat(arr[1]),
                'rate': formatFloat(float(arr[2])),
                'step': formatFloat(arr[4])
            }
    f.close()
    return res


# 计算实时数据
def countRealTime():
    res = getPrice()
    for code in _dict:
        s_obj = _dict[code]
        num = s_obj['num']
        cost = float(s_obj['cost'])

        obj = res[code]
        cur = obj['cur']

        obj['sum'] = formatFloat(obj['cur'] * num)
        obj['gain'] = formatFloat(obj['step'] * num)
        obj['profitStep'] = formatFloat((cur - cost) * num)
        obj['profitRate'] = formatFloat((cur - cost) / cost * 100)
    return res


# 格式化数字，保留两位小数
def formatFloat(num, keepLen=2):
    return round(float(num), keepLen)


# 发送邮件
def sendEmail():
    mail_host = configData['smtp']  # 设置服务器
    mail_user = configData['user']  # 用户名
    mail_pass = configData['pwd']  # 口令
    mail_port = configData['port']
    receivers = configData['receiver']  # 接收邮箱

    localtime = time.localtime(time.time())
    sender = mail_user

    # 发送的主题
    subject = u'{0}-{1}-{2} 报表'.format(localtime.tm_year, str(localtime.tm_mon).zfill(2),
                                       str(localtime.tm_mday).zfill(2))
    html = getHtml()

    message = MIMEText(html, 'html', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = formataddr([u'股票助手', sender])
    message['To'] = ",".join(receivers)

    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, str(mail_port))  # 25 为 SMTP 端口号  outlook端口587  网易是25

    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())

    print u"邮件发送成功"
    smtpObj.quit()


# 根据数据生成html
def getHtml():
    colors = {'red': '#DD636F', 'green': '#74C573'}
    wrapper = '''
        <body style="padding:0; margin:0;background:#1D2024;">
            <div style="margin:0;padding:20px 0;background:#1D2024;">
                <table cellpadding="1" cellspacing="1" style="width:100%;font-size:14px;border:none; text-align:center;color:#fff;background-color:#1D2024;">
                    <tr>
                        <td style="height:36px; line-height:36px;background:#24282B;">代码</td>
                        <td style="background:#24282B;">最新价/成本价</td>
                        <td style="background:#24282B;">盈亏</td>
                        <td style="font-weight:normal;background:#24282B;">持仓</td>
                    </tr>
                    {forstr}
                    <tr>
                        <td style="background:#24282B; padding:10px 0;line-height:1.5; font-size:0;" colspan="4">
                            <p style="font-size:16px; margin:0; width:50%; display:inline-block;">当日盈亏:&nbsp;<span
                                    style="margin:0;color:{curColor};">{curSymbol}${curStep}
                                </span>
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td style="background:#24282B; padding:10px 0;line-height:1.5; font-size:0;" colspan="4">
                            <p style="font-size:16px; margin:0; width:50%; display:inline-block;">总盈亏:&nbsp;<span
                                    style="margin:0;color:{color};">{symbol}${step}&nbsp;({rate}%)</span></p>
                            <p style="font-size:16px; margin:0; width:50%; display:inline-block;">
                                总持仓:&nbsp;${sum}</p>
                        </td>
                    </tr>
                </table>
            </div>
        </body>
        '''

    forstr = '''
            <tr>
                <td style="background:#24282B;line-height:36px; height:36px;">{code}</td>
                <td style="background:#24282B;">
                    <p style="margin:0;">${cur}</p>
                    <p style="margin:0;">${cost}</p>
                </td>
                <td style="background:#24282B; padding:10px 0;line-height:1.5;">
                    <p style="margin:0;color:{color};">{symbol}${gain}</p>
                    <p style="margin:0;color:{color};">{symbol}{step}({symbol}{rate}%)</p>
                    <p style="margin:0;color:{profitColor};">{profitSymbol}${profitStep}&nbsp;({profitSymbol}{profitRate}%)</p>
                </td>
                <td style="background:#24282B;">
                    <p style="margin:0;">{num}</p>
                    <p style="margin:0;">${sum}</p>
                </td>
            </tr>
        '''

    res = countRealTime()

    strArr = []

    total = {'sum': 0, 'rate': 0, 'step': 0, 'symbol': '', 'color': colors['green'], 'curSymbol': '',
             'curColor': colors['green'], 'curStep': 0, 'curRate': 0}
    for code in res:
        data = res[code]
        data['code'] = code.upper()
        data['color'] = colors['red']
        data['symbol'] = '-'
        data['profitSymbol'] = '-'
        data['profitColor'] = colors['red']
        dicobj = _dict[code]
        data['cost'] = dicobj['cost']
        data['num'] = dicobj['num']

        total['sum'] += data['sum']
        total['step'] += data['profitStep']
        total['curStep'] += data['gain']

        if data['rate'] >= 0:
            data['color'] = colors['green']
            data['symbol'] = ''

        if data['profitRate'] >= 0:
            data['profitColor'] = colors['green']
            data['profitSymbol'] = ''

        data['gain'] = abs(data['gain'])
        data['rate'] = abs(data['rate'])
        data['step'] = abs(data['step'])
        data['profitRate'] = abs(data['profitRate'])
        data['profitStep'] = abs(data['profitStep'])

        strArr.append(forstr.format(**data))

    total['forstr'] = ''.join(strArr)

    orig = 0
    for code in _dict:
        s_obj = _dict[code]
        num = s_obj['num']
        cost = float(s_obj['cost'])
        orig += cost * num

    total['rate'] = formatFloat(total['step'] / orig * 100)
    total['curRate'] = formatFloat(total['curStep'] / total['sum'])

    if total['step'] < 0:
        total['color'] = colors['red']
        total['symbol'] = '-'

    if total['curStep'] < 0:
        total['curStep'] = abs(total['curStep'])
        total['curColor'] = colors['red']
        total['curSymbol'] = '-'

    resstr = wrapper.format(**total)

    return resstr


# 获取脚本文件的当前路径
def getCurPath():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def main():
    while True:
        localtime = time.localtime(time.time())
        # 5:00 am 已经收盘，可以发送邮件了
        if localtime.tm_hour == 5 and localtime.tm_min > 0:
            sendEmail()
            break
        else:
            time.sleep(10) #10s 打印一次数据

        print(time.localtime(time.time()))
        print(countRealTime())


if __name__ == "__main__":
    main()


'''   config.json 结构：
{
  "smtp": "smtp.163.com",  #smtp服务器(163服务器地址：smtp.163.com)
  "port": "25", #smtp 端口号(outlook端口587，163是25)
  "user": "xxx@163.com",
  "pwd": "xxxxxx",
  "receiver": ["receiver@163.com"],  # 接收者邮箱
  "stockData": {   # 配置持仓数据
    "jd": {           # 持仓code
      "cost": 40.06,  # 成本价
      "num": 78       # 持仓股数
    },
    "baba": {
      "cost": 178,
      "num": 25
    }
  }
}
'''