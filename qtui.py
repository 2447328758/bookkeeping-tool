from datetime import date
from PySide6.QtWidgets import *
from PySide6.QtCore import QFile,Signal,QDate
from PySide6.QtUiTools import QUiLoader
from Bill import Bill


class DateDialog(QWidget):
    datesignal =Signal(str)
    def __init__(self, parent=None):
        super(DateDialog,self).__init__()
        self.initGUI()
        self.initEvent()

    def initGUI(self):
        qfile = QFile("UIModifyDate.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()
        self.ui = QUiLoader().load(qfile)

    def initEvent(self):
        self.ui.srsubmit.clicked.connect(self.accept)
        self.ui.srcancle.clicked.connect(self.reject)

    def accept(self):
        date_tuple = QDate(self.ui.dateTimeEdit.date()).getDate()
        print("accept"+str(date(date_tuple[0],date_tuple[1],date_tuple[2])).replace("-","/"))
        self.datesignal.emit(str(date(date_tuple[0],date_tuple[1],date_tuple[2])).replace("-","/"))
        self.ui.close()
        self.close()

    def reject(self):
        print("reject")
        self.ui.close()
        self.close()

class MainWin(QMainWindow):
    waysignal = Signal(int)
    def __init__(self):
        super(MainWin,self).__init__()
        self.initGUI()
        self.setLBDate(str(date.today()).replace("-","/"))
        self.initEvent()
        self.waysignal.emit(1)

    def initGUI(self):
        qfile = QFile("UiMain.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()
        self.ui=QUiLoader().load(qfile)
        self.ui.show()
        self.dateDialog=DateDialog()
        
        
    def initEvent(self):
        self.ui.srdatemodify.clicked.connect(self.UiDateModifyDialogShow)
        self.dateDialog.datesignal.connect(self.getDateFromDialog)
        self.ui.srsubmit.clicked.connect(self.submitButtonClicked)
        self.waysignal.connect(self.setWay)
        self.ui.srway.currentIndexChanged.connect(lambda : self.waysignal.emit(1))
     
    def UiDateModifyDialogShow(self):
        self.dateDialog.ui.show()

    def getDateFromDialog(self,connect):
        self.setLBDate(connect)
        self.waysignal.emit(1)


    def submitButtonClicked(self):
       bill = Bill(
        indate=self.nowDate,
        # money=QSpinBox(self.ui.srmoney).value(),
        # python的强制类型转换创建了一个新的对象不是原来的对象
        # 所以不要轻易使用强制类型转换
        money=self.ui.srmoney.value(),
        way=self.ui.srway.currentText(),
        src=self.ui.srsrc.currentText(),
        pur=self.ui.srpur.toPlainText(),
        id=self.ui.srid.text()
        )
       print(bill.args)
       message = QMessageBox(self.ui)
       message.setWindowTitle("result")
       if bill.save():
        message.setText("SUCCESS!")
       else:
        message.setText("FAIL!")
       message.show()
    
    def setLBDate(self,date):
        self.nowDate=date
        self.ui.lbdateshow.setText(str(date))
        self.waysignal.emit(1) # 事件发生
    
    def setWay(self,connect):
        # print(f"connect:{connect}")
        way = self.ui.srway.currentText()
        # print(way)
        if(way == "ALIPAY"):
            self.ui.srid.setText(f'''{str(self.nowDate).replace("/","")}220014064914''' )
            #print(self.ui.srid.text())
        elif(way == "WECHAT"):
            self.ui.srid.setText("")
        
        
if __name__ == "__main__":
    app = QApplication()
    win = MainWin()
    app.exec()
    