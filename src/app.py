import sys
from PyQt5 import QtWidgets
from src.views.main_layout import App

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.setWindowTitle("Plant Disease Prediction")
    window.show()
    sys.exit(app.exec_())
