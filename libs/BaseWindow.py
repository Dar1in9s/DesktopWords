from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QAction, QMenu, qApp, QDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from libs.window_ui import Ui_window
import sys


class BaseWindow(QWidget, Ui_window):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setupUi(self)
        self.bg_widget = QWidget(self)
        self.tray = QSystemTrayIcon()

    def base_init(self):
        self.setWindowIcon(QIcon(self.icon_file))
        self.init_bg_widget()
        self.tray_init()

    def tray_init(self):
        self.tray.setIcon(QIcon(self.icon_file))
        self.tray.setVisible(True)
        about_action = QAction("&About", self, triggered=self.about)
        show_action = QAction("&显示页面", self, triggered=self.show)
        quit_action = QAction("&退出", self, triggered=qApp.quit)
        tray_menu = QMenu(self)
        tray_menu.addAction(about_action)
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        self.tray.setContextMenu(tray_menu)
        self.tray.activated.connect(self.act)

    def act(self, reason):
        if reason == 2 or reason == 3:
            self.show()

    def about(self):
        dialog_about = QDialog()
        dialog_about.setWindowFlags(Qt.WindowCloseButtonHint)
        dialog_about.setWindowModality(Qt.NonModal)
        dialog_about.setWindowTitle('About')
        dialog_about.setWindowIcon(QIcon(self.icon_file))
        l1, l2, l3 = (QLabel() for i in range(3))

        l1.setText(str("Version: 1.0"))
        l2.setText(str('Author: <a href="https://dar1in9s.github.io/">Dar1in9</a>'))
        l3.setText(str('Github: <a href="https://github.com/Dar1in9s/DesctopWords">https://github.com/Dar1in9s/DesctopWords</a>'))
        l2.setOpenExternalLinks(True)
        l3.setOpenExternalLinks(True)
        vbox = QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addWidget(l2)
        vbox.addWidget(l3)
        dialog_about.setLayout(vbox)

        dialog_about.exec_()

    def init_bg_widget(self):
        self.bg_widget.setObjectName('bg_widget')
        self.bg_widget.setGeometry(0, 0, 520, 420)
        self.bg_widget.lower()
        self.bg_widget.setVisible(False)

        x = QApplication.desktop().width() - self.width()
        y = int(QApplication.desktop().height() / 2 - self.height() / 4)
        self.move(x, y)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.move_flag = True
            self.start_pos = (event.globalX(), event.globalY())
            self.click_window_pos = (event.pos().x(), event.pos().y())
        else:
            self.move_flag = False

    def mouseMoveEvent(self, event):
        if self.move_flag and self.start_pos:
            now_click_pos = (event.globalX(), event.globalY())
            change_width = now_click_pos[0] - self.start_pos[0]
            change_height = now_click_pos[1] - self.start_pos[1]
            self.move(self.x() + change_width, self.y() + change_height)
            self.start_pos = now_click_pos

    def mouseReleaseEvent(self, event):
        self.start_pos = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BaseWindow()
    window.show()
    QApplication.processEvents()
    sys.exit(app.exec_())
