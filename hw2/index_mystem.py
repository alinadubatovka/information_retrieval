#coding: utf-8

import sys
import os

doc_path = sys.argv[1]
index_path = sys.argv[2]
     
def add_into_index(word, entry):
	filename, position = entry
	if index.get(word) == None:
		index[word] = dict()
	if index[word].get(filename) == None:
		index[word][filename] = [position]
	else:
		index[word][filename].append(position)
		

index = dict()
tmp_filename = "mylittlefile.txt"
for filename in os.listdir(doc_path):
	os.system("mystem -nl -e utf-8 %s %s" % (doc_path + "/" + filename, tmp_filename))
	inp = open(tmp_filename, "r", encoding = "utf-8")	
	pos = 0
	for line in inp.read().splitlines():	
		words = line.replace("?", "").split("|")
		for word in words:
			add_into_index(index, word, (filename, str(pos)))
		pos += 1
	inp.close()
os.remove(tmp_filename)

out = open(index_path, "w", encoding = "utf-8")
for word in index.keys():
	out.write(word + ":")
	for filename in index[word].keys():
		out.write(filename + "|")
		out.write(" ".join(index[word][filename]) + ";")
	out.write("\n")
out.close()