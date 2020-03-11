import  numpy as np

circle_info = {}
line_info = {}

def getRandomCircle(index):
    max_X = 800
    max_Y = 800
    label = 'Cir'
    x = np.random.randint(100,max_X)
    y = np.random.randint(100,max_Y)
    r = np.random.randint(100,200)
    #print(x,y)
    if x+r>max_X:
        x = x-r
    if y+r>max_Y:
        y = y-r
    label = label + str(index)
    return x,y,r,label

def SaveCircle(n,x,y,r,lable):
    circle_info[n] = {'x':x,'y':y,'r':r,'lable':lable}
    return circle_info

def getCircleCenter(x,y, circle_dict):
    cx, cy, index = None, None, None
    for i,j in zip(circle_dict.values(),circle_dict.keys()):
        if (x>i['x'] and x<i['x'] + i['r']) and (y>i['y'] and y<i['y'] + i['r']):
            cx = i['x']+(i['r']/2)
            cy = i['y']+(i['r']/2)
            index = j
    return cx,cy,index

def SaveLine(index, line, lable):
    line_info[index] = {'line':line, 'lable':lable}
    return line_info

def getLineCenter(x1,y1,x2,y2):
    return abs((x1+x2))/2, abs((y1+y2))/2

def CheckAvailableLine(line, line_dir):
    for l in line_dir.values():
        if line.x1()==l['line'].x1() and line.y1()==l['line'].y1() \
             and line.x2()==l['line'].x2() and line.y2()==l['line'].y2():
            return True
        elif line.x1()==l['line'].x2() and line.y1()==l['line'].y2() \
             and line.x2()==l['line'].x1() and line.y2()==l['line'].y1():
            return True
    return False

def CheckEmptyLine(line):
    if line.x1() == line.x2() and line.y1()==line.y2():
        return True
    return False

def getLineCBox(l1, l2, line_dict):
    for l,i in zip(line_dict.values(),line_dict.keys()):
        x,y = getLineCenter(l['line'].x1(),l['line'].y1(),l['line'].x2(),l['line'].y2())
        if (l1>x-20 and l1<x+20) and (l2>y-20 and l2<y+20):
            return x,y,i
    return None,None,None

