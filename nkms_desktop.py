#!/usr/bin/python3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QSystemTrayIcon, QMenu, QAction)
from PyQt5.QtGui import QIcon

class nkms_desktop(QSystemTrayIcon):

    def __int__(self):
        super(nkms_desktop, self).__init__()

        self.setIcon(QIcon.fromTheme("accessories-character-map"))
        m = QMenu("Net Keyboard Mouse Switcher", self)

        exit_action = QAction("Exit", self, triggered=self.exit_app)
        m.addAction(exit_action)


    def exit_app(self):
        exit()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    nkms = nkms_desktop()
    nkms.show()
    sys.exit(app.exec_())