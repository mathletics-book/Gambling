#!/usr/bin/env python

import sys
import os
import random
import numpy as np

def play_in(ratings, matchups):

	if np.random.normal(ratings[matchups[0].rsplit(",")[0]]-ratings[matchups[0].rsplit(",")[1]],10)>0:
		p1 = matchups[0].rsplit(',')[0]
	else:
		p1 = matchups[0].rsplit(',')[1]
	if np.random.normal(ratings[matchups[1].rsplit(",")[0]]-ratings[matchups[1].rsplit(",")[1]],10)>0:
        	p2 = matchups[1].rsplit(',')[0]
	else:
        	p2 = matchups[1].rsplit(',')[1]
	if np.random.normal(ratings[matchups[2].rsplit(",")[0]]-ratings[matchups[2].rsplit(",")[1]],10)>0:
        	p3 = matchups[2].rsplit(',')[0]
	else:
        	p3 = matchups[2].rsplit(',')[1]
	if np.random.normal(ratings[matchups[3].rsplit(",")[0]]-ratings[matchups[3].rsplit(",")[1]],10)>0:
        	p4 = matchups[3].rsplit(',')[0]
	else:
        	p4 = matchups[3].rsplit(',')[1]

	return p1,p2,p3,p4

def simulate_region(ratings,matchups):

	if np.random.normal(ratings[matchups[0].rsplit(",")[0]]-ratings[matchups[0].rsplit(",")[1]],10)>0:
                p1 = matchups[0].rsplit(',')[0]
	else:
                p1 = matchups[0].rsplit(',')[1]
	if np.random.normal(ratings[matchups[1].rsplit(",")[0]]-ratings[matchups[1].rsplit(",")[1]],10)>0:
                p2 = matchups[1].rsplit(',')[0]
	else:
                p2 = matchups[1].rsplit(',')[1]
	if np.random.normal(ratings[matchups[2].rsplit(",")[0]]-ratings[matchups[2].rsplit(",")[1]],10)>0:
                p3 = matchups[2].rsplit(',')[0]
	else:
                p3 = matchups[2].rsplit(',')[1]
	if np.random.normal(ratings[matchups[3].rsplit(",")[0]]-ratings[matchups[3].rsplit(",")[1]],10)>0:
                p4 = matchups[3].rsplit(',')[0]
	else:
                p4 = matchups[3].rsplit(',')[1]
	if np.random.normal(ratings[matchups[4].rsplit(",")[0]]-ratings[matchups[4].rsplit(",")[1]],10)>0:
                p5 = matchups[4].rsplit(',')[0]
	else:
                p5 = matchups[4].rsplit(',')[1]
	if np.random.normal(ratings[matchups[5].rsplit(",")[0]]-ratings[matchups[5].rsplit(",")[1]],10)>0:
                p6 = matchups[5].rsplit(',')[0]
	else:
                p6 = matchups[5].rsplit(',')[1]
	if np.random.normal(ratings[matchups[6].rsplit(",")[0]]-ratings[matchups[6].rsplit(",")[1]],10)>0:
                p7 = matchups[6].rsplit(',')[0]
	else:
                p7 = matchups[6].rsplit(',')[1]
	if np.random.normal(ratings[matchups[7].rsplit(",")[0]]-ratings[matchups[7].rsplit(",")[1]],10)>0:
                p8 = matchups[7].rsplit(',')[0]
	else:
                p8 = matchups[7].rsplit(',')[1]
	## round 32
	if np.random.normal(ratings[p1]-ratings[p2],10)>0:
		p9 = p1
	else:
		p9 = p2
	if np.random.normal(ratings[p3]-ratings[p4],10)>0:
                p10 = p3
	else:
                p10 = p4
	if np.random.normal(ratings[p5]-ratings[p6],10)>0:
                p11 = p5
	else:
                p11 = p6
	if np.random.normal(ratings[p7]-ratings[p8],10)>0:
		p12 = p7
	else:
		p12 = p8
	## sweet 16
	if np.random.normal(ratings[p9]-ratings[p10],10)>0:
		p13 = p9
	else:
		p13 = p10
	if np.random.normal(ratings[p11]-ratings[p12],10)>0:
		p14 = p11
	else:
		p14 = p12
	## elite 8
	if np.random.normal(ratings[p13] - ratings[p14],10)>0:
		return p13
	else:
		return p14

f_ratings = open("team_ratings.csv","r")

ratings = dict()

for line in f_ratings:
	linef = line.rstrip().rsplit(",")
	ratings[linef[0]] = float(linef[1])

f_pin = open("playin.csv","r")
matchups = []
for line in f_pin:
	matchups.append(line.rstrip())


pin_winners = play_in(ratings,matchups)

f_east = open("east.csv",'r')
east = []
for line in f_east:
	east.append(line.rstrip())

east_t = [simulate_region(ratings,east) for _ in range(10000)]

f_west = open("west.csv","r")
west = []
for line in f_west:
	west.append(line.rstrip())

west_t = [simulate_region(ratings,west) for _ in range(10000)]

f_midwest = open("midwest.csv","r")
midwest = []
for line in f_midwest:
	midwest.append(line.rstrip())

midwest_t = [simulate_region(ratings,midwest) for _ in range(10000)]

f_south = open("south.csv","r")
south = []
for line in f_south:
	south.append(line.rstrip())

south_t = [simulate_region(ratings,south) for _ in range(10000)]

final_4 = []

for i in range(10000):
	if np.random.normal(ratings[east_t[i]]-ratings[west_t[i]],10)>0:
		f1 = east_t[i]
	else:
		f1 = west_t[i]
	if np.random.normal(ratings[midwest_t[i]]-ratings[south_t[i]],10)>0:
		f2 = midwest_t[i]
	else:
		f2 = south_t[i]
	if np.random.normal(ratings[f1]-ratings[f2],10)>0:
		final_4.append(f1)
	else:
		final_4.append(f2)

print()
print("                Team    WinTitle")
for k in ratings.keys():
        w2 = final_4.count(k)
        print("{:>20s}    {:.2f}".format(k, w2/10000))
