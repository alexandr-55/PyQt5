import sys
import random
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel
import PyQt5.QtGui as QtGui
from PyQt5.QtCore import Qt
from PyQt5 import Qt
from PyQt5.QtWidgets import QLCDNumber

#  Начальный диалог - выбор уровня сложности игры
class Example(QMainWindow):
    def __init__(self):
        self.wid = 0
        self.heig = 0
        self.mine = 0
        self.sp = []
        self.sp_mine = []
        super().__init__()
        uic.loadUi('1.ui', self)
        self.initUI()
        
    def initUI(self): 
        # кнопки выбора уровня сложности игры
        self.radioButton.clicked.connect(self.size_init)
        self.radioButton_2.clicked.connect(self.size_init)
        self.radioButton_3.clicked.connect(self.size_init)
        self.radioButton_4.clicked.connect(self.size_init)
        self.pushButton.clicked.connect(self.field)
    
    def size_init(self):
        if self.sender().text() == 'Легкий':
            self.wid = self.heig = self.mine = 10
        elif self.sender().text() == 'Средний':
            self.wid = self.heig = 16
            self.mine = 40
        elif self.sender().text() == 'Сложный':
            self.wid = 30
            self.heig = 16
            self.mine = 99
        elif self.sender().text() == 'Собственный': # требуется разработка 
            self.wid = 0
            self.heig = 0
            self.mine = 0            
        
    def field(self):        
        self.ex3 = Example2(self.wid, self.heig, self.mine)
        self.show()
        

class Example2(QWidget): 
    def __init__(self, wid, heig, mine):
        self.wid = wid
        self.heig = heig
        self.mine = mine
        self.sp_sosedi = []     #поле для мин и подсчета мин вокруг ячейки 
        super().__init__()
        self.initUI()
  
    def initUI(self):
        # создаем поле для игры
        if self.wid == 10 and self.heig == 10:
            self.setGeometry(350, 200, 200, 250)
        elif self.wid == 16 and self.heig == 16:
            self.setGeometry(230, 180, 320, 370)
        elif self.wid == 30 and self.heig == 16:
            self.setGeometry(0, 180, 600, 370)
        else:
            self.setGeometry(350, 200, 200, 250)
            self.label1 = QLabel(self)
            self.label1.setFont(Qt.QFont("sefif", 10))  
            self.label1.setText("Режим в разработке")
            self.label1.move(70, 10)        
            pass   # добавить режим
        #
        #  Расставим кнопки - ячейки
        n0 = 50
        self.sp = []
        num = 0
        for i in range(self.heig):
            n = 0
            sp0 = []
            for j in range(self.wid):               
                sp0.append(QPushButton('', self))
                sp0[-1].resize(20, 20)
                sp0[-1].move(n, n0)
                sp0[-1].setObjectName(str(num))
                sp0[-1].setText('')
                num += 1
                n += 20
            n0 += 20
            self.sp.append(sp0)
        #
        # создание поля для вывода результата игры
        self.label = QLabel(self)
        self.label.setFont(Qt.QFont("sefif", 10))  
        self.label.setText("                           ")
        self.label.move(80, 10)            
        #
        # создаем  поля для отображения кол-ва ненайденных мин
        self.LCD_count = QLCDNumber(self)
 #       self.LCD_count.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.LCD_count.move(0, 0)
        self.count = self.mine
        self.LCD_count.setStyleSheet("QLCDNumber { background-color: red; color: white; }")     
        self.LCD_count.display(self.count) 
        #
        # расставляю миным 
        self.setMine_random()
        #
        # в списоу sp_sosedi положить мины (число-9) для остальных ячеек 
        # подсчитать кол. мин по соседству
        self.count_sosedi()
        for i in self.sp:
            for j in i:
                j.clicked.connect(self.press_btn)     #j.deleteLater)#)
        self.show()

    #  random-ая расстановка мин для игрыb
    def setMine_random(self):
        self.sp_mine = []
        for ih in range(self.heig):
            p = []
            for jw in range(self.wid):
                p.append(False)
            self.sp_mine.append(p)
        for i in range(self.mine):
            x = random.randint(0, len(self.sp_mine) - 1)
            y = random.randint(0, len(self.sp_mine[0]) - 1)
            while self.sp_mine[x][y]:
                x = random.randint(0, len(self.sp_mine) - 1)
                y = random.randint(0, len(self.sp_mine[0]) - 1)
            self.sp_mine[x][y] = True  

    # в список sp_sosedi положить мины (число - 9),
    # для остальных ячеек подсчитать кол. мин по соседству
    def count_sosedi(self):
        # сначало все ячейки = 0
        for i in self.sp_mine:
            sp0 = []
            for j in i:
                sp0.append(0)
            self.sp_sosedi.append(sp0)
        for ih in range(self.heig):
            for jw in range(self.wid):
                #print("111", i, j)
                if self.is_mine(ih, jw):
                    self.sp_sosedi[ih][jw] = 9
                    if self.is_btn_exist(ih - 1, jw - 1):
                        self.sp_sosedi[ih - 1][jw - 1] += 1
                    if self.is_btn_exist(ih - 1, jw):
                        self.sp_sosedi[ih - 1][jw] += 1
                    if self.is_btn_exist(ih - 1, jw + 1):
                        self.sp_sosedi[ih - 1][jw + 1] += 1 
                    if self.is_btn_exist(ih, jw - 1):
                        self.sp_sosedi[ih][jw - 1] += 1
                    if self.is_btn_exist(ih, jw + 1):
                        self.sp_sosedi[ih][jw + 1] += 1  
                    if self.is_btn_exist(ih + 1 , jw - 1):
                        self.sp_sosedi[ih + 1][jw - 1] += 1
                    if self.is_btn_exist(ih + 1, jw):
                        self.sp_sosedi[ih + 1][jw] += 1  
                    if self.is_btn_exist(ih + 1, jw + 1):
                        self.sp_sosedi[ih + 1][jw + 1] += 1 
        #for i in self.sp_mine:
            #print(i)
        #for i in self.sp_sosedi:
            #print(i)
 
    # возвращает наличие\отсутствие бомбы        
    def is_mine(self, ih, jw):
        return self.sp_mine[ih][jw]
    
    def is_btn_exist(self, ih, jw):
        if ih < 0 or jw < 0:
            return False      
        if ih >= self.heig or jw >= self.wid:
            return False
        if self.is_mine(ih, jw):
            return False
        return True     
    
    #
    # Нажатие на правую кнопку мышки
    def press_btn(self):
        # определить координаты нажатой кнопки на игровом поле
        n = int(self.sender().objectName())  
        k_ih = n // self.wid
        k_jw = n % self.wid
        #
        if self.label.text().strip() != '': # есть рез-т прошлой игры
            pass 
        elif self.sender().text() == '*':   # если пометка мины, то снять её
            self.sender().setText('')
            self.count += 1
            self.LCD_count.display(self.count)
        elif self.sender().text() != '':      # ячейка уже открыта ранее - ничего не делать
            pass           
        elif self.is_mine(k_ih, k_jw):      # открылась мина - это проигрыш
            # показать правильное расположение мин (на белом фоне), ошибка - на красном
            for jw in range(self.wid):
                for ih in range(self.heig):
                    if self.is_mine(ih, jw):
                        mstyle = 'QPushButton {background-color: white; color: red;}'
                        self.sp[ih][jw].setStyleSheet(mstyle)
                        self.sp[ih][jw].setText('M')
            # показать ошибку - на красном
            mstyle = 'QPushButton {background-color: red; color: black;}'
            self.sender().setStyleSheet(mstyle)
            self.sender().setText('M') 
            self.label.setText("*** Проигрыш ***")
        elif self.sp_sosedi[k_ih][k_jw] != 0 :  # у ячейки есть соседи 
            aa = self.sp_sosedi[k_ih][k_jw]
            self.sender().setText(str(aa))  # показать кол-во соседей
        else:    # ячейка пустая
            #  помечу уже найденные пустые ячейки числом 77 ( 0 --> 77)
            self.sp_sosedi[k_ih][k_jw] = 77
            self.open_null_cell(k_ih, k_jw)  # рекурсивный поиск соседних пустых ячеек
            #for ki in self.sp_sosedi:
                #print('! ', ki)              #
            # поиск границы (ячеек с соседями) для найденной области пустых ячеек (77)  
            for ih in range(self.heig):
                for jw in range(self.wid):
                    if self.sp_sosedi[ih][jw] == 77:
                        self.open_granicy(ih, jw)
            for ih in range(self.heig):
                for jw in range(self.wid):
                    if self.sp_sosedi[ih][jw] == 77:
                        mstyle = 'QPushButton {background-color: cyan; color: black;}'
                        self.sp[ih][jw].setStyleSheet(mstyle)
                        self.sp[ih][jw].setText('.')  
                        
    #
    # рекурсивный поиск пустых ячеек рядом с заданной с заменой значения 0 -> 77
    def open_null_cell(self, tih, tjw): 
        for i in range(tih - 1, tih + 2):
            for j in range(tjw - 1, tjw + 2):
                if self.is_btn_exist(i, j):
                    if self.sp_sosedi[i][j] == 0:
                        self.sp_sosedi[i][j] = 77
                        self.open_null_cell(i, j)     
        return True
    
    #
    # вывести на игровое поле ячейки с числами вокруг пустой области 
    def open_granicy(self, iht, jwt):
        for i in range(iht - 1, iht + 2):
            for j in range(jwt - 1, jwt + 2):
                if self.is_btn_exist(i, j):
                    if self.sp[i][j].text() == '' and  (0 < self.sp_sosedi[i][j] < 9):
                        aa = self.sp_sosedi[i][j]
                        self.sp[i][j].setText(str(aa))
                                                               
    # нажатие на правую клавишу мыши - пометка\снятие пометки с мины
    def mousePressEvent(self, event):
#        if event.button() == Qt.RightButton:
        xm = event.x()
        ym = event.y()
        w1 = xm // 20
        h1 = (ym - 50) // 20
        if w1 >= 0 and h1 >= 0:
            if self.sp[h1][w1].text() == '*':
                mstyle = 'QPushButton {color: black;}'
                self.sp[h1][w1].setStyleSheet(mstyle)                            
                self.sp[h1][w1].setText('')
                self.count += 1
                self.LCD_count.display(self.count)                
            elif self.sp[h1][w1].text() == '':
                mstyle = 'QPushButton {color: blue;}'
                self.sp[h1][w1].setStyleSheet(mstyle)                
                self.sp[h1][w1].setText('*')
                self.count -= 1
                self.LCD_count.display(self.count)
        # все мины расставлены - сверка с исходной расстановкой
        if self.count == 0:
            osh = False
            for ih in range(self.heig):
                for jw in range(self.wid):
                    if self.sp[ih][jw].text() == '*' and self.sp_sosedi[ih][jw] != 9:
                        osh = True
            if osh:
                for ih in range(self.heig):
                    for jw in range(self.wid):
                        if self.is_mine(ih, jw):
                            mstyle = 'QPushButton {background-color: red; color: black;}'
                            self.sp[ih][jw].setStyleSheet(mstyle)
                            self.sp[ih][jw].setText('M')
                            self.label.setText("***   Проигрыш   ***  :(")
            else:
                self.label.setText("ПОБЕДА!!!")
  
    def view_mine(self):
        for i in range(len(self.sp_mine)):
            for j in range(len(self.sp[i])):
                if self.sp_mine[i][j]: pass
                    #self.sp[i][j].setText('m')
           
    def print_sosedi(self):
        for i in self.sp_sosedi:
            print(i)

                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())