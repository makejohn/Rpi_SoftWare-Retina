import numpy as np
import cv2
from os.path import join
import os
from os import system,name
from sys import argv
from retinavision.retina import Retina
from retinavision import datadir, utils
from retinavision.cortex import Cortex
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#default save path
v_save_path = argv[1] + '/'

#check if the path exist or not, if not, creat the path
def path_exist():
    x = os.path.exists(v_save_path)
    if x:
        print('File Exist!')
    else:
        os.makedirs(v_save_path)
path_exist()
##clear function for clean the screen on both window and linxu system.
def clear():
    if name =='nt':
        _ = system('cls')
    else:
        _ = system('clear')

clear()

#Prepare cortex
C = Cortex(gpu=False)
lp = join(datadir, "cortices", "50k_Lloc_tight.pkl")
rp = join(datadir, "cortices", "50k_Rloc_tight.pkl")
C.loadLocs(lp, rp)
C.loadCoeffs(join(datadir, "cortices", "50k_Lcoeff_tight.pkl"),join(datadir, "cortices", "50k_Rcoeff_tight.pkl"))
os.system('sh sendVector.sh')
V = np.load('tmp/vector.npy')
cimg = C.cort_img(V)
cv2.imwrite('tmp/cimg_tmp.jpg',cimg)
class retinaGui(QtGui.QWidget):
    
    def __init__(self):
        super(retinaGui, self).__init__()
        self.initUI()
    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('retina', 10))
        self.setToolTip('retina')
        
        # Show image
        self.pic = QtGui.QLabel(self)
        self.pic.setGeometry(50, 150, 800, 400)
        self.pic.setPixmap(QtGui.QPixmap("tmp/cimg_tmp.jpg"))
        self.pic.setScaledContents (True)
	
        # take another button
        btn = QtGui.QPushButton('New Image From pi', self)
        btn.setToolTip('Press For New vector')
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.takeNew)
        btn.move(50, 50)
        
        #save button
        btn2 = QtGui.QPushButton('save', self)
        btn2.setToolTip('Save vector')
        btn2.resize(btn2.sizeHint())
        btn2.clicked.connect(self.saveImage)
        btn2.move(200, 50)
        
        #next button
        btn3 = QtGui.QPushButton('Back-projected Image', self)
        btn3.setToolTip('Back-projected')
        btn3.resize(btn3.sizeHint())
        btn3.clicked.connect(self.switch)
        btn3.move(300, 50)
        
        #cortical button
        btn4 = QtGui.QPushButton('cortical Image', self)
        btn4.setToolTip('cortical')
        btn4.resize(btn4.sizeHint())
        btn4.clicked.connect(self.switchCort)
        btn4.move(350, 95)
        
        
        #change name
        self.text_name = QLineEdit(self)
        self.text_name.move(60,100)
        #change name button
        btn5 = QtGui.QPushButton('Set new name', self)
        btn5.setToolTip('Press For set name')
        btn5.resize(btn5.sizeHint())
        btn5.clicked.connect(self.showName)
        btn5.move(200, 95)
        
        
        self.setGeometry(500, 500, 850, 650)
        self.setWindowTitle('Retina-with-Pi')
        self.show()
    
    
    
    def setName(self):
        vector_new_name = self.text_name.text()

    def showName(self):
        print(self.text_name.text())
    def newVector(self):
        os.system('sh sendVector.sh')
    
    def loadVector(self):
        #load the vector which generate from the Pi
        V = np.load('tmp/vector.npy')
        cimg = C.cort_img(V)
        cv2.imwrite('tmp/cimg_tmp.jpg',cimg)
    
    def saveImage(self):
        #check the name
        vector_new_name = self.text_name.text()
        vector_new_name = str(vector_new_name)
        print(vector_new_name)
        filename_list = os.listdir(v_save_path)
        num = 1
        while True:
            save_name = vector_new_name+'_' + "{:03n}".format(num)+".npy"
            if save_name in filename_list:
                num = num + 1
            else:
                save_cmd = "mv tmp/vector.npy "+ v_save_path + save_name
                dele_cmd = "rm tmp/cimg_tmp.jpg"
                dele2_cmd ="rm tmp/bck.jpg"
                os.system(save_cmd)
                os.system(dele_cmd)
                os.system(dele2_cmd)
                break
        print('Finish')
    
    def switch(self):
        self.pic.setPixmap(QtGui.QPixmap( "tmp/bck.jpg"))
    def switchCort(self):
        self.pic.setPixmap(QtGui.QPixmap( "tmp/cimg_tmp.jpg"))
    #Image updating
    def takeNew(self):
        self.newVector()
        self.loadVector()
        self.pic.setPixmap(QtGui.QPixmap( "tmp/cimg_tmp.jpg"))
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = retinaGui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
