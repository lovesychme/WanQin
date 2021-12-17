# _*_ coding:utf-8 _*_
import os
import re
import sys

from PyQt5 import QtWidgets ,QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from optyUnsecuredRevenue import OUR
from config import *
from crm_ui import Ui_MainWindow

class Wind(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Wind, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Ncs Auto Tool')
        self.setMinimumSize(self.size())
        self.setMaximumSize(self.size())
        #variants
        self.fileChecks=[]
        self.worker=None


        #set place holder
        self.source_edit.setPlaceholderText('Source Directory')
        self.out_edit.setPlaceholderText('Output Directory')

        #set signal
        self.source_select.clicked.connect(self.selectSourceDir)
        self.source_open.clicked.connect(self.openSourceDir)
        self.out_select.clicked.connect(self.selectOutputDir)
        self.out_open.clicked.connect(self.openOutDir)
        self.save_btn.clicked.connect(self.saveConfig)
        self.source_edit.textChanged.connect(self.updateList)

        self.run_btn.clicked.connect(self.runProcess)
        self.cancel_btn.clicked.connect(self.close)

        #ReadConfig
        self.config = Config('ncs_config.yml')
        c=self.config
        if os.path.exists(c.get('sourceDir')):
            self.sourceDir=c.get('sourceDir')
        if os.path.exists(c.get('outDir')):
            self.outDir=c.get('outDir')

        #get ready
        self.status='Ready'
        self.show()

    def selectSourceDir(self):
        originalPath = self.sourceDir
        if originalPath and os.path.exists(originalPath):
            x = QFileDialog.getExistingDirectory(self, 'Select Source Directory', originalPath).replace('/','\\')
        else:
            x = QFileDialog.getExistingDirectory(self, 'Select Source Directory').replace('/','\\')
        if os.path.exists(x):
            self.sourceDir=x

        if originalPath != x:
            self.status='Source Directory Updated'
    def openSourceDir(self):
        if os.path.exists(self.sourceDir):
            os.startfile(self.sourceDir)
    def selectOutputDir(self):
        originalPath = self.sourceDir
        if originalPath and os.path.exists(originalPath):
            x = QFileDialog.getExistingDirectory(self, 'Select Output Directory', originalPath).replace('/', '\\')
        else:
            x = QFileDialog.getExistingDirectory(self, 'Select Output Directory').replace('/', '\\')
        if os.path.exists(x):
            self.outDir = x

        if originalPath != x:
            self.status = 'Output Directory Updated'
    def openOutDir(self):
        if os.path.exists(self.outDir):
            os.startfile(self.outDir)
    def updateList(self):
        if not os.path.exists(self.sourceDir):
            self.status=f'Source directory not exist.'
            return
        tw:QTableWidget=self.tableWidget
        tw.clear()
        tw.setColumnCount(1)
        tw.verticalHeader().setVisible(False)
        tw.horizontalHeader().setVisible(False)
        tw.horizontalHeader().setStretchLastSection(True)
        tw.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        tw.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tw.setSelectionMode(QAbstractItemView.NoSelection)

        files,select=self.getDirFiles(self.sourceDir)

        self.fileChecks=[]

        if files:
            tw.setRowCount(len(files))
            i=0
            for f in files:
                b = QCheckBox(f)
                if f==select:
                    b.setChecked(True)
                tw.setCellWidget(i,0,b)
                self.fileChecks.append(b)
                i+=1
        else:
            tw.setRowCount(0)
        tw.resizeRowsToContents()

    def getDirFiles(self,dir):
        if not os.path.isdir(dir):
            return None,None
        if dir.endswith("\\"):
            dir=dir[0:-1]
        files=[x.lower() for x in os.listdir(dir)]
        li=[]
        select=None
        visitTime=0
        for f in files:
            if re.search(r'^[^~]+.xls[a-z]?$',f):
                li.append(f)
                vt=os.path.getatime(f"{dir}\\{f}")
                if visitTime<vt:
                    visitTime=vt
                    select=f
        return li,select
    def saveConfig(self):
        c=self.config
        c.set('sourceDir',self.sourceDir)
        c.set('outDir',self.outDir)
        c.save()
        self.status='Config saved.'

    def runProcess(self):
        if self.worker:
            QMessageBox.warning(self,'warning','Task under processing')
            return
        if not os.path.exists(self.sourceDir):
            self.status = 'source directory not exist.'
            return
        sourceFiles = self.selectedSourceFiles
        if not sourceFiles:
            self.status='no source files selected.'
            return
        if not os.path.exists(self.outDir):
            self.status='output directory not exist.'
            return
        self.saveConfig()
        self.status='start process.'

        worker=Worker()
        worker.sources=[f'{self.sourceDir}\\{f}' for f in self.selectedSourceFiles]
        worker.outDir=self.outDir
        worker.msgSin.connect(self.setStatus)
        worker.endSin.connect(self.endProcess)
        worker.start()
        self.worker=worker

    def endProcess(self,b):
        if b:
            self.worker=None
            self.openOutDir()

    @property
    def sourceDir(self):
        return self.source_edit.text()
    @sourceDir.setter
    def sourceDir(self,s):
        self.source_edit.setText(s)

    @property
    def outDir(self):
        return self.out_edit.text()
    @outDir.setter
    def outDir(self, s):
        self.out_edit.setText(s)

    @property
    def status(self):
        return self.statusbar.currentMessage()
    @status.setter
    def status(self,msg):
        self.statusbar.showMessage(msg)

    def setStatus(self,s):
        self.status=s

    @property
    def selectedSourceFiles(self):
        li=[]
        b:QCheckBox
        for b in self.fileChecks:
            if b.isChecked():
                li.append(b.text())
        return li

class Worker(QThread):
    msgSin = pyqtSignal(str)
    endSin =pyqtSignal(list)
    def __init__(self,parent=None):
        super(Worker, self).__init__(parent)
        self.sources=None
        self.outDir=None
    def run(self):
        our=OUR()
        our.sources=self.sources
        our.outDir=self.outDir
        our.msgSin=self.msgSin
        try:
            our.closeAllExcel()
            outs=our.processAll()
        except Exception as e:
            self.msgSin.emit(str(e))
        if our.errMsg:
            self.msgSin.emit(our.errMsg)
        self.endSin.emit(outs)
if __name__ =='__main__':
    app=QtWidgets.QApplication(sys.argv)
    wind=Wind()
    sys.exit(app.exec_())