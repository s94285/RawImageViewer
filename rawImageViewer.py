from PyQt5 import QtWidgets
from Ui_mainWindow import Ui_MainWindow
from PyQt5.QtGui import QImage,QPixmap,QStandardItemModel,QKeySequence
from PyQt5.QtCore import QByteArray,QFile
from PyQt5.QtCore import Qt,QDir,QItemSelectionModel,QModelIndex
import sys,os
from send2trash import send2trash

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.W = 1920
        self.H = 1080
        self.IMAGESIZE = self.W*self.H*8
        self.pic = None
        self.picPath = None
        self.pixmap = None
        self.dirModel = QtWidgets.QFileSystemModel(self)
        self.fileModel = QtWidgets.QFileSystemModel(self)
        self.isInterlacing = False

        self.ui.actionOpen_Folder.triggered.connect(self.openDirDialog)
        self.ui.treeView.clicked.connect(self.treeViewClicked)
        self.ui.listView.doubleClicked.connect(self.listViewDoubleClicked)

        self.dirModel.setFilter(QDir.NoDotAndDotDot|QDir.AllDirs)
        self.ui.treeView.setModel(self.dirModel)
        for i in range(1,self.dirModel.columnCount()):
            self.ui.treeView.hideColumn(i)
        self.fileModel.setNameFilters(["*.raw"])
        self.fileModel.setFilter(self.fileModel.filter()&~QDir.Dirs)
        self.ui.listView.setModel(self.fileModel)
        self.ui.listView.selectionModel().currentChanged.connect(self.listViewMoved)
        # use myComputer as first directory
        self.ui.treeView.setRootIndex(self.dirModel.setRootPath(self.dirModel.myComputer()))
        self.ui.listView.setRootIndex(self.fileModel.setRootPath(self.fileModel.myComputer()))

        self.checkbox = QtWidgets.QCheckBox()
        self.checkbox.setText("1080i        ")
        self.ui.statusbar.addPermanentWidget(self.checkbox)
        self.checkbox.stateChanged.connect(self.checkboxClicked)
        # override imageLabel resizeEvent to update pixmap
        self.ui.imageLabel.resizeEvent = self.imageLabelResizeEvent
        # add delete function
        self.deleteShortcut = QtWidgets.QShortcut(QKeySequence.Delete,self)
        self.deleteShortcut.activated.connect(self.deleteEvent)
        # add gotoButton
        self.ui.gotoButton.clicked.connect(self.gotoClicked)

    def openDirDialog(self,MainWindow):
        "Open folder selecting dialog"
        dialog = QtWidgets.QFileDialog(self)
        path = dialog.getExistingDirectory(None)
        self.openDir(path)

    def openDir(self,path):
        "Open directory on treeview"
        self.ui.addressLineEdit.setText(path)
        self.ui.treeView.setCurrentIndex(self.dirModel.index(path))
        self.fileModel.setRootPath(path)
        self.ui.listView.setRootIndex(self.fileModel.index(path))

    def gotoClicked(self):
        "Triggered by gotoButton and addressLineEdit return pressed signal"
        path = self.ui.addressLineEdit.text()
        if(os.path.isdir(path)):
            self.openDir(path)

    def checkboxClicked(self,state):
        self.isInterlacing = (state==Qt.Checked)
        self.updateImage()

    def treeViewClicked(self,index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        self.ui.addressLineEdit.setText(path)
        self.ui.listView.setRootIndex(self.fileModel.index(path))

    def listViewMoved(self,index):
        path = self.fileModel.fileInfo(index).absoluteFilePath()
        self.showImage(path)

    def listViewDoubleClicked(self,index):
        # TODO: implement double click features on folders
        if(not self.ui.listView.selectionModel()): # Not created yet
            return
        path = self.fileModel.fileInfo(index).absoluteFilePath()
        if(os.path.isdir(path)):
            # self.dirModel.
            pass
            

    def showImage(self, path):
        "Show image on graphics view"
        self.picPath = path
        self.setWindowTitle(os.path.basename(path)+" [Raw Image Viewer]")
        self.updateImage()
        
    def updateImage(self):
        if(self.picPath):
            self.ui.statusbar.showMessage(self.picPath)
            picFile = QFile(self.picPath)
            if(not picFile.open(QFile.ReadOnly)):
                return
            if(self.isInterlacing):
                self.pic = QImage(picFile.read(self.IMAGESIZE//2),self.W,self.H//2,QImage.Format_Grayscale8)
            else:
                self.pic = QImage(picFile.read(self.IMAGESIZE),self.W,self.H,QImage.Format_Grayscale8)
            self.pixmap = QPixmap.fromImage(self.pic)
            self.ui.imageLabel.setPixmap(self.pixmap.scaled(self.ui.imageLabel.width(),self.ui.imageLabel.height(),Qt.KeepAspectRatio))
        
    def imageLabelResizeEvent(self,event):
        "Override the resize event"
        #resize image label
        self.updateImage()

    def deleteEvent(self):
        "Create Message Box for confirmation and delete selected items"
        if(not self.ui.listView.selectionModel()): # Not created yet
            return
        selectedIndexes = self.ui.listView.selectionModel().selectedIndexes()
        if(len(selectedIndexes)==0):return
        if(len(selectedIndexes)==1):
            # Only 1 selection, no confirming
            path = self.fileModel.fileInfo(selectedIndexes[0]).absoluteFilePath()
            print("Delete to Trash: " + path)
            send2trash(path)
        else:
            # Multiselection, need confirmation
            messageBox = QtWidgets.QMessageBox(self)
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Yes)
            messageBox.addButton(QtWidgets.QMessageBox.No)
            messageBox.setDefaultButton(QtWidgets.QMessageBox.No)
            messageBox.setWindowTitle("Delete")
            messageBox.setText(" Delete {:d} items\n\n Confirm?".format(len(selectedIndexes)))
            if(messageBox.exec()==QtWidgets.QMessageBox.Yes):
                print("Deleting")
                for index in selectedIndexes:
                    path = self.fileModel.fileInfo(index).absoluteFilePath()
                    print("Delete to Trash: " + path)
                    send2trash(path)
            else:
                print("Do nothing")


    def test(self,MainWindow):
        print(self.ui.listView.selectionModel())

        
        
        

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())