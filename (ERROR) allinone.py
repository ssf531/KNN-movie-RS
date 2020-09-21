import os, csv, math

predict = {}
knndict = {}

def writecsv(csv_title, csv_content):
	with open(csv_title, 'w', newline='', encoding='latin-1') as writefile:
		w = csv.writer(writefile)
		w.writerows(csv_content)

year, genres = {}, {}
with open('parser.csv', 'r') as readfile:
	rows = csv.reader(readfile, delimiter = ',')
	for row in rows:
		genres[row[0]] = row[2:]
		year[row[0]] = int(row[1])
		
def jaccard(list1, list2): # 0 = no distance (most similar), 1 = max distance
	s1 = set(list1)
	s2 = set(list2)
	inter = len(s1.intersection(s2))
	j = inter/(len(s1)+len(s2)-inter)
	return 1-j

def distance(id1, id2, yearweight, genreweight):
	yeardif = abs(year[id1] - year[id2])
	yearsq = (year[id1] - year[id2])**2
	genredif = jaccard(genres[id1], genres[id2])
	return yeardif + genredif

def main(knn):
	with open('usermovie.csv', 'r') as readfile:
		rows = csv.reader(readfile, delimiter = ',')
		for row in rows:
			uid = row[0]
			temp = [99 for x in range(len(row))] # distance vector
			for i in range(2, len(row)):
				temp[i] = distance(row[1], row[i])
			
			zzz = sorted(range(len(temp)), key=lambda k: temp[k])[:knn]
			knndict[str(uid)] = set(row[x] for x in zzz)
			predict[str(uid)] = row[1]
			
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
	writecsv('%sNN.csv' % (knn), [[mean, std]])
	
for knn in range(1,11):
	main(knn)