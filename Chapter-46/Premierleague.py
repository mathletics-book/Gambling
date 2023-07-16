import pandas as pd
import numpy as np
import scipy
from math import log
from scipy.stats import skellam
from scipy import optimize

df = pd.read_csv("PL2012-13.csv")

teams = list(set(df.HomeTeam.unique()) & set(df.AwayTeam.unique()))


# create indices that will be handy for the optimization 

df['hidx'] = df.HomeTeam.apply(lambda x: teams.index(x))
df['aidx'] = df.AwayTeam.apply(lambda x: teams.index(x))
df['xhdefidx'] = df.hidx + len(teams)
df['xhoffidx'] = df.hidx
df['xadefidx'] = df.aidx + len(teams)
df['xaoffidx'] = df.aidx

n_teams = len(teams)
ghome = n_teams*2
gaway = n_teams*2+1

def off_constr(x):
    return np.mean(x[:n_teams]) - 1

def def_constr(x):
    return np.mean(x[n_teams:n_teams*2]) - 1

def obj(x):
    err = ((df['HomeGoals'] - x[ghome] * df.xhoffidx.apply(lambda i: x[i]) * df.xadefidx.apply(lambda i: x[i]))**2).sum()
    err += ((df['AwayGoals'] - x[gaway] * df.xaoffidx.apply(lambda i: x[i]) * df.xhdefidx.apply(lambda i: x[i]))**2).sum()
    return err


x0 = np.random.random(size=len(teams)*2 + 2)

res = optimize.minimize(obj, x0, constraints=[{'type':'eq', 'fun':off_constr}, {'type':'eq', 'fun':def_constr}],
                        options={'maxiter':300})
res.success, res.message

print("Home average points: {:.3f}".format(res.x[ghome]))
print("Away average points: {:.3f}".format(res.x[gaway]))
print()
print("                Team   Off Rate    Def Rate")
for i, t in enumerate(teams):
    print("{:>20s}    {:.2f}      {:.2f}".format(t, res.x[i], res.x[i+n_teams]))

### make predictions

print("=====================================")
print("Chelsea @ Reading")
chelsea = teams.index("Chelsea")
reading = teams.index("Reading")

xG_chelsea = res.x[gaway]*res.x[chelsea]*res.x[reading+n_teams]
xG_reading = res.x[ghome]*res.x[reading]*res.x[chelsea+n_teams]
print(" ")
print("{:>20s}    {:.2f}".format("Expected Goals for Reading: ",xG_reading))
print("{:>20s}    {:.2f}".format("Expected Goals for Chelsea: ",xG_chelsea))
print(" ")

## simulate the game 10000 times 
s_reading = np.random.poisson(xG_reading, 10000)
s_chelsea = np.random.poisson(xG_chelsea, 10000)

print("{:>10s}    {:.2f}".format("Probability Reading wins: ",sum([1 for i in range(10000) if s_reading[i] > s_chelsea[i]])/10000))
print("{:>10s}    {:.2f}".format("Probability Chelsea wins: ",sum([1 for i in range(10000) if s_reading[i] < s_chelsea[i]])/10000))
print("{:>10s}    {:.2f}".format("Probability of a draw: ",sum([1 for i in range(10000) if s_reading[i] == s_chelsea[i]])/10000))


print("=====================================")
print("Skellam regression")

def obj_skellam(x):
    err = (skellam.pmf(df['HomeGoals']-df['AwayGoals'],x[ghome] * df.xhoffidx.apply(lambda i: x[i]) * df.xadefidx.apply(lambda i: x[i]),x[gaway] * df.xaoffidx.apply(lambda i: x[i]) * df.xhdefidx.apply(lambda i: x[i])))
    logerr = np.array([log(i) for i in list(err)]).sum()
    return -logerr

x0 = np.ones(len(teams)*2 + 2)

res = optimize.minimize(obj_skellam, x0, options={'maxiter':3})

res.success, res.message

print()
print("                Team   Off Rate    Def Rate")
for i, t in enumerate(teams):
    print("{:>20s}    {:.2f}      {:.2f}".format(t, res.x[i], res.x[i+n_teams]))

