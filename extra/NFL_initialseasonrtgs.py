from scipy.stats import norm
import sys
import os
import pandas as pd
import numpy as np
from scipy import optimize


df = pd.read_csv("hnfl_2023_schedule.csv")
df['playoffs'] = playoffs
dflines = pd.read_csv("NFL_totalwins_betting.csv")
teams = list(dflines["Team"])
col1 = "VisTm"
col2 = "HomeTm"
df['aidx'] = df[col1].apply(lambda x: teams.index(x))
df['hidx'] = df[col2].apply(lambda x: teams.index(x))
reg_season = df[df['Week'] <= 17].copy()

n_teams = 32
home_edge = 2 # this is based on the home edge from Sagarin ratings for the 2022 season

def rtg_constr(x):
    return np.mean(x)

def obj(x):
	err = 0
	reg_season['proj'] = home_edge+reg_season.hidx.apply(lambda i: x[i]) - reg_season.aidx.apply(lambda i: x[i])
	reg_season['hwinpr']=1 - norm.cdf(0.5,reg_season['proj'],14.5)
	reg_season['awinpr'] = 1-reg_season['hwinpr']
	w = np.zeros(shape=n_teams)
	for i in range(len(reg_season)):
		w[teams.index(reg_season[col1][i])] = w[teams.index(reg_season[col1][i])] + reg_season['awinpr'][i]
		w[teams.index(reg_season[col2][i])] = w[teams.index(reg_season[col2][i])] + reg_season['hwinpr'][i]
	err = ((dflines["Line"]-w)**2).sum()
	return err


x0 = np.zeros(shape=n_teams)

res = optimize.minimize(obj,x0, constraints=[{'type':'eq', 'fun':rtg_constr}], method="SLSQP",
                        options={'maxiter':10000})


preseason_ratings = dict()

print(res.success, res.message)
print("                Team   Rating   Line")
for i, t in enumerate(dflines["Team"]):
    print("{:>20s}    {:.2f}    {:.1f}".format(t, res.x[i],dflines["Line"][i]))
    preseason_ratings[t] = res.x[i]
