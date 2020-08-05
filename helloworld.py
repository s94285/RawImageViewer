from PyQt5 import QtWidgets
from UI import Ui_MainWindow
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QByteArray,QFile
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label.setText('Hello World!')
        self.ui.pushButton.clicked.connect(self.showImage)

        self.W = 1920
        self.H = 1080
        self.IMAGESIZE = self.W*self.H*8
        self.pic = None
        
    def showImage(self, mainWindow):
        "Show image on graphics view"
        print("AAA")
        # self.ui.imageLabel
        # picArray =
        picFile = QFile("images/2K_good_0804_1_12.raw")
        if(not picFile.open(QFile.ReadOnly)):return
        self.pic = QImage(picFile.read(self.IMAGESIZE),self.W,self.H,QImage.Format_Grayscale8)
        self.ui.imageLabel.setPixmap(QPixmap.fromImage(self.pic))

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())