import numpy as np
import cv2
from os.path import join
import os
from retinavision.retina import Retina
from retinavision.cortex import Cortex
from retinavision import datadir, utils

R = Retina(gpu=False)
R.info()
R.loadLoc(join(datadir, "retinas", "ret50k_loc.pkl"))
R.loadCoeff(join(datadir, "retinas", "ret50k_coeff.pkl"))

#open cap and set resolution as 1280*720, the default is 640*320 which
#is too small for 50k node, so, we need change the resolution
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


ret, campic = cap.read()
x = campic.shape[1] / 2
y = campic.shape[0] / 2
fixation = (y, x)
R.prepare(campic.shape, fixation)
ret, img = cap.read()
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
V = R.sample(img,fixation)
#back project
tight = R.backproject_last()
tight = cv2.cvtColor(tight, cv2.COLOR_BGR2RGB)
cv2.imwrite("tight.jpg", tight)
#cortex
C = Cortex(gpu=False)
lp = join(datadir, "cortices", "50k_Lloc_tight.pkl")
rp = join(datadir, "cortices", "50k_Rloc_tight.pkl")
C.loadLocs(lp, rp)
C.loadCoeffs(join(datadir, "cortices", "50k_Lcoeff_tight.pkl"),join(datadir, "cortices", "50k_Rcoeff_tight.pkl"))
cimg = C.cort_img(V)
cimg = cv2.cvtColor(cimg, cv2.COLOR_BGR2RGB)
cv2.imwrite("cimg.jpg", cimg)
