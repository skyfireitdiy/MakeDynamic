from ui_create_project import Ui_CreateProject
from PyQt5.QtWidgets import QDialog


class CreateProjectDlg(QDialog):
    def __init__(self, parent=None):
        super(CreateProjectDlg, self).__init__(parent)
        self._ui = Ui_CreateProject()
        self._ui.setupUi(self)
