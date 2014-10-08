#coding: utf-8

import sys
import os
import pymorphy2

doc_path = sys.argv[1]
index_path = sys.argv[2]

index = dict()
tmp_filename = "mylittlefile.txt"
for filename in os.listdir(doc_path):
	os.system("mystem -nl -e utf-8 %s %s" % (doc_path + "/" + filename, tmp_filename))
	inp = open(tmp_filename, "r", encoding = "utf-8")	
	for line in inp.read().split():
		words = line.replace("?", "").split("|")
		for word in words:
			if index.get(word) == None:
				index[word] = set()
			index[word].add(filename)
	inp.close()
os.remove(tmp_filename)

out = open(index_path, "w", encoding = "utf-8")
for word in index.keys():
	out.write(word + ":")
	out.write(" ".join(index[word]) + "\n")