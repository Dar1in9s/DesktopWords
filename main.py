from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor, QPainter, QTextCursor
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from libs.BaseWindow import BaseWindow
from libs.Threads import TranslateThread, DownloadThread
import config
import sys
import random
import os


class Window(BaseWindow):
    def __init__(self):
        super().__init__()
        # 变量定义
        self.word_file = config.word_file
        self.voice_dir = config.voice_dir
        self.icon_file = './resources/images/logo.png'
        self.max_voice_file_num = config.max_voice_file_num
        self.update_interval = config.update_interval * 60 * 1000
        self.bg_color_leave = config.bg_color_leave
        # 初始化
        self.base_init()

        # 实例化线程和定时器
        self.translator = TranslateThread()
        self.downloader = DownloadThread(self.voice_dir)
        self.timer = QTimer(self)
        # 连接信号
        self.btn_close.clicked.connect(self.close)
        self.timer.timeout.connect(self.next_word)
        self.translator.signal_finish.connect(self.update_word_info)

        self.timer.start(self.update_interval)
        self.next_word()

    # 读单词（发音）
    def read_word(self):
        word = self.btn_word.text().strip()
        if os.path.exists(self.voice_dir+word+'.mp3'):
            player = QMediaPlayer(self)
            media_content = QMediaContent(QUrl.fromLocalFile(self.voice_dir+word+'.mp3'))
            player.setMedia(media_content)
            player.setVolume(100)
            player.play()
        else:
            self.download_voice()

    # 刷新
    def refresh_word(self):
        if not self.translator.running_flag:
            self.translator.running_flag = True
            word = self.btn_word.text().strip()
            self.textEdit_explant.setText('获取中...')
            self.translator.word = word
            self.translator.start()
            self.download_voice()

    # 下一个单词
    def next_word(self):
        if not self.translator.running_flag:
            self.translator.running_flag = True
            with open(self.word_file, 'r') as f:
                words = f.readlines()
            word = random.choice(words).strip()
            self.btn_word.setText(word)
            self.textEdit_explant.setText('获取中...')
            self.word_adjust_size()
            self.translator.word = word
            self.translator.start()
            self.download_voice()

            self.timer.stop()
            self.timer.setInterval(self.update_interval)
            self.timer.start()

    # 下载发音
    def download_voice(self):
        word = self.btn_word.text().strip()
        if not self.downloader.running_flag and not os.path.exists(self.voice_dir+word+'.mp3'):
            dir_list = os.listdir(self.voice_dir)
            if dir_list:
                dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(self.voice_dir, x)))
            if len(dir_list) > 10:
                os.remove(self.voice_dir + dir_list[0])

            self.downloader.word = word
            self.downloader.start()

    # 更新单词信息
    def update_word_info(self, word_info):
        if word_info['code'] == 0 and word_info['isWord']:
            self.label_phonetic.setText(word_info['phonetic'][0])
            self.textEdit_explant.setText('')
            for i in word_info['explains']:
                self.textEdit_explant.append(i)
        else:
            self.label_phonetic.setText('')
            self.textEdit_explant.setText(word_info['msg'])
            self.textEdit_explant.moveCursor(QTextCursor.Start)
        self.translator.running_flag = False

    # 单词按钮大小调整
    def word_adjust_size(self):
        self.btn_word.adjustSize()
        width = self.btn_word.width()
        x = (self.width() - width) / 2 if self.width() > width else 0
        y = 30
        self.btn_word.move(x, y)

    def enterEvent(self, event):
        self.bg_widget.setVisible(True)

    def leaveEvent(self, event):
        self.bg_widget.setVisible(False)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.bg_color_leave)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setQuitOnLastWindowClosed(False)
    app.setStyleSheet(open('./resources/style.qss', 'r', encoding='utf8').read())
    window = Window()
    window.show()
    sys.exit(app.exec_())
