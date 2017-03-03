'''
Locus.sh Assignment
Diffusion Limited Aggregation (DLA) 

- Matrix M X M where M is an odd integer
- Image is toroidally bound

-Nishchay Suri
155120029
Department of Physics
'''
import numpy as np
import random as rnd

class DLA():
	def __init__(self,dim,num,stickiness):
		self.M = dim	            # Matrix is of the dimention : M X M (Assuming M is odd)
		self.num = num				# num is the number of Particles
		self.stickiness = stickiness		 
		self.Matrix = self.Initialize_Matrix()
		self.stuck = False      	# Turns True when a particle gets stuck
		
		# Location of new Particle Introduced along the border
		self.row=0					
		self.col=0

		# Array of Adjacent indices in the Matrix
		self.adj = np.array([[self.row-1,self.col-1], [self.row-1,self.col], [self.row-1,self.col+1],
							 [self.row,self.col-1]  ,						 [self.row,self.col+1],
							 [self.row+1,self.col-1], [self.row+1,self.col], [self.row+1,self.col+1]])



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



	# Gets adjacent elements from (row,col)  (Matrix is toroidally bound)
	def get_adjacent(self,row,col):
		self.adj = np.array([  [row-1,col-1], [row-1,col], [row-1,col+1],
							   [row,col-1]  ,			   [row,col+1],
							   [row+1,col-1], [row+1,col], [row+1,col+1]])

		#For wrapping
		for r in range(0,8):
			for c in range(0,2):
				if(self.adj[r,c] == -1):
					self.adj[r,c] = self.M-1

				elif(self.adj[r,c] == self.M):
					self.adj[r,c] = 0

		return(self.adj)




	# Takes a random step from the element (row,col) by checking all adjacent cells and updates (self.row,self.col)
	def random_step(self,row,col):
		flag = False							# Flag turns True when a neighbouring cell has element 1
		self.adj = self.get_adjacent(row,col)

		# Counting number of neighbours having element 1 
		list_elements = []   					
		for elem in self.adj:
			if(self.Matrix[elem[0],elem[1]] == 1):
				flag = True
				list_elements.append(elem)    
		

		# Removes the elements from adjacency list which has element 1
		self.adj = np.delete(self.adj,list_elements,0) 


		# If no neighbouring element is 1 
		if(flag == False): 
			self.Matrix[row,col] = 0
			num = rnd.randint(0,7)
			self.row , self.col = self.adj[num]
			self.Matrix[self.row,self.col] = 1
		
		# If a neighbouring element is 1 and particle does not stick probabilistically
		elif(flag == True and rnd.random() > self.stickiness and len(self.adj)!=0):
			num = rnd.randint(0,len(self.adj)-1)
			self.Matrix[row,col] = 0
			self.row , self.col = self.adj[num]
			self.Matrix[self.row,self.col] = 1
		
		else:
			self.stuck = True
			self.Matrix[row,col] = 1 

		

	# Run for N particles 
	def Run_simulation(self):

		for i in range(0,self.num):
			self.Intro_New_Particle()
			self.stuck = False

			while(self.stuck == False):
				self.random_step(self.row,self.col)


'''
FOR DLA
INPUT:
1st Parameter : Dimention M (odd) of  M X M Matrix
2nd Parameter : Number of Particles
3rd Parameter : Stickiness from [0,1]
'''

if __name__=='__main__':
	d = DLA(101,4000,1)
	d.Run_simulation()







