#coding: cp1251

import math

n = int(input())
grade = [int(g) for g in input().split()]


def dcg(grades):
	res = 0
	for i in range(len(grade)):
		res += (pow(2, grades[i]) - 1) / math.log(i + 2, 2)
	return res

	
DCG = dcg(grade)

best_ranking = grade.copy()
best_ranking.sort()
best_ranking.reverse()
NDCG = DCG / dcg(best_ranking)

pBreak = 0.15


def pFound(grades):
	res = 0
	pLook = 1# - pBreak
	for grade in grades:
		pRel = (pow(2, grade) - 1) / pow(2, 3)# - grade[i])
		res += pLook * pRel
		pLook *= (1 - pRel) * (1 - pBreak)
	return res


PFound = pFound(grade)

print("DCG = ", DCG)
print("NDCG = ", NDCG)
print("PFound = ", PFound)