import cv2
from retinavision.retina import Retina
from retinavision.cortex import Cortex
from retinavision import datadir, utils
from os.path import join
import datetime

beforeTime = datetime.datetime.now()
# Create and load retina
R = Retina(gpu=False)
R.info()
R.loadLoc(join(datadir, "retinas", "ret50k_loc.pkl"))
R.loadCoeff(join(datadir, "retinas", "ret50k_coeff.pkl"))
# R.loadLoc(join(datadir, "retinas", "8k_loc.pkl"))
# R.loadCoeff(join(datadir, "retinas", "8k_coeff.pkl"))
# Create and prepare cortex
C = Cortex(gpu=False)
lp = join(datadir, "cortices", "50k_Lloc_tight.pkl")
rp = join(datadir, "cortices", "50k_Rloc_tight.pkl")
# lp = join(datadir, "cortices", "8k_cort_leftloc.pkl")
# rp = join(datadir, "cortices", "8k_cort_rightloc.pkl")
C.loadLocs(lp, rp)
C.loadCoeffs(join(datadir, "cortices", "50k_Lcoeff_tight.pkl"),join(datadir, "cortices", "50k_Rcoeff_tight.pkl"))
# C.loadCoeffs(join(datadir, "cortices", "8k_cort_leftcoeff.pkl"),
#              join(datadir, "cortices", "8k_cort_rightcoeff.pkl"))

# fixation=None
cap = cv2.VideoCapture(0)  # cap is the capture object (global)
ret, campic = cap.read()

# Prepare retina
x = campic.shape[1] / 2
y = campic.shape[0] / 2

fixation = (y, x)
R.prepare(campic.shape, fixation)
afterTime = datetime.datetime.now()
print (afterTime - beforeTime).seconds

