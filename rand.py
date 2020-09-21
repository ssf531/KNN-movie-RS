import os, csv, math, random

predict = {}
knndict = {}

def writecsv(csv_title, csv_content, append=False):
	if append:
		with open(csv_title, 'a', newline='') as writefile:
			w = csv.writer(writefile)
			w.writerows(csv_content)	
	else:
		with open(csv_title, 'w', newline='') as writefile:
			w = csv.writer(writefile)
			w.writerows(csv_content)

year, genres = {}, {}
with open('parser.csv', 'r') as readfile:
	rows = csv.reader(readfile, delimiter = ',')
	for row in rows:
		genres[row[0]] = [x for x in row[2:] if x != ""]
		year[row[0]] = int(row[1])
		
def jaccard(list1, list2): # 0 = no distance (most similar), 1 = max distance

	s1 = set(list1)
	s2 = set(list2)
	inter = len(s1.intersection(s2))
	try: 
		j = inter/(len(s1)+len(s2)-inter)
		return 1-j
	except:
		return 0

# hamming
# simple matching coefficient
# rand index
# sorensen index
# tversky index
# 
	
def distance(id1, id2, yw, y2w):
	yeardif = abs(year[id1] - year[id2])
	yearsq = abs(year[id1] - year[id2])**0.5
	genredif = jaccard(genres[id1], genres[id2])
	return yw*yeardif + y2w*yearsq + genredif

def main(knn, w1, w2, s=1):
	random.seed(s)
	with open('usermovie.csv', 'r') as readfile:
		rows = csv.reader(readfile, delimiter = ',')
		for row in rows:
			train = random.randint(1, len(row)-1)
			uid = row[0]
			temp = [99 for x in range(len(row))] # distance vector
			mov = [x for x in range(1,len(row))] # generalize
			mov.remove(train)
			for i in mov:
				temp[i] = distance(row[train], row[i], w1, w2)
			
			zzz = sorted(range(len(temp)), key=lambda k: temp[k])[:knn]
			knndict[str(uid)] = set(row[x] for x in zzz)
			predict[str(uid)] = row[train]
			
	lenauthor = 283228
	predout = [[] for x in range(lenauthor+1)]
	nnout = [[] for x in range(lenauthor+1)]
	nn = []
	with open('out.csv', 'r') as readfile:
		rows = csv.reader(readfile, delimiter = ',')
		for row in rows:
			if row[0] not in predict: continue
			if row[1] == predict[row[0]]:
				predout[int(row[0])].append(row[2])
			if row[1] in knndict[row[0]]:
				nnout[int(row[0])].append(row[2])

	#######################################333			
			
	nnout2 = []
	predout2 = []

	for row in nnout:
		if len(row) == 0: continue
		num = 0
		for r in row:
			num += int(r)
		nnout2.append(num/knn)

	nnout = [] # clear memory

	for row in predout:
		if len(row) == 0: continue
		predout2.append(int(row[0]))
	predout = [] # clear memory
	
	
	out = []
	for i in range(len(predout2)):
		out.append(nnout2[i] - predout2[i])
	nnout2 = []; predout2 = [] # clear memory
		
	"""
	"""

	mean = sum(out) / len(out)   # mean
	var  = sum(pow(x-mean,2) for x in out) / len(out)  # variance
	std  = math.sqrt(var)  # standard deviation
	out = [] # clear memory
	writecsv('%d.csv' % s, [['%d_1:%f:%f' % (knn,w1,w2), mean, std]], append=True)
	
for knn in range(5,8):
	for yy in [0]:
		for yy2 in [0.5, 1.0]:
			main(knn, yy, yy2, 1234)