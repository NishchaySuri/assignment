'''
Locus.sh Assignment
Diffusion Limited Aggregation (DLA)

-Nishchay Suri
155120029
Department of Physics
'''
import numpy as np
import random as rnd

class DLA():
	def __init__(self,dim,num,stickiness):
		self.M = dim						# Matrix is of the dimention : M X M (Assuming M is odd)
		self.num = num				# num is the number of Particles
		self.stickiness = stickiness		 
		self.Matrix = self.Initialize_Matrix()
		
		# Location of new Particle Introduced along the border
		self.row=0					
		self.col=0



	def Initialize_Matrix(self): # Set the middle element of the Matrix as 1
		self.Matrix = np.zeros((self.M,self.M))
		self.Matrix[(self.M-1)/2,(self.M-1)/2] = 1
		return(self.Matrix)



	def Print_Matrix(self):
		print self.Matrix



	''' 
		|->
		#######
		#	  #
		#     #   Intro_New_Particle = Introduces new particle along the border of Matrix
		#     #
		#######
	
	'''
	def Intro_New_Particle(self): # Randomly introduces a new particle along the border
		flag = True
		while flag:
			num = rnd.randint(0, 4*(self.M-1) -1) # There are ( 4 * (M-1) ) elements along the border. We select a random number from 0 to ( 4* (M -1) )
			quotient = int(num/(self.M-1))
			remainder = num%(self.M-1)

			if quotient == 0:
				self.row = quotient
				self.col = remainder
				element = self.Matrix[self.row,self.col]

			elif quotient == 1:
				self.row = remainder
				self.col = self.M-1
				element = self.Matrix[self.row,self.col]

			elif quotient == 2:
				self.row = self.M-1
				self.col = self.M-1-remainder
				element = self.Matrix[self.row,self.col]

			elif quotient == 3:
				self.row = self.M-1-remainder
				self.col = 0
				element = self.Matrix[self.row,self.col]

			if(element == 0):
				self.Matrix[self.row,self.col] = 1
				flag = False



	







if __name__=='__main__':
	a = DLA(5,1,1)
		