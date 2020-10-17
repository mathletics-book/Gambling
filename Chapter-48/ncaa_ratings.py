# http://warrennolan.com/basketball/2019/rpi-live
rpi = []
team_rpi = []

f = open("rpi19.csv","r")

for l in f:
	try:
		rpi.append(int(l.rstrip()))
	except:
		team_rpi.append(l.rstrip())

f = open("net19.csv","r")
ranks = []
for l in f:
	lf = l.rstrip().rsplit(",")
	ranks.append((int(lf[2]),rpi[team_rpi.index(lf[0])]))


from scipy.stats import spearmanr
c=[]
cmean = []
for r in [10,25,50,100,200,300,353]:
	c.append(spearmanr(arank[0:r,1],arank[0:r,0])[0])
	cmean.append(np.mean(abs(arank[0:r,1]-arank[0:r,0]))/r)
