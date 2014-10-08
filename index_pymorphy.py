#coding: utf-8

import sys
import os
import pymorphy2

doc_path = sys.argv[1]
index_path = sys.argv[2]

morph = pymorphy2.MorphAnalyzer()

index = dict()
for filename in os.listdir(doc_path):
	inp = open(doc_path + "/" + filename, "r", encoding = "utf-8")	
	for line in inp.read().split():
		words = list()
		if not morph.parse(line):
			words.append(line)
		else:	
			words = [elem.normal_form for elem in morph.parse(line)]

		for word in words:
			if index.get(word) == None:
				index[word] = set()
			index[word].add(filename)

out = open(index_path, "w", encoding = "utf-8")
for word in index.keys():
	out.write(word + ":")
	out.write(" ".join(index[word]) + "\n")