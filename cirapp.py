import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton,QInputDialog, QLineEdit, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QBrush, QColor, QFont, QPainterPath
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

        self.myPenWidth = 13
        self.myPenColor = Qt.black
        self.image = QImage(self.width, self.height, QImage.Format_RGB32)
        self.path = QPainterPath()
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
        self.lastpoint = None
        self.delete = False
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
        #self.clearImage()
        self.update()

    def clearImage(self):
        self.path = QPainterPath()
        self.image.fill(Qt.white)  ## switch it to else
        self.update()

    def saveImage(self, fileName, fileFormat):
        self.im = True
        self.image.save(fileName, fileFormat)

    def paintEvent(self,event):
        QMainWindow.paintEvent(self, event)
        #print(2)
        
        #painter0 = QPainter(self)
        #painter0.drawImage(event.rect(), self.image, self.rect())
        if self.circle:
            #print(3)
            painter = QPainter(self.image)
            #qp1 = QPainter(self)
            cp = QPainter(self)
            pen = QPen(Qt.red, 3)
            painter.setPen(pen)
            cp.setPen(pen)
            qp = QPainter(self)
            
            #
            qp.setPen(pen)
            qp.setFont(QFont('Decorative', 10))
            #qp1.setPen(pen)
            #qp1.setFont(QFont('Decorative', 10))
            self.clearImage()
            for i in self.circles:
                painter.drawEllipse(self.circles[i]['x'], self.circles[i]['y'], self.circles[i]['r'], self.circles[i]['r']) 
                cp.drawEllipse(self.circles[i]['x'], self.circles[i]['y'], self.circles[i]['r'], self.circles[i]['r']) 
                qp.drawText(self.circles[i]['x'], self.circles[i]['y'], self.circles[i]['lable'])
               # qp1.drawText(self.circles[i]['x'], self.circles[i]['y'], self.circles[i]['lable'])
            
            painter.end()
            qp.end()
            cp.end()
            #self.circle = False
            #qp1.end()
       
        if self.circle:
            qp1 = QPainter(self.image)
            qp1.setPen(pen)
            qp1.setFont(QFont('Decorative', 10))
            for i in self.circles:
                qp1.drawText(self.circles[i]['x'], self.circles[i]['y'], self.circles[i]['lable'])
            qp1.end()

            if self.lastpoint != None:
                Cx, Cy, _ = getCircleCenter(self.lastpoint.x(),self.lastpoint.y(),self.circles)
            
                if not Cx==None:
                    
                    painter3 = QPainter(self)
                    pen = QPen(Qt.black,5)
                    painter3.setPen(pen)
                    painter3.drawPoint(Cx,Cy)
                    #self.points.append((Cx,Cy))
                    #self.press=False
                    painter3.end()

        if self.delete:
            self.circles, self.lines = DeleteCircle(self.lastpoint2.x(),self.lastpoint2.y(), self.circles, self.lines)
            self.delete = False
            
        if self.press :
            if len(self.points)==2:
                self.points = []
            try:
                self.points.append((Cx,Cy))
            except: 
                self.points = []
            self.press=False
            if len(self.points)==2 and self.points[0][0] != None and self.points[1][0] != None:
                self.line = QLine(self.points[0][0],self.points[0][1],self.points[1][0],self.points[1][1])
                #print(self.line)
                if not CheckAvailableLine(self.line.x1(),self.line.y1(),self.line.x2(),self.line.y2(), self.lines):
                    if not CheckEmptyLine(self.line):
                        self.points = []
                        self.lines = SaveLine(len(self.lines)+1, self.line, 'line'+str(len(self.lines)+1))
                    
        #if self.circle:
        painter1 = QPainter(self)
        Lpainter = QPainter(self)
        Tp1 = QPainter(self.image)
        pen = QPen(Qt.black, 3)
        painter1.setPen(pen)
        Tp1.setPen(pen)
        Lpainter.setPen(pen)
        Lpainter.setFont(QFont('Decorative', 10))
        Tp1.setFont(QFont('Decorative', 10))
        for l in self.lines.values():
            x,y = getLineCenter(l['line'].x1(),l['line'].y1(),l['line'].x2(),l['line'].y2())
            if not l['line'].isNull():
                painter1.drawLine(l['line'])
                Lpainter.drawText(x, y, l['lable'])
                Tp1.drawText(x, y, l['lable'])
        painter1.end()
        Lpainter.end()
        Tp1.end()
        
        Tp = QPainter(self.image)
        pen = QPen(Qt.black, 3)
        Tp.setPen(pen)
        for l in self.lines.values():
            x,y = getLineCenter(l['line'].x1(),l['line'].y1(),l['line'].x2(),l['line'].y2())
            if not l['line'].isNull():
                Tp.drawLine(l['line'])
        Tp.end()

        if self.im:
            painter0 = QPainter(self)
            painter0.drawImage(event.rect(), self.image, self.rect())
            #pass


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastpoint = event.pos()
            self.press = True
            self.update()
        if event.button() == Qt.RightButton:
            self.lastpoint2 = event.pos()
            self.delete = True
            self.update()
    '''        
    def mouseMoveEvent(self, event):
        self.path.lineTo(event.pos())
        p = QPainter(self.image)
        p.setPen(QPen(self.myPenColor,
                      self.myPenWidth, Qt.SolidLine, Qt.RoundCap,
                      Qt.RoundJoin))
        p.drawPath(self.path)
        p.end()
        self.update()'''

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