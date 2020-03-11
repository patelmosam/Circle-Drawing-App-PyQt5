import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton,QInputDialog, QLineEdit, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt, QPoint, QLine
from Cbackend import *
import numpy as np

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 700
        self.top = 700
        self.width = 1200
        self.height = 1000
        self.image = QImage(self.width, self.height, QImage.Format_RGB32)
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black

        self.label = QLabel(self)
        self.label.resize(80,20)


        button = QPushButton('Add', self)
        button.setToolTip('This is an example button')
        button.move(10,150)
        button.clicked.connect(self.draw_circle)
        
        button1 = QPushButton('Save', self)
        button1.setToolTip('This is an example button')
        button1.move(10,200)
        button1.clicked.connect(lambda : self.saveImage('image.png', 'PNG'))     
        self.circle = False
        self.m = 0
        self.circles = {}
        self.points = []
        self.press = False
        self.press1 = False
        self.text = ''
        self.text1 = ''
        self.index = 0
        self.lines = {}
        self.lcnt = 0
        self.im = False
        #self.line = QLineEdit(self)
        button2 = QPushButton('Generate Report', self)
        button2.setToolTip('This is an example button')
        button2.move(10,250)
        button2.clicked.connect(self.p)  
        
        self.show()

    def p(self):
        print(self.circles)
    @pyqtSlot()
    def on_click(self):
        print('button click')

    @pyqtSlot()
    def on_click1(self):
        print('button1 click')

    @pyqtSlot()
    def on_click2(self):
        print('button2 click')

    def draw_circle(self):
        button = self.sender()
        self.m+=1
        self.x, self.y, self.r, self.cname = getRandomCircle(self.m)
        self.circles = SaveCircle(self.m,self.x,self.y,self.r,self.cname)
        self.circle = True
        self.update()

    def saveImage(self, fileName, fileFormat):
        self.im = True
        self.image.save(fileName, fileFormat)

    def paintEvent(self,event):
        QMainWindow.paintEvent(self, event)
        
        if self.circle:
            #print(3)
            painter = QPainter(self)
            pen = QPen(Qt.red, 3)
            painter.setPen(pen)
            qp = QPainter(self)
            qp.setPen(pen)
            qp.setFont(QFont('Decorative', 10))
            
            for i in range(1,self.m+1):
                painter.drawEllipse(self.circles[i]['x'], self.circles[i]['y'], self.circles[i]['r'], self.circles[i]['r']) 
                qp.drawText(self.circles[i]['x'], self.circles[i]['y'], self.circles[i]['lable'])
            painter.end()
            qp.end()
       

        if self.press:
            Cx, Cy, _ = getCircleCenter(self.lastpoint.x(),self.lastpoint.y(),self.circles)
            if len(self.points)==2:
                self.points = []
            if not Cx==None:
                painter3 = QPainter(self)
                pen = QPen(Qt.black,5)
                painter3.setPen(pen)
                painter3.drawPoint(Cx,Cy)
                self.points.append((Cx,Cy))
                self.press=False
                painter3.end()
            
            if len(self.points)==2:
                line = False
                self.line = QLine(self.points[0][0],self.points[0][1],self.points[1][0],self.points[1][1])
                if not CheckAvailableLine(self.line, self.lines):
                    if not CheckEmptyLine(self.line):
                        self.lines = SaveLine(len(self.lines)+1, self.line, 'line'+str(len(self.lines)+1))
                 
        painter1 = QPainter(self)
        Lpainter = QPainter(self)
        pen = QPen(Qt.black, 3)
        painter1.setPen(pen)
        Lpainter.setPen(pen)
        Lpainter.setFont(QFont('Decorative', 10))
        for l in self.lines.values():
            x,y = getLineCenter(l['line'].x1(),l['line'].y1(),l['line'].x2(),l['line'].y2())
            if not l['line'].isNull():
                painter1.drawLine(l['line'])
                Lpainter.drawText(x, y, l['lable'])
        painter1.end()
        Lpainter.end()
        
        if self.im:
            #painter0 = QPainter(self)
            #painter0.drawImage(event.rect(), self.image, self.rect())
            pass


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastpoint = event.pos()
            self.press = True
            self.update()
            
    
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastpoint1 = event.pos()
            Cx, Cy, index = getCircleCenter(self.lastpoint1.x(),self.lastpoint1.y(),self.circles)
            lx, ly, lindex = getLineCBox(self.lastpoint1.x(),self.lastpoint1.y(),self.lines)
            
            if not lindex==None:
                self.getText(lindex, 'line')
            elif not index==None:
                self.getText(index, 'circle')
                
            self.update()

    def getText(self,index,type):
        text, okPressed = QInputDialog.getText(self, "Enter Lable",'change '+ type + " lable:", QLineEdit.Normal, "")
        if okPressed and text != '':
            #self.text1 = text
            if type == "circle":
                self.circles[index]['lable'] = text
            elif  type == 'line':
                self.lines[index]['lable'] = text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())