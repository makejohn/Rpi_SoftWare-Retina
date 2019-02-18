import numpy as np
import cv2
from os.path import join
import os
from retinavision.retina import Retina
from retinavision import datadir, utils
from sys import argv

#set laptop host name and path
HOST_NAME = argv[1]
TMP_PATH = argv[2]

SCP_PATH = HOST_NAME + ":" + TMP_PATH

#print(SCP_PATH)


#save vector as vector.npy
def saveVector():
        np.save('vector',V)
        tight = R.backproject_last()
        cv2.imwrite('bck.jpg',tight)
	#sent to laptop
        scp_cmd = 'scp -p vector.npy '+SCP_PATH
        scp_cmd_img = 'scp -p bck.jpg '+SCP_PATH
	#scp_cmd_fixation = 'scp - p fixation '+SCP_PATH
        os.system(scp_cmd)
        os.system(scp_cmd_img)
	#delete vector.npy
        os.system('rm *vector.npy')
        os.system('rm bck.jpg')


#open cap and set resolution as 1280*720, the default is 640*320 which
#is too small for 50k node, so, we need change the resolution
cap = utils.camopen()
#count time
#project_start = datetime.datetime.now()
ret, campic = cap.read()

R = Retina(gpu=False)
R.info()
R.loadLoc(join(datadir, "retinas", "ret50k_loc.pkl"))
R.loadCoeff(join(datadir, "retinas", "ret50k_coeff.pkl"))

##prepare
x = campic.shape[1] / 2
y = campic.shape[0] / 2
fixation = (y, x)
R.prepare(campic.shape, fixation)

ret, img = cap.read()
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
V = R.sample(img,fixation)
saveVector()
