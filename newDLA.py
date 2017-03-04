'''
Locus.sh Assignment
Diffusion Limited Aggregation (DLA) 

- Matrix M X M where M is an odd integer
- Image is toroidally bound

-Nishchay Suri
155120029
Department of Physics
'''
import time
import numpy as np
import random as rnd
import matplotlib.pyplot as plt

class DLA():
	def __init__(self,dim,num,stickiness):
		self.M = dim	            # Matrix is of the dimention : M X M (Assuming M is odd)
		self.num = num				# num is the number of Particles

		# Centre of the Large M X M matrix
		self.row_centre = (dim-1)/2
		self.col_centre = (dim-1)/2

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




	# Plots the pixels on image using Matrix
	def plot(self):
		plt.imshow(self.Matrix)
		plt.show()



	''' 
		|->
		#######
		#	  #
		#     #   Intro_New_Particle = Introduces new particle along the border of Matrix
		#     #
		#######
	
	'''
	def Intro_New_Particle(self,dim_temp): # Randomly introduces a new particle along the border of dim_temp around the bigger matrix
		flag = True
		self.M = dim_temp
		row_diff = self.row_centre - (dim_temp-1)/2
		col_diff = self.col_centre - (dim_temp-1)/2

		while flag:
			num = rnd.randint(0, 4*(self.M-1) -1) # There are ( 4 * (M-1) ) elements along the border. We select a random number from 0 to ( 4* (M -1) )
			quotient = int(num/(self.M-1))
			remainder = num%(self.M-1)

			if quotient == 0:
				self.row = row_diff + quotient
				self.col = col_diff + remainder
				element = self.Matrix[row_diff + self.row,col_diff + self.col]

			elif quotient == 1:
				self.row = row_diff + remainder
				self.col = col_diff + self.M-1
				element = self.Matrix[row_diff + self.row,col_diff + self.col]

			elif quotient == 2:
				self.row = row_diff + self.M-1
				self.col = col_diff + self.M-1-remainder
				element = self.Matrix[row_diff + self.row,col_diff + self.col]

			elif quotient == 3:
				self.row = row_diff + self.M-1-remainder
				self.col = col_diff + 0
				element = self.Matrix[row_diff + self.row,col_diff + self.col]

			if(element == 0):
				self.Matrix[self.row,self.col] = 1
				flag = False





	# Randomly introduces a new particle anywhere in the matrix (To increase efficiency)
	def Intro_New_Particle_anywhere(self):
		flag = True

		while(flag):
			rnd_row = rnd.randint(0,self.M-1)
			rnd_col = rnd.randint(0,self.M-1)
			if(self.Matrix[rnd_row,rnd_col] == 0):
				self.Matrix[rnd_row,rnd_col] = 1
				self.row = rnd_row
				self.col = rnd_col
				flag = False




	# Gets adjacent elements from (row,col)  (Matrix is toroidally bound)
	def get_adjacent(self,row,col,dim_temp):
		self.adj = np.array([  [row-1,col-1], [row-1,col], [row-1,col+1],
							   [row,col-1]  ,			   [row,col+1],
							   [row+1,col-1], [row+1,col], [row+1,col+1]])

		#For wrapping
		for r in range(0,8):
			for c in range(0,2):
				if(self.adj[r,c] == self.row_centre - (dim_temp-1)/2 -1):
					self.adj[r,c] = self.row_centre + (dim_temp-1)/2 

				elif(self.adj[r,c] == self.row_centre + (dim_temp-1)/2 +1):
					self.adj[r,c] = self.row_centre - (dim_temp-1)/2

		return(self.adj)




	# Takes a random step from the element (row,col) by checking all adjacent cells and updates (self.row,self.col)
	def random_step(self,row,col,dim_temp):
		flag = False							# Flag turns True when a neighbouring cell has element 1
		self.adj = self.get_adjacent(row,col,dim_temp)

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
			if(i%50 == 0):
				print i

			if i<=700:
				self.Intro_New_Particle(101)
				self.stuck = False

				while(self.stuck == False):
					self.random_step(self.row,self.col,101)

			if i>700 and i<=1900:
				self.Intro_New_Particle(201)
				self.stuck = False

				while(self.stuck == False):
					self.random_step(self.row,self.col,201)






'''
FOR DLA
INPUT:
1st Parameter : Dimention M (odd) of  M X M Matrix
2nd Parameter : Number of Particles
3rd Parameter : Stickiness from [0,1]
'''

if __name__=='__main__':
	d = DLA(501,1700,1)
	start = time.time()
	d.Run_simulation()
	end = time.time()

	print("Time elapsed {}".format(end-start))







