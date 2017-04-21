import numpy as np
import csv
import math
import matplotlib.pyplot as plt

matchl = 0
matchr = 0
tsvfile = open('training_granted.tsv','r')
tsvreader = csv.reader(tsvfile,delimiter = '\t')

lx,ly,rx,ry = [],[],[],[]

for line in tsvreader:
	if(line[0] == 'time'):
		temp = 0
	elif(line[1] == 'MSG'):
		break
	elif(line[1] == 'nan' or line[2] == 'nan' or line[4] == 'nan' or line[5] == 'nan'):
		temp = 0
	else:
		lx.append(line[1])
		ly.append(line[2])
		rx.append(line[4])
		ry.append(line[5])

tsvfile = open('test_granted.tsv','r')
tsvreader = csv.reader(tsvfile,delimiter = '\t')

lax,lay,rax,ray = [],[],[],[]

for line in tsvreader:
	if(line[0] == 'time'):
		temp = 0
	elif(line[1] == 'MSG'):
		break
	elif(line[1] == 'nan' or line[2] == 'nan' or line[4] == 'nan' or line[5] == 'nan'):
		temp = 0
	else:
		lax.append(line[1])
		lay.append(line[2])
		rax.append(line[4])
		ray.append(line[5])


def d(m,x,y,const):
	dist = (m*x-y+const)/(math.sqrt(m**2+1)) + 0.001
	return(dist)

def areacheck(x1,y1,x2,y2,x0,y0):  # make sure these values are in float
	x1 = float(x1)
	y1 = float(y1)
	x2 = float(x2)
	y2 = float(y2)
	x0 = float(x0)
	y0 = float(y0)
	out = 1
	m = (y1-y2+0.001)/(x1-x2+0.001)
	m1 = (-1)/m
	const1 = y1-m1*x1
	const2 = y2-m1*x2
	const = y1-m*x1
	dis = d(m,x0,y0,const)
	dis1 = d(m1,x0,y0,const1)
	dis2 = d(m1,x0,y0,const2)
	if(abs(dis) >= 5):
		out = 0
	elif ((dis1/(abs(dis1))) == (dis2/(abs(dis2))) and dis1 != 0.001 and dis != 0.001):
		out = 0
	return out

if (len(lax) <= 0.8*len(lx)):
	print 'not able to properly scan the path for left eye (check the lighting conditions)'

else:
	last = 0
	for i in range(0,len(lax)):
		count = 0
		while (count < 5):
			lol = areacheck(lx[last],ly[last],lx[last+1],ly[last+1],lax[i],lay[i])
			if (lol == 1):
				matchl = matchl + 1
				last = last + count
				break
			count = count + 1


if (len(rax) <= 0.8*len(rx)):
	print 'not able to properly scan the path for right eye (check the lighting conditions)'

else:
	last = 0
	for i in range(0,len(rax)):
		count = 0
		while (count < 5):
			lol = areacheck(rx[last],ry[last],rx[last+1],ry[last+1],rax[i],ray[i])
			if (lol == 1):
				matchr = matchr + 1
				last = last + count
				break
			count = count + 1


if ((matchl + matchr) >= 0.5*(len(lx)+len(rx))):
	print 'Access Granted'
else:
	print 'Access Denied'

print float(matchl+matchr)/float(len(lax)+len(rax))*100,'percent matched'