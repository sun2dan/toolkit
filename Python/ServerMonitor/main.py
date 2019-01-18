#!/usr/bin/env python
# coding=utf-8
import httplib, sys, time
from sendEmail import sendEmail

# python2
reload(sys)
sys.setdefaultencoding('utf8')


def get_nowtime():
    date_str = time.strftime("%m-%d %H:%M:%S", time.localtime())
    return date_str


def main():
    try:
        conn = httplib.HTTPConnection("tools.jr.jd.com", 80, True, 2.0)
        conn.request("HEAD", "/js/lib/clipboard.min.js")
        # conn.sock.settimeout(2.0)
        res = conn.getresponse()

        status = res.status
        conn.close()
        if status == 200:
            print get_nowtime(), 200, res.reason
        else:
            print get_nowtime(), res.status, res.reason, res.getheaders()
            sendEmail(res.status, res.reason, res.getheaders())
            quit()
    except Exception as e:
        if str(e) == 'timed out':
            print get_nowtime(), 'time out'
        else:
            print get_nowtime(), 'catch other error', e


if __name__ == "__main__":
    # windows 隐藏 console
    # whnd = ctypes.windll.kernel32.GetConsoleWindow()
    # if whnd != 0:
    #     ctypes.windll.user32.ShowWindow(whnd, 0)
    #     ctypes.windll.kernel32.CloseHandle(whnd)
    while True:
        main()
        time.sleep(100)
