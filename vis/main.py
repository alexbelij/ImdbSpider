#coding=utf-8
import numpy as np
from numpy import asarray
import matplotlib.pyplot as plt
import csv
from functools import reduce
import math
def char2num(c):
    return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[c]

def str2float(s):
    s1 = s.split('.')[0]
    try:
        s2 = s.split('.')[1]
    except IndexError as e:
        s2 = '0'
    return reduce(lambda x,y: x*10+y, map(char2num, s1))+reduce(lambda x,y: x/10.0+y, map(char2num, s2[::-1]))/10.0

#read csv    
def readcsv(filename):
    csvfile = file(filename, 'rb')
    reader = csv.reader(csvfile)

    #data loading
    data = []
    for line in reader:
        #delete title and 
        if reader.line_num == 1:
            continue
        data.append(line)
    csvfile.close()

    return data

def b_s(datar):
    #data filtering
    dtr = datar[:]
    del(dtr[0])
    for line in dtr:
        try:
            line[3] = int(line[3])
            line[-1] = str2float(line[-1])
        except ValueError as e:
            dtr.remove(line)
    #numpy array building
    score = []
    box = []
    for line in dtr:
        score.append(line[3])
        box.append(line[-1])
    score = np.array(score, int)
    box = np.array(box, float)
    return score, box
    
    
data2011 = readcsv('data.csv')

def boxScore():
    #Opening Weekend  Box Office - Audience Score: Scatter Plot

    s,b = b_s(data2011)
    T = ((b/10.0)**2+s**2)**0.5
    plt.scatter(s,b, s=75, c = T, alpha=.5)
    plt.xlabel('Audience Score')
    plt.ylabel('Openning Weekend/$m')
    plt.title('Box Office in Opening Weekend - Audience Score:2007')
    plt.ylim(-10,b.max()*1.1)
    plt.xlim(s.min()-2, s.max()+2)

    nicemovie = []
    for x in s:
        md = {}
        if x >s.max()*0.9:
            itemindex = np.argwhere(s == x)[0][0]
            if b[itemindex]>b.max()*0.9:
                md['score'] = s[itemindex]
                md['box'] = b[itemindex]
                md['name'] = data2011[itemindex+1][0]
                nicemovie.append(md)

    if len(nicemovie) != 0:
        dmovie = nicemovie[0]
        if len(nicemovie)>1:
            dis = 0
            for x in nicemovie:
                temp = x['score']*x['score']+x['box']*x['box']
                if temp>dis:
                    dis = temp
                    dmovie = x

                
        plt.annotate(dmovie['name'],
                    xy=(dmovie['score'], dmovie['box']), xycoords='data',
                    xytext=(-200, 10), textcoords='offset points', fontsize=12,
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
                
    plt.show()
    '''

    '''
    studio = []
    sdata = data2011[1:]
    for line in sdata:
        if line[1] == '':
            sdata.remove(line)
        if line[1].find('fox')!=-1:
            line[1] = 'Fox'
        if line[1].find('Warner')!=-1:
            line[1] = 'Warner bros'
        if line[1].find('Dreamworks')!=-1:
            line[1] = 'Dreamworks'
        if line[1].find('Relativity')!=-1:
            line[1] = 'Relativity'
        if line[1].find('Happy')!=-1:
            line[1] = 'Happy madison'
        if line[1].find('Sony')!=-1:
            line[1] = 'Sony'
            
    csvdata = []        
    for line in sdata:
        studio.append(line[1])
        csvdata.append(line[1].replace(' ', ''))


    csvfile = file('s11', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(csvdata)
    csvfile.close()
        
    wd = {}
    for x in studio:
        if wd.has_key(x):
            wd[x] += 1
        else:
            wd[x] = 1
    print wd

    xmax = 0
    for x in wd:
        if wd[x]>xmax:
            xmax = wd[x]
    print xmax    
    ang = 0
    for n in wd:
        x = 0.5 + np.cos(ang)*0.3/(math.log(wd[n]+1))
        y = 0.5 + np.sin(ang)*0.4/(math.log(wd[n]+1))
        ang += np.pi/7.0
        if x > 0.9:
            x = 0.9
        if y > 0.9:
            y = 0.9
        plt.text(x, y, n, ha='center', va='center', color="#15555c", alpha=1-0.5/math.log(wd[n]+1),
                transform=plt.gca().transAxes, fontsize=10+ 10*int((math.log(wd[n]+1))), clip_on=True)

    plt.xticks([]), plt.yticks([])             
    # savefig('../figures/text_ex.png',dpi=48)
    plt.show()

def genre():
    #Genre Radar Plot

    #load data
    d = []
    for l in data2011:
        temp = []
        temp.append(l[1])    
        temp.append(int(l[0]))
        temp.append(str2float(l[2]))
        temp.append(str2float(l[3].replace(',','')))
        temp.append(str2float(l[4]))
        temp.append(str2float(l[5].replace('%', '')))
        d.append(temp)

    dd = {}
    for line in d:
        if dd.has_key(line[0]):
            dd[line[0]].append(line[1:])
            
        else:
            dd[line[0]] = []
            dd[line[0]].append(line[1:])
    

    #cal average
    for x in dd:
        l = [0,0,0,0,0]
        n = 0
        for line in dd[x]:
            l[0]=line[0]
            l[1]= line[1] 
            l[2]= line[2]
            l[3]= line[3]
            l[4]= line[4]
            n+=1
        dd[x] = []
        for y in l:
            dd[x].append(y/(n*1.0))
        
    maxd = []
    mind = []
    mn = []
    for x in dd:
        m = 0
        n = 100000
        for y in dd[x]:
            if y>m:
                m = y
            if y<n:
                n = y
        maxd.append(m)
        mind.append(n)
        mn.append(m-n)
    print maxd,mind

    aa = []
    for x in dd:
        aa.append(x)

    labels = np.array(['Score', 'Domestic Gross', 'Foreign Gross', 'Budget', 'Profitability'])
    dataLenth = 5
    data = np.array([0.350993377,0.303445498,0.314033565,0.5393018,0.004135868])
    #========自己设置结束============

    angles = np.linspace(0, 2*np.pi, dataLenth, endpoint=False)
    data = np.concatenate((data, [data[0]])) # 闭合
    angles = np.concatenate((angles, [angles[0]])) # 闭合

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)# polar参数！！
    ax.plot(angles, data, 'bo-', linewidth=2)# 画线
    ax.fill(angles, data, facecolor='g', alpha=0.25)# 填充
    ax.set_thetagrids(angles * 180/np.pi, labels,)
    ax.set_title('Crime', va='bottom',)
    ax.set_rlim(0,1)
    ax.grid(True)
    plt.show()
    #for line in data2011:
    #    if not d.has_key(line[5]):
    #        d[line[5]] = []
    #        d[line[5]].append(list(int(line[3]),str2float(line[8]),str2float(line[9]),str2float(line[11]),str2float(line[12].replace('%', ''))))