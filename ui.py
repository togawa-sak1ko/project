import sys
import json
import test as t
from PyQt5.QtWidgets import *
from PyQt5 import uic,QtGui,QtCore
import pyqtgraph as pg
import matplotlib.pyplot as plt
import math
earth_radius = 6371
import pyproj

class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_data()
        self.init_ui()
        self.initdraw()

    def init_ui(self):
        self.ui = uic.loadUi("map.ui")

        # 提取要操作的控件
        self.start = self.ui.lineEdit  # 起始

        self.end = self.ui.lineEdit_2  # 终点
        self.start1 = self.ui.lineEdit_3

        self.start2 = self.ui.lineEdit_4
        self.ends = self.ui.lineEdit_5

        self.findshortestpath = self.ui.btn1  # 最短时间
        self.findleasttrans = self.ui.btn2  # 最少换乘

        self.findshortestpath1 = self.ui.btn3
        self.findleasttrans1 = self.ui.btn4

        self.findshortestpath2 = self.ui.btn5
        self.findleasttrans2 = self.ui.btn6

        self.textBrowser_2 = self.ui.textBrowser_2
        self.vl = self.ui.vl
        self.getatt = self.ui.comboBox
        self.getatt.addItems(self.load_att())

        self.linemsg = self.ui.comboBox_2
        self.linemsg.addItems(self.loadline())
        self.transmsg = self.ui.comboBox_3
        self.transmsg.addItems(self.loadtrans())
        self.attrmsg = self.ui.comboBox_4
        self.attrmsg.addItems(self.load_att())

        self.searchline = self.ui.btn7
        self.searchtrans = self.ui.btn8
        self.searchattr = self.ui.btn9

        self.pw = pg.PlotWidget()

        # 设置图表标题
        self.pw.setTitle("线路", color='#008080', size='12pt')
        self.pw.setXRange(min=-100,  # 最小值
                          max=430)  # 最大值

        self.pw.setYRange(min=-100,  # 最小值
                        max=430)  # 最大值

        self.pw.setBackground('w')

        self.findshortestpath.clicked.connect(self.getshort)
        self.findleasttrans.clicked.connect(self.gettrans)
        self.findshortestpath1.clicked.connect(self.getshort1)
        self.findleasttrans1.clicked.connect(self.gettrans1)
        self.findshortestpath2.clicked.connect(self.getshort2)
        self.findleasttrans2.clicked.connect(self.gettrans2)
        self.searchline.clicked.connect(self.getlinemsg)
        self.searchtrans.clicked.connect(self.gettransmsg)
        self.searchattr.clicked.connect(self.getattrmsg)
    def init_data(self):
        with open('lines.json', 'r', encoding='utf-8') as f:
            data = f.read()
        self.dataA = json.loads(data)  # lines_1
        # print(dataA)  全线路，包含换乘站

        info = {}
        with open('subway.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                key, value = line.strip().split('=')  # 分割键和值
                # info[key] = value
                info1 = {}
                for item in value.strip().split(','):  # 分割键和值
                    k, v = item.strip().split(':')
                    info1[k] = v
                    # print(info1)
                info[key] = info1
        self.info = info    #线路距离关系文件，最短距离用

        info_t = {}
        with open('subway1.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                key, value = line.strip().split('=')  # 分割键和值
                # info[key] = value
                info3 = {}
                for item in value.strip().split(','):  # 分割键和值
                    k, v = item.strip().split(':')
                    info3[k] = v
                    # print(info1)
                info_t[key] = info3
        self.info_t = info_t    #线路距离关系文件，最少换乘用

        info_trans = {}
        with open('trans.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                key, value = line.strip().split('=')  # 分割键和值
                # info[key] = value
                info2 = {}
                for item in value.strip().split(','):  # 分割键和值
                    k, v = item.strip().split(':')
                    info2[k] = v
                    # print(info1)
                info_trans[key] = info2
        self.info_trans = info_trans    #换乘站距离关系文件

        with open('lines_1.json', 'r', encoding='utf-8') as f:
            data1 = f.read()
        self.dataB = json.loads(data1)  #全线路不含换乘站

        with open('position1.json', 'r', encoding='utf-8') as f:
            po = f.read()
        self.position = json.loads(po)  #全站点经纬度信息文件

        with open('color.json', 'r', encoding='utf-8') as f:
            co = f.read()
        self.color = json.loads(co) #线路颜色文件

        with open('attractions.json', 'r', encoding='utf-8') as f:
            at = f.read()
        self.attractions = json.loads(at)   #景点信息文件

    def dij(self, start, end):
        g = t.graph(self.info)
        d = t.dijkstra(g, start, self.info_trans, self.dataB, self.dataA)
        g1 = t.graph(self.info_t)
        d1 = t.dijkstra(g1, start, self.info_trans, self.dataB, self.dataA)
        self.short = d.find_shortest_path(end)
        self.s_time = d.getTime(self.short)
        self.s_price = d.getPrice(self.short)
        patha = d1.find_shortest_path(end)
        self.trans, self.trans_stas_2 = d1.totrans(patha)
        self.t_time = d1.getTime(self.trans)
        self.t_price = d1.getPrice(self.trans)
        self.trans_stas_1 = d.trans_station(self.short)


    def getshort(self):
            start = self.start.text()
            end = self.end.text()
            if start in self.info.keys() and end in self.info.keys():
                self.dij(start, end)
                delimiter = "-> "
                string = delimiter.join(self.short)
                delimiter1 = ', '
                string1 = delimiter1.join(self.trans_stas_1)
                self.textBrowser_2.setText(string+"\n"+"用时："+str(self.s_time)+'分钟'+'\n'+'票价：'+str(self.s_price)+'元'+'\n'+'换乘站：'+string1)
                self.textBrowser_2.repaint()
                self.draw(self.short)
            else:
                self.textBrowser_2.setText('...')
                self.textBrowser_2.repaint()

    def gettrans(self):
        start = self.start.text()
        end = self.end.text()
        if start in self.info.keys() and end in self.info.keys():
            self.dij(start, end)
            delimiter = "-> "
            string = delimiter.join(self.trans)
            delimiter1 = ', '
            string1 = delimiter1.join(self.trans_stas_2)
            self.textBrowser_2.setText(string+"\n"+"用时："+str(self.t_time)+'分钟'+'\n'+'票价：'+str(self.t_price)+'元'+'\n'+'换乘站：'+string1)
            self.textBrowser_2.repaint()
            self.draw(self.trans)
        else:
            self.textBrowser_2.setText('...')
            self.textBrowser_2.repaint()

    def wgs48_to_xy(self, lon, lat):
        latlon = pyproj.Proj(init='epsg:4326')
        xy = pyproj.Proj(init='epsg:3857')
        x = []
        y = []
        for a, b in zip(lon, lat):
            x1, y1 = pyproj.transform(latlon, xy, a, b)
            x.append(int((x1 - 12932851) / 100))
            y.append(int((y1 - 4855241) / 100))
        return x, y


    def initdraw(self):
        for k, v in self.position.items():
            x = []
            y = []
            for key, value in v.items():
                x.append(value[0])
                y.append(value[1])
            a, b = self.wgs48_to_xy(x, y)
            color = self.color[k]
            self.pw.plot(a,
                         b,
                         pen = QtGui.QPen(QtGui.QColor(color), 2, QtCore.Qt.SolidLine),
                         symbol = 'o',
                         symbolPen = "#000000",
                         symbolSize = 10
                         )
            self.vl.addWidget(self.pw)
    def draw(self, path):
        self.pw.clear()
        self.initdraw()
        x = []
        y = []
        for station in path:
            for k, v in self.position.items():
                if station in v.keys():
                    x.append(v[station][0])
                    y.append(v[station][1])
        a, b = self.wgs48_to_xy(x, y)
        self.pw.plot(a,
                     b,
                     pen=QtGui.QPen(QtGui.QColor(0,0,0), 5, QtCore.Qt.SolidLine),
                     symbol='o',
                     symbolPen="#F8F8FF",
                     symbolSize=10
                     )
        self.vl.addWidget(self.pw)


    def load_att(self):
        attr = []
        for key, value in self.attractions.items():
            for i in value:
                attr.append(i)
        return attr

    def getshort1(self):
        start = self.start1.text()
        for k, v in self.attractions.items():
            if self.getatt.currentText() in v:
                end1 = k
                break
        if start in self.info.keys() and end1 in self.info.keys():
            self.dij(start, end1)
            delimiter = "-> "
            string = delimiter.join(self.short)
            delimiter1 = ', '
            string1 = delimiter1.join(self.trans_stas_1)
            self.textBrowser_2.setText(string+"\n"+"用时："+str(self.s_time)+'分钟'+'\n'+'票价：'+str(self.s_price)+'元'+'\n'+'换乘站：'+string1)
            self.textBrowser_2.repaint()
            self.draw(self.short)
        else:
            self.textBrowser_2.setText('...')
            self.textBrowser_2.repaint()

    def gettrans1(self):
        start = self.start1.text()
        for k, v in self.attractions.items():
            if self.getatt.currentText() in v:
                end1 = k
                break
        if start in self.info.keys() and end1 in self.info.keys():
            self.dij(start, end1)
            delimiter = "-> "
            string = delimiter.join(self.trans)
            delimiter1 = ', '
            string1 = delimiter1.join(self.trans_stas_2)
            # string1 = delimiter1.join(self.patha)
            self.textBrowser_2.setText(string+"\n"+"用时："+str(self.t_time)+'分钟'+'\n'+'票价：'+str(self.t_price)+'元'+'\n'+'换乘站：'+string1)
            self.textBrowser_2.repaint()
            self.draw(self.trans)
        else:
            self.textBrowser_2.setText('...')
            self.textBrowser_2.repaint()

    def splite(self):
        e = []
        for i in self.ends.text().strip().split(' '):
            e.append(i)
        self.attrs = e

    def getshort2(self):
        start = self.start2.text()
        self.short1 = []
        trans = []
        self.splite()
        time1 = 0
        price1 = 0
        for i in self.attrs:
            end1 = i
            for k, v in self.attractions.items():
                if end1 in v:
                    end = k
                    if end1 != self.attrs[0]:
                        start1 = self.attrs[self.attrs.index(end1) - 1]
                        for k, v in self.attractions.items():
                            if start1 in v:
                                start = k
                    break
            if start in self.info.keys() and end in self.info.keys():
                self.dij(start, end)
                self.short1.extend(self.short)
                self.short1.append(end1)
                time1 += self.s_time
                price1 += self.s_price
                trans.extend(self.trans_stas_1)
            else:
                self.textBrowser_2.setText('...')
                self.textBrowser_2.repaint()
        self.draw(self.short1)
        count = 0
        for i in self.short1:
            if self.short1.count(i) > 1:
                count += 1
        delimiter = "-> "
        string = delimiter.join(self.short1)
        delimiter1 = ', '
        string1 = delimiter1.join(trans)
        if count <= 5:
            count = 1 - 0.1 * count
        else:
            count = 0.5
        price1 = price1 * count
        self.textBrowser_2.setText(string + "\n" + "用时：" + str(time1) + '分钟' + '\n' + '票价：' + str(
            price1) + '元' + '\n' + '换乘站：' + string1)
        self.textBrowser_2.repaint()

    def gettrans2(self):
        start = self.start2.text()
        self.trans1 = []
        trans = []
        self.splite()
        time1 = 0
        price1 = 0
        for i in self.attrs:
            end1 = i
            for k, v in self.attractions.items():
                if end1 in v:
                    end = k
                    if end1 != self.attrs[0]:
                        start1 = self.attrs[self.attrs.index(end1) - 1]
                        for k, v in self.attractions.items():
                            if start1 in v:
                                start = k
                    break
            if start in self.info.keys() and end in self.info.keys():
                self.dij(start, end)
                self.trans1.extend(self.trans)
                self.trans1.append(end1)
                time1 += self.t_time
                price1 += self.t_price
                trans.extend(self.trans_stas_2)
            else:
                self.textBrowser_2.setText('...')
                self.textBrowser_2.repaint()
        self.draw(self.trans1)
        count = 0
        for i in self.trans1:
            if self.trans1.count(i) > 1:
                count += 1
        delimiter = "-> "
        string = delimiter.join(self.trans1)
        delimiter1 = ', '
        string1 = delimiter1.join(trans)
        if count <= 5:
            count = 1 - 0.1 * count
        else:
            count = 0.5
        price1 = price1 * count
        self.textBrowser_2.setText(string + "\n" + "用时：" + str(time1) + '分钟' + '\n' + '票价：' + str(
            int(price1)) + '元' + '\n' + '换乘站：' + string1)
        self.textBrowser_2.repaint()

    def loadline(self):
        line = []
        for k, v in self.dataA.items():
            line.append(k+'号线')
        return line

    def loadtrans(self):
        line = []
        for k, v in self.info_trans.items():
            line.append(k)
        return line

    def getlinemsg(self):
        line = self.linemsg.currentText()[0]
        for k, v in self.dataA.items():
            if k == line:
                delimiter1 = ', '
                string = delimiter1.join(v)
                self.textBrowser_2.setText('以下站点属于'+str(line)+'号线:\n'+string)
                self.textBrowser_2.repaint()

    def gettransmsg(self):
        s = self.transmsg.currentText()
        for k, v in self.info_trans.items():
            if k == s:
                delimiter1 = ', '
                string = delimiter1.join(v)
                self.textBrowser_2.setText('该换乘站可通往以下站点:\n'+string)
                self.textBrowser_2.repaint()


    def getattrmsg(self):
        a = self.attrmsg.currentText()
        for k, v in self.attractions.items():
            if a in v:
                self.textBrowser_2.setText('在'+str(k)+'站下车')
                self.textBrowser_2.repaint()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyWindow()
    # 展示窗口
    w.ui.show()

    app.exec()

