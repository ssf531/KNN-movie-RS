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

gclass = {}
with open('genre.csv', 'r') as readfile:
	rows = csv.reader(readfile, delimiter = ',')
	for row in rows:
		gclass[row[1]] = row[0]
		
moviename = {}
with open('names.csv', 'r', encoding='latin-1') as readfile:
	rows = csv.reader(readfile, delimiter = ',')
	for row in rows:
		moviename[row[0]] = row[1]
			
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
	j = inter/(len(s1)+len(s2)-inter)
	return 1-j
	
	

def corr():
	pass

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

def main(user, movie):
	knn = 5
	w1 = 0
	w2 = 0.5
	
	ratings = {}
	with open('out.csv', 'r') as readfile:
		rows = csv.reader(readfile, delimiter = ',')
		for row in rows:
			if int(row[0]) < user: continue
			elif int(row[0]) == user:
				ratings[row[1]] = float(row[2])/2
			else: break
	
	# for r in ratings:
		# print(r)
	
	with open('usermovie.csv', 'r') as readfile:
		rows = csv.reader(readfile, delimiter = ',')
		for row in rows:
			uid = row[0]
			if int(uid) != user: continue
			ans = row[1:].index(str(movie))+1
			temp = [99 for x in range(len(row))] # distance vector
			mov = [x for x in range(1,len(row))] # generalize
			mov.remove(ans)
			for i in mov:
				temp[i] = distance(row[ans], row[i], w1, w2)
			
			zzz = sorted(range(len(temp)), key=lambda k: temp[k])[:knn]
			
			nn = set(row[x] for x in zzz)
			id = row[ans] # movie to predict
				
			print("%s has a predicted rating of %.1f stars based on the ratings you gave for the %d most similar movies in the past." % (moviename[id], ratings[id], knn))
			print("It was released in year %d and has genres:" % year[id])
			genrecount = []
			for p in genres[id]:
				print("-", gclass[p])
				count = 0
				for n in nn:
					for g in genres[n]:
						if gclass[g] == gclass[p]: count += 1
				genrecount.append((gclass[p], count))
			
			print("Of these %d most similar movies," % knn)
			output = sorted(genrecount, key=lambda x: x[-1], reverse=True)
			gc = [[] for x in range(6)]
			for o in output:
				if o[1] > 0.5*knn:
					gc[o[1]].append(o[0])
					print("%d were of genre %s" % (o[1], o[0]))
			year0, year2, year5 = 0, 0, 0
			print("and")
			for n in nn:
				if year[n] == year[id]: year0 += 1
				if abs(year[n]-year[id]) < 2: year2 += 1
				if abs(year[n]-year[id]) < 5: year5 += 1
			if year0 > 0.5*knn: print("%d were relased in the same year." % year0)
			elif year2 > 0.5*knn: print("%d were relased within 2 years." % year2)
			elif year5 > 0.5*knn: print("%d were relased within 5 years." % year5)
			
			
				
				
			break


	# with open('predict.txt', 'w') as tf:
		# tf.write(. E.g. movieX was rated 4 stars and
# is 0.85 similar and movieY was rated 3.2 and has a
# similarity of 0.7.")

	
# main(1, 481)
#main(123100, 34583)
main(4,33679)