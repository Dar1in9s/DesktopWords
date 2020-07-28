# DesctopWords
桌面单词悬浮窗，对着桌面发呆的同时又可以多背几个单词了 2333

## 使用
**安装环境**
`pip install -r requirements.txt`

**配置有道翻译API**
1. 进入[https://ai.youdao.com/appmgr.s](https://ai.youdao.com/appmgr.s)，注册账号，创建翻译服务，获取应用ID和应用密钥

2. 编辑`config.py`中的`APP_KEY`和`APP_SRCRET`

**启动**

使用vbs脚本启动：
1. 更改`DesctopWords.bat`文件中的`pythonw.exe`路径
2. 双击`DesctopWords.bat`启动
    Ps：可将`DesctopWords.bat`加入系统启动项，实现开机自启（推荐）

使用python命令行启动：
`python main.py`或`pythonw main.py`(后台运行)


## 自定义颜色搭配
- 更改`config.py`
- 更改`resources/style.qss`


默认颜色搭配是以我的桌面为基础的，可以根据自己的桌面进行修改。
附上是我的电脑下的程序截图：

![](https://blog-1300147235.cos.ap-chengdu.myqcloud.com/20200728204553.png)

