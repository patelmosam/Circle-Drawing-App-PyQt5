import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton,QInputDialog, QLineEdit, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QBrush, QColor, QFont, QPainterPath
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt, QPoint, QLine
from Cbackend import *
import numpy as np
import json

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'circle drawing app'
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
        self.circle = False
        self.m = 0
        self.circles = {}
        self.points = []
        self.line_list = {}
        self.press = False
        self.text = ''
        self.index = 0
        self.lines = {}
        self.im = False
        self.lastpoint, self.select_circle = None, None
        self.delete = False
        self.move = False

        button = QPushButton('Add', self)
        button.setToolTip('Add a new random circle')
        button.move(10,150)
        button.clicked.connect(self.draw_circle)
        
        button1 = QPushButton('Save', self)
        button1.setToolTip('Save image of canvas')
        button1.move(10,200)
        button1.clicked.connect(lambda : self.saveImage('image.png', 'PNG'))     

        button2 = QPushButton('Generate Report', self)
        button2.setToolTip('Generate a report')
        button2.move(10,250)
        button2.clicked.connect(self.report)  
        
        self.show()

    @pyqtSlot()
    def report(self):
        report = GenerateReport(self.circles, self.lines)
        with open('report.json','w') as file:
            json.dump(report,file)


    def draw_circle(self):
        button = self.sender()
        self.m+=1
        self.x, self.y, self.r, self.cname = getRandomCircle(self.m)
        self.circles = SaveCircle(self.m,self.x,self.y,self.r,self.cname)
        self.circle = True
        self.update()

    def clearImage(self):
        self.path = QPainterPath()
        self.image.fill(Qt.white)  
        self.update()

    def saveImage(self, fileName, fileFormat):
        self.im = True
        self.image.save(fileName, fileFormat)

    def paintEvent(self,event):
        QMainWindow.paintEvent(self, event)
 
        if self.circle:
            painter = QPainter(self.image)
            cp = QPainter(self)
            pen = QPen(Qt.red, 3)
            painter.setPen(pen)
            cp.setPen(pen)
            qp = QPainter(self)
            qp.setPen(pen)
            qp.setFont(QFont('Decorative', 10))
            self.clearImage()
            for i in self.circles:
                painter.drawEllipse(self.circles[i]['x'], self.circles[i]['y'], self.circles[i]['r'], self.circles[i]['r']) 
                cp.drawEllipse(self.circles[i]['x'], self.circles[i]['y'], self.circles[i]['r'], self.circles[i]['r']) 
                qp.drawText(self.circles[i]['x'], self.circles[i]['y'], self.circles[i]['lable'])
            
            painter.end()
            qp.end()
            cp.end()

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
                    painter3.end()

        if self.delete:
            self.circles, self.lines = DeleteCircle(self.lastpoint.x(),self.lastpoint.y(), self.circles, self.lines)
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
                
                if not CheckAvailableLine(self.line.x1(),self.line.y1(),self.line.x2(),self.line.y2(), self.lines):
                    if not CheckEmptyLine(self.line):
                        self.points = []
                        self.lines = SaveLine(len(self.lines)+1, self.line, 'line'+str(len(self.lines)+1))
                    
        
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
            

        if not self.select_circle is None:
            r = self.circles[self.select_circle]['r']
            self.circles[self.select_circle]['x'] = self.lastpoint2.x() 
            self.circles[self.select_circle]['y'] = self.lastpoint2.y() 
            P = QPoint(self.lastpoint2.x() + (r/2),self.lastpoint2.y() + (r/2))
            for l in self.line_list:
                if self.line_list[l] == 0:

                    self.lines[l]['line'].setP1(P)
                elif self.line_list[l] == 1:
                    self.lines[l]['line'].setP2(P)
            self.select_circle = None
            self.line_list = {}

        if self.move  and self.select_circle == None:
            x_,y_,self.select_circle = getCircleCenter(self.lastpoint.x(),self.lastpoint.y(),self.circles)
            
            if x_ is not None:
                for i,j in zip(line_info,line_info.values()):
                    if j['line'].x1()==int(x_) and j['line'].y1()==int(y_):
                        self.line_list[i] = 0
                    elif j['line'].x2()==int(x_) and j['line'].y2()==int(y_):
                        self.line_list[i] = 1
            self.move = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastpoint = event.pos()
            self.press = True
            self.update()
        if event.button() == Qt.RightButton:
            self.lastpoint2 = event.pos()
            self.move = True
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete = True
            self.update()

    def getText(self,index,type):
        text, okPressed = QInputDialog.getText(self, "Enter Lable",'change '+ type + " lable:", QLineEdit.Normal, "")
        if okPressed and text != '':
            if type == "circle":
                self.circles[index]['lable'] = text
            elif  type == 'line':
                self.lines[index]['lable'] = text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())