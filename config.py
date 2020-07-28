from PyQt5.QtGui import QColor

# 单词文件位置
word_file = './resources/words/wordlist.txt'

# 单词音频保存目录
voice_dir = './resources/words/voice/'

# 单词音频文件最大保存数量
max_voice_file_num = 10

# 单词自动更新频率（分钟）
update_interval = 2

# 鼠标没有放上去时的背景颜色，前三个是rgb值，最后一个是透明度
bg_color_leave = QColor(80, 147, 166, 25)

# 其余参数可以在./resources/style.qss中修改
