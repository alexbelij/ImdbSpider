#coding=utf-8
#data cleansing

import csv
#read csv
filename = 'movie2011.csv'
csvfile = file(filename, 'rb')
reader = csv.reader(csvfile)

#data cleansing
newline = []
titleline = ['Film', 'Studio', 'Tomattoes', 'Score', 'Story', 'Genre',
 'Theater', 'Box', 'DomesticGross','ForeignGross', 'WorldGross',
 'Budget', 'Profitability', 'OpenningWeekend']
newline.append(titleline)
for line in reader:
    #pass unitline and titleline
    if line[0].strip() != '' and line[0].strip()!= 'Film':
        newline.append(line[:14])
        
#put averageline on newline[1]
if newline[1][0] != 'Average':
    for line in newline:
        if line[0] == 'Average':
            linecopy = line
            newline.remove(line)
            break
    newline.insert(1,linecopy)

#standardize str
for line in newline:
    line[0] = line[0].capitalize()
    line[1] = line[1].capitalize()
    line[4] = line[4].capitalize()
    line[5] = line[5].capitalize()
    for data in line:
        data.strip()
        
print newline
csvfile.close()

csvfile = file('s'+filename, 'wb')
writer = csv.writer(csvfile)
writer.writerows(newline)
csvfile.close()