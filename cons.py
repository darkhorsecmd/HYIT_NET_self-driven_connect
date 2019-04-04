import requests
import time
import re
import configparser
import subprocess

class login(object):
    cf  = configparser.ConfigParser()
    cf.read("config.ini")



    user = cf.get("config","user")
    pwd = cf.get("config","pwd")
    every = int(cf.get("config","every"))

    def __init__(self):
        self.login_url = "http://172.16.5.73/portal/login.php"
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '55',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': '172.16.5.73',
            'Origin': 'http://172.16.5.73',
            'Referer': 'http://172.16.5.73/webAuth/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.payload = {
            "opr": "pwdLogin",
            "userName": login.user,
            "pwd": login.pwd,
            "rememberPwd": "0"
        }
        self.every = login.every  # 检测间隔时间，单位为妙

    def login(self):
        try:
            requests.post(self.login_url, headers=self.headers, data=self.payload)
            if self.canConnect() is False:
                print("连接失败，请检查网络环境或账号密码")
            else:
                print(self.getCurrentTime(),u"网络连接成功")
        except Exception as e:
            print("some errors")
            print(str(e))

    def canConnect(self):
        try:
            q = requests.get("http://www.baidu.com", timeout=5)
            m = re.search(r'STATUS OK', q.text)
            if m:
                return True
            else:
                return False
        except Exception as conE:
            return False

    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    def main(self):
        print(self.getCurrentTime(), u"Hi，欢迎使用自动登陆系统")
        while True:
            self.login()
            while True:
                can_connect = self.canConnect()
                if not can_connect:
                    print(self.getCurrentTime(), u"断网了...")
                    self.login()
                else:
                    print(self.getCurrentTime(), u"一切正常...")
                time.sleep(self.every)
            time.sleep(self.every)

if __name__ == '__main__':
    logins = login()
    logins.main()
