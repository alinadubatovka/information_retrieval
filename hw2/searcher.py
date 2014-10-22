#coding: utf-8

import sys


index_path = sys.argv[1]


def readIndex(path):
	index = dict()
	inp = open(path, "r", encoding = "utf-8")
	
	while True:
		row = inp.readline()
		if not row:
			break
		word, docs = row[0:-1:].split(":")
		index[word] = dict()
		for doc in docs.split(";"):
			if not doc:
				continue
			filename, positions = doc.split("|")
			index[word][filename] = positions.split()

	return index


index = readIndex(index_path)


def incorrectQuery():
	print("incorrect query")
	return ("IQ")
	

def queryParse(query):
	q = query.replace("(", "").replace(")", "")

	cntAnd = q.count("AND")
	cntOr = q.count("OR")
	if cntAnd * cntOr:
		#print("queryParse")
		return incorrectQuery()
	if not (cntAnd + cntOr):
		return ([q], "AND")

	words = list()
	queryType = "AND" if cntAnd else "OR"
	
	words = q.split(" " + queryType + " ")
	#for i in range(len(q)):
		#if i % 2 and q[i] != queryType:
		#	return (list(), incorrectQuery())
		#words.append(q[i])
		
	return (words, queryType)


def getDocuments(word):
	if index.get(word) == None:
		return set()
	else:
		return index[word]


def	intersectPoslists(list1, list2, dist):
	i = 0
	j = 0
	while i < len(list1):
		while j < len(list2):
			#print(i, j, int(list1[i]), int(list2[j]), dist)
			if int(list2[j]) > int(list1[i]) + dist:
				break
			if int(list2[j]) >= int(list1[i]):
				return True
			j += 1
		i += 1
	return False


def intersectDocsets(word1, word2, dist):
	sign = 0 if dist.isnumeric() else (1 if int(dist) > 0 else -1)
	dist = abs(int(dist))

	doc1 = getDocuments(word1)
	doc2 = getDocuments(word2)
	
	if not doc1 or not doc2:
		return set()

	res = set()
	for doc in (doc1.keys() & doc2.keys()):
		is_good = False
		if sign == 1:
			is_good = intersectPoslists(doc1[doc], doc2[doc], dist)	
		elif sign == -1:
			#print(-1)
			is_good = intersectPoslists(doc2[doc], doc1[doc], dist)	
		else:
			is_good = intersectPoslists(doc1[doc], doc2[doc], dist) or intersectPoslists(doc2[doc], doc1[doc], dist)
		
		if is_good:
			res.add(doc)
	return res


def subqueryProcess(subquery):
	#print("subqueryProcess")
	#print(subquery)
	tokens = subquery.split()
	if not len(tokens) % 2:
		#print("subqueryProcess")
		#print("len % 2 == 0")
		return incorrectQuery()
	
	#print(tokens)
	sets = getDocuments(tokens[0]).keys()
	for i in range(1, len(tokens)):
		if not sets:
			break
		if i % 2: 
			if "/" not in tokens[i]:
				#print("subqueryProcess")
				#print("tokens[2 * k + 1] doesn't contain /")
				return incorrectQuery()
		else:
			sets &= set(intersectDocsets(tokens[i - 2], tokens[i], tokens[i - 1].replace("/", "")))
		
	return sets


def search(subresults, queryType):
	result = set(subresults[0])
	if queryType == "OR":
		for subres in subresults:
			if not subres:           
				continue
			result |= subres
	
	if queryType == "AND":
		if not result:
			return set()
		for subres in subresults:
			if not subres:
				return set()
			result &= set(subres)
	
	return result


def printResult(result):
	#print(result)
	if not result:
		print("no documents found")
	else:
		print("found " + ", ".join(list(result)[:2:]) + ((" and %d more" % (len(result) - 2)) if len(result) > 2 else ""))


while True:
	query = input()
	subqueries, queryType = queryParse(query)
	#print(subqueries)
	
	if queryType == "IQ":
		continue

	subresults = [subqueryProcess(subquery) for subquery in subqueries]
	if "IQ" in subresults:
		continue

	result = search(subresults, queryType)
	printResult(result)