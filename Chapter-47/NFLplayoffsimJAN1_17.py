#!/usr/bin/env python

import sys
import os
import random
import numpy as np

home_edge = 3

afc = ["NE","KC","PIT","HOU","OAK","MIA"]
nfc = ["DAL","ATL","SEA","GB","NYG","DET"]

rating = {"DAL":6.97, "ATL":8.48, "SEA":2.13, "GB":2.83, "NYG":2.13, "DET":-1.4, "NE":9.29, "KC":5.6,"PIT":4.74,"HOU":-2.63,"OAK":-3.74,"MIA":-2.4}

afc_champ = []
nfc_champ = []
super_bowl = []


for i in range(100000):
	#wild card games
	m = "OAK HOU"
	if np.random.normal(home_edge+rating[m.rsplit(" ")[1]]-rating[m.rsplit(" ")[0]],14)>0:
                w11 = m.split()[1]
	else:
                w11 = m.split()[0]
	m = "MIA PIT"
	if np.random.normal(home_edge+rating[m.rsplit(" ")[1]]-rating[m.rsplit(" ")[0]],14)>0:
                w12 = m.split()[1]
	else:
                w12 = m.split()[0]
	m = "NYG GB"
	if np.random.normal(home_edge+rating[m.rsplit(" ")[1]]-rating[m.rsplit(" ")[0]],14)>0:
                w13 = m.split()[1]
	else:
                w13 = m.split()[0]
	m = "DET SEA"
	if np.random.normal(home_edge+rating[m.rsplit(" ")[1]]-rating[m.rsplit(" ")[0]],14)>0:
                w14 = m.split()[1]
	else:
                w14 = m.split()[0]
	#divisional round
	#AFC
	if afc.index(w11) < afc.index(w12):
		m1 = w12+" NE"
		m2 = w11+" KC"
	else:
		m1 = w11+" NE"
		m2 = w12+" KC"
	if np.random.normal(home_edge+rating[m1.rsplit(" ")[1]]-rating[m1.rsplit(" ")[0]],14)>0:
                w21 = m1.split()[1]
	else:
                w21 = m1.split()[0]
	if np.random.normal(home_edge+rating[m2.rsplit(" ")[1]]-rating[m2.rsplit(" ")[0]],14)>0:
                w22 = m2.split()[1]
	else:
                w22 = m2.split()[0]
	#NFC 
	if nfc.index(w13) < nfc.index(w14):
                m1 = w14+" DAL"
                m2 = w13+" ATL"
	else:
                m1 = w13+" DAL"
                m2 = w14+" ATL"
	if np.random.normal(home_edge+rating[m1.rsplit(" ")[1]]-rating[m1.rsplit(" ")[0]],14)>0:
                w23 = m1.split()[1]
	else:
                w23 = m1.split()[0]
	if np.random.normal(home_edge+rating[m2.rsplit(" ")[1]]-rating[m2.rsplit(" ")[0]],14)>0:
                w24 = m2.split()[1]
	else:
                w24 = m2.split()[0]
	#conference round
	#AFC 
	if afc.index(w21) > afc.index(w22):
		m = w21+" "+w22
	else:
		m = w22+" "+w21
	if np.random.normal(home_edge+rating[m.rsplit(" ")[1]]-rating[m.rsplit(" ")[0]],14)>0:
		afc_champ.append(m.split()[1])
	else:
		afc_champ.append(m.split()[0])
	#NFC
	if nfc.index(w23) > nfc.index(w24):
                m = w23+" "+w24
	else:
                m = w24+" "+w23
	if np.random.normal(home_edge+rating[m.rsplit(" ")[1]]-rating[m.rsplit(" ")[0]],14)>0:
		nfc_champ.append(m.split()[1])
	else:
		nfc_champ.append(m.split()[0])
	#super bowl
	m = afc_champ[-1]+" "+nfc_champ[-1]
	if np.random.normal(rating[m.rsplit(" ")[1]]-rating[m.rsplit(" ")[0]],14)>0:
                super_bowl.append(m.split()[1])
	else:
                super_bowl.append(m.split()[0])


print()
print("                Team   MakeSB    WinSB")
for k in rating.keys():
        w1 = max(afc_champ.count(k),nfc_champ.count(k))
        w2 = super_bowl.count(k)
        print("{:>20s}    {:.2f}      {:.2f}".format(k, w1/100000, w2/100000))

