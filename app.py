import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton,QInputDialog, QLineEdit, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QBrush, QColor, QFont, QPainterPath
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt, QPoint, QLine
from backend import *
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

        self.cnt = 0
        self.circle_dict = {}
        self.points = []
        self.line_list = {}
        self.press = False
        self.text = ''
        self.index = 0
        self.line_dict = {}
        self.im = False
        self.lastpoint, self.select_circle = None, None
        self.delete = False
        self.move = False

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

        # add button for adding random circle
        button = QPushButton('Add', self)
        button.setToolTip('Add a new random circle')
        button.move(10,150)
        button.clicked.connect(self.draw_circle)
        
        # save button to save circle image
        button1 = QPushButton('Save', self)
        button1.setToolTip('Save image of canvas')
        button1.move(10,200)
        button1.clicked.connect(lambda : self.saveImage('image.png', 'PNG'))     

        # generate report button
        button2 = QPushButton('Generate Report', self)
        button2.setToolTip('Generate a report')
        button2.move(10,250)
        button2.clicked.connect(self.report)  
        
        self.show()

    # method for generate report, activates on generate report button press
    @pyqtSlot()
    def report(self):
        report = GenerateReport(self.circle_dict, self.line_dict)
        with open('report.json','w') as file:
            json.dump(report,file)

    # method for drawing circle, activates on add button press
    def draw_circle(self):
        button = self.sender()
        self.cnt+=1
        self.x, self.y, self.r, self.circle_lable = getRandomCircle(self.cnt)
        self.circle_dict = SaveCircle(self.cnt,self.x,self.y,self.r,self.circle_lable)
        self.circle = True
        self.update()

    def clearImage(self):
        self.path = QPainterPath()
        self.image.fill(Qt.white)  
        self.update()

    # method for save circle image, activates on save button press
    def saveImage(self, fileName, fileFormat):
        self.im = True
        self.image.save(fileName, fileFormat)

    # paint event method
    def paintEvent(self,event):
        QMainWindow.paintEvent(self, event)

        # draw circle & wirte lable on canvas paint event
        if self.circle:
            Cpainter = QPainter(self.image)
            Cpainter_img = QPainter(self)
            pen = QPen(Qt.red, 3)
            Cpainter.setPen(pen)
            Cpainter_img.setPen(pen)
            Tpainter1 = QPainter(self)
            Tpainter1.setPen(pen)
            Tpainter1.setFont(QFont('Decorative', 10))
            self.clearImage()
            for i in self.circle_dict:
                Cpainter.drawEllipse(self.circle_dict[i]['x'], self.circle_dict[i]['y'], self.circle_dict[i]['r'], self.circle_dict[i]['r']) 
                Cpainter_img.drawEllipse(self.circle_dict[i]['x'], self.circle_dict[i]['y'], self.circle_dict[i]['r'], self.circle_dict[i]['r']) 
                Tpainter1.drawText(self.circle_dict[i]['x'], self.circle_dict[i]['y'], self.circle_dict[i]['lable'])
            
            Cpainter.end()
            Tpainter1.end()
            Cpainter_img.end()

        if self.circle:

            # draw circle on image paint event
            Tpainter1_img = QPainter(self.image)
            Tpainter1_img.setPen(pen)
            Tpainter1_img.setFont(QFont('Decorative', 10))
            for i in self.circle_dict:
                Tpainter1_img.drawText(self.circle_dict[i]['x'], self.circle_dict[i]['y'], self.circle_dict[i]['lable'])
            Tpainter1_img.end()

            # draw point paint event for selecting circle
            if self.lastpoint != None:
                Cx, Cy, _ = getCircleCenter(self.lastpoint.x(),self.lastpoint.y(),self.circle_dict)
              
                if not Cx==None:
                    Ppainter = QPainter(self)
                    pen = QPen(Qt.black,5)
                    Ppainter.setPen(pen)
                    Ppainter.drawPoint(Cx,Cy)
                    Ppainter.end()

        # erase circle paint event 
        if self.delete:
            self.circle_dict, self.line_dict = DeleteCircle(self.lastpoint.x(),self.lastpoint.y(), self.circle_dict, self.line_dict)
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
                
                if not CheckAvailableLine(self.line.x1(),self.line.y1(),self.line.x2(),self.line.y2(), self.line_dict):
                    if not CheckEmptyLine(self.line):
                        self.points = []
                        self.line_dict = SaveLine(len(self.line_dict)+1, self.line, 'line'+str(len(self.line_dict)+1))
                    
        # draw line and lable on canvas event 
        Lpainter = QPainter(self)
        Tpainter2 = QPainter(self)
        Tpainter2_img = QPainter(self.image)
        pen = QPen(Qt.black, 3)
        Lpainter.setPen(pen)
        Tpainter2_img.setPen(pen)
        Tpainter2.setPen(pen)
        Tpainter2.setFont(QFont('Decorative', 10))
        Tpainter2_img.setFont(QFont('Decorative', 10))
        for l in self.line_dict.values():
            x,y = getLineCenter(l['line'].x1(),l['line'].y1(),l['line'].x2(),l['line'].y2())
            if not l['line'].isNull():
                Lpainter.drawLine(l['line'])
                Tpainter2.drawText(x, y, l['lable'])
                Tpainter2_img.drawText(x, y, l['lable'])
        Lpainter.end()
        Tpainter2.end()
        Tpainter2_img.end()
        
        # draw line on image event 
        Lpainter_img = QPainter(self.image)
        pen = QPen(Qt.black, 3)
        Lpainter_img.setPen(pen)
        for l in self.line_dict.values():
            x,y = getLineCenter(l['line'].x1(),l['line'].y1(),l['line'].x2(),l['line'].y2())
            if not l['line'].isNull():
                Lpainter_img.drawLine(l['line'])
        Lpainter_img.end()

        # draw image event
        if self.im:
            Ipainter = QPainter(self)
            Ipainter.drawImage(event.rect(), self.image, self.rect())
            
        # circle move action
        if not self.select_circle is None:
            r = self.circle_dict[self.select_circle]['r']
            self.circle_dict[self.select_circle]['x'] = self.lastpoint2.x() 
            self.circle_dict[self.select_circle]['y'] = self.lastpoint2.y() 
            P = QPoint(self.lastpoint2.x() + (r/2),self.lastpoint2.y() + (r/2))
            for l in self.line_list:
                if self.line_list[l] == 0:

                    self.line_dict[l]['line'].setP1(P)
                elif self.line_list[l] == 1:
                    self.line_dict[l]['line'].setP2(P)
            self.select_circle = None
            self.line_list = {}

        if self.move  and self.select_circle == None:
            x_,y_,self.select_circle = getCircleCenter(self.lastpoint.x(),self.lastpoint.y(),self.circle_dict)
            
            if x_ is not None:
                for i,j in zip(line_info,line_info.values()):
                    if j['line'].x1()==int(x_) and j['line'].y1()==int(y_):
                        self.line_list[i] = 0
                    elif j['line'].x2()==int(x_) and j['line'].y2()==int(y_):
                        self.line_list[i] = 1
            self.move = False

    # mouse press event method
    def mousePressEvent(self, event):
        '''
        left mouse button: for select circle
        right mouse button: for move circle
        '''
        if event.button() == Qt.LeftButton:
            self.lastpoint = event.pos()
            self.press = True
            self.update()
        if event.button() == Qt.RightButton:
            self.lastpoint2 = event.pos()
            self.move = True
            self.update()
  
    # mouse double click event
    def mouseDoubleClickEvent(self, event):
        '''
        mouse double click: for change the lable of circle and line
        '''
        if event.button() == Qt.LeftButton:
            self.lastpoint1 = event.pos()
            Cx, Cy, index = getCircleCenter(self.lastpoint1.x(),self.lastpoint1.y(),self.circle_dict)
            lx, ly, lindex = getLineCBox(self.lastpoint1.x(),self.lastpoint1.y(),self.line_dict)
            
            if not lindex==None:
                self.getText(lindex, 'line')
            elif not index==None:
                self.getText(index, 'circle')
                
            self.update()

    # delete key press event method
    def keyPressEvent(self, event):
        ''' delete key: for deleting circle '''
        if event.key() == Qt.Key_Delete:
            self.delete = True
            self.update()

    # helper method for changing lable 
    def getText(self,index,type):
        text, okPressed = QInputDialog.getText(self, "Enter Lable",'change '+ type + " lable:", QLineEdit.Normal, "")
        if okPressed and text != '':
            if type == "circle":
                self.circle_dict[index]['lable'] = text
            elif  type == 'line':
                self.line_dict[index]['lable'] = text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())