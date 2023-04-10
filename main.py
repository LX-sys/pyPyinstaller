import sys
from PyQt5.QtWidgets import QApplication
from libGui.startInterface import StartInterface


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = StartInterface()
    win.show()

    sys.exit(app.exec_())
