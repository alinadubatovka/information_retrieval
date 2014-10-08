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
		word, docs = row.split(":")
		if index.get(word) == None:	
			index[word] = set()
		for doc in docs.split():
			index[word].add(doc)

	return index


index = readIndex(index_path)


def incorrectQuery():
	print("incorrect query")
	return (set(), "IQ")
	

def queryProcess(query):
	q = query.replace("(", "").replace(")", "").split()

	if len(q) == 1:
		return(q, "AND")	

	cntAnd = q.count("AND")
	cntOr = q.count("OR")
	if cntAnd * cntOr:
		return incorrectQuery()
	if not cntAnd + cntOr:
		return incorrectQuery()

	words = list()
	queryType = "AND" if cntAnd else "OR"
	for i in range(len(q)):
		if i % 2 and q[i] != queryType:
			return incorrectQuery()	
		words.append(q[i])
		
	return (words[::2], queryType)


def search(words, queryType):
	if queryType == "OR":
		result = set()
		for word in words:
			if index.get(word) == None:
				continue
			result |= index[word]
	
	if queryType == "AND":
		if index.get(words[0]) == None:
			return set()
		result = index[words[0]].copy()
		for word in words:
			if index.get(word) == None:
				return set()
			result &= index[word]
	
	return result


def printResult(result):
	if not result:
		print("no documents found")
	else:
		print("found " + ", ".join(list(result)[:2:]) + ((" and %d more" % (len(result) - 2)) if len(result) > 2 else ""))


while True:
	query = input()
	words, queryType = queryProcess(query)
	if queryType == "IQ":
		continue
	result = search(words, queryType)
	printResult(result)