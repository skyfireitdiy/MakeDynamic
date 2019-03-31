from PyQt5.QtWidgets import QMainWindow, QApplication, QDirModel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

from ui_mainwindow import Ui_MainWindow

import sys


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._dir_model = QDirModel(self)

        self._ui.project_tree.setModel(self._dir_model)

    def _on_load_url(self, url: str):
        self._browser.load(QUrl(url))

    def _on_backward(self):
        self._browser.back()

    def _on_forward(self):
        self._browser.forward()

    def _on_refresh(self):
        self._browser.reload()

    def load_project(self, project_config: dict):
        """
        加载项目文件
        :param project_config:项目文件
        :return: 是否加载成功，错误信息
        """
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
