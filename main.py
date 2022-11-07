
import sys
from PyQt5.QtWidgets import QApplication
from libGui.pyPyinstaller import PyPyinstaller


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = PyPyinstaller()
    win.show()

    sys.exit(app.exec_())
