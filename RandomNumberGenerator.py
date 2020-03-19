#!/usr/bin/python3
from prettytable import PrettyTable
table=PrettyTable()
table.field_names =["Iteration","Probabilités attendues","Nos probabilités","Valeur attendues","Nos valeurs"]

class Generator:

	def __init__(self,modulus = 2**32,a = 22695477,c =1,seed = 1337):
		self.modulus = modulus
		self.a = a
		self.c = c
		self.seed = seed

	def lcg(self,min,max):
		self.seed = (self.a*self.seed+self.c)%self.modulus
		#return (xi + (max - min)) % (max - min + 1) + min
		return int(min + ((self.seed - 0) / (self.modulus - 0)) * (max - min))
		
	def lcg_List (self,nbIterate,min,max):
		prs = [];
		xn = self.seed;
		for i in range (nbIterate):
			xn = (self.a*xn + self.c) % self.modulus;
			#prs.append ((xn + (max - min)) % (max - min +1) + min);
			prs.append(int(min + ((xn - 0) / (self.modulus - 0)) * (max - min)))
		return prs;

def DiceTest(nbIterate,gen):
	expectedResult = [1/36, 1/18, 1/12, 1/9, 5/36, 1/6, 5/36, 1/9, 1/12, 1/18, 1/36]
	myResult = [0,0,0,0,0,0,0,0,0,0,0]
	(modulus,a,c,min,max) = (2**32,22695477,1,1,7)
	for i in range (nbIterate):
		res = int(gen.lcg(min,max)) + int(gen.lcg(min,max))-2
		#print(res)
		myResult[res] = myResult[res] + 1
	print(myResult)
	print("Test Khi 2 à 5% de marge d'erreur ")
	KHI1 = 0
	for i in range(11):
		# Formule KHI2 : 
		#Chi2 Calculé : somme(Effectif Theorique - Effectif Reel)^2 / Effectif Théorique
		KHI1 = KHI1 +(myResult[i] - nbIterate * expectedResult[i])**2/(nbIterate*expectedResult[i])
	
	# Nous allons fusionner les probabilités de 2,3 et 11,12
	RES2 = 0
	RES2 = RES2 + ((myResult[0]+myResult[1]) - nbIterate * (expectedResult[0]+expectedResult[1]))**2/(nbIterate * (expectedResult[0]+expectedResult[1])) 
	RES2 = RES2+((myResult[9]+myResult[10]) - nbIterate * (expectedResult[9]+expectedResult[10]))**2/(nbIterate * (expectedResult[9]+expectedResult[10])) 
	
	for i in range(2, 9):
		RES2 = RES2 + ( myResult[i] - nbIterate * expectedResult[i])**2/(nbIterate * expectedResult[i])
	
	if (KHI1 >= 18.31 or RES2 >=18.31):
		print("---------------------  TEST KHI DEUX INCORRECT --------------------------")
		for i in range(11):
			table.add_row([i%11+1,expectedResult[i],int(myResult[i])/1000, 1000*expectedResult[i],myResult[i]])
		print(table)

		print("khi 2 statistic : 11 catégories " + str(KHI1) + " >= " + str(18.31))
		if(RES2 <= 18.31):
			print("------------------------------------------ 9 categories est juste khi 2 statistic : 9 catégories " + str(RES2) + " >= " + str(18.31) + "--------------------------------------")
		else:
			print("khi 2 statistic : 9 catégories " + str(RES2) + " >= " + str(18.31))
	else:
		print("-----------------------------TEST KHI DEUX CORRECT ----------------------------------")
		print("khi 2 OK " + str(KHI1))
		print("KHI 2 DEUXIEME TEST A 9 CATEGORIES" + str(RES2))

#Initialisation du seed de départ
#seed(14)
(modulus,multiplier,increment,seed) = (2**32,22695477,1,1)
gen = Generator(modulus,multiplier,increment,seed)
#print(gen.lcg_List(10,0,7))
if __name__ == "__main__":
	for i in range(1, 2):
		DiceTest(1000,gen)