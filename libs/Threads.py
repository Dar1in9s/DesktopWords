import requests
import hashlib
import time
import json
import uuid
from PyQt5.QtCore import QThread, pyqtSignal


class TranslateThread(QThread):
    signal_finish = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.YOUDAO_URL = 'https://openapi.youdao.com/api'
        self.APP_KEY = '09caff2f8edd9fb1'
        self.APP_SECRET = 'sAGZ0EVVHLd1eTIf5kWYz01epheH1owr'
        self.word = None
        self.running_flag = False

    def run(self):
        result = self.translate()
        self.signal_finish.emit(result)

    def translate(self):
        data = {}
        now_time = str(int(time.time()))
        data['from'] = 'en'
        data['to'] = 'zh-CHS'
        data['signType'] = 'v3'
        data['curtime'] = now_time
        salt = str(uuid.uuid1())
        data['appKey'] = self.APP_KEY
        data['q'] = self.word
        data['salt'] = salt
        sign_str = self.APP_KEY + self.truncate(self.word) + salt + now_time + self.APP_SECRET
        data['sign'] = hashlib.sha256(sign_str.encode('utf-8')).hexdigest()
        result = dict()
        try:
            response = requests.post(self.YOUDAO_URL, data=data, timeout=3).content.decode()
            res = json.loads(response)
            if res['errorCode'] == '0':
                result['code'] = 0
                result['isWord'] = res['isWord']
                if res['isWord']:
                    result['phonetic'] = '[{}]'.format(res['basic']['phonetic']),
                    result['explains'] = res['basic']['explains']
                    result['msg'] = '查询成功'
                else:
                    result['msg'] = '单词错误'
            else:
                result['code'] = 1
                result['msg'] = '错误代码：' + res['errorCode']
        except requests.exceptions.RequestException:
            result['code'] = 1
            result['msg'] = '请求失败'
        return result

    @staticmethod
    def truncate(q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


class DownloadThread(QThread):
    def __init__(self, voice_dir):
        super().__init__()
        self.URL = 'http://dict.youdao.com/dictvoice?type=1&audio='
        self.word = None
        self.running_flag = False
        self.voice_dir = voice_dir

    def run(self):
        try:
            response = requests.get(self.URL+self.word, timeout=3)
            if response.status_code == 200:
                with open(self.voice_dir+self.word+'.mp3', 'wb') as f:
                    f.write(response.content)
        except requests.exceptions.RequestException:
            pass
        self.running_flag = False

