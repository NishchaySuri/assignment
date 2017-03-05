'''
Locus.sh Assignment
Diffusion Limited Aggregation (DLA) 

- Matrix M X M where M is an odd integer
- Image is toroidally bound

-Nishchay Suri
155120029
Department of Physics
'''
from timeit import default_timer as timer
import numpy as np
import random as rnd
import matplotlib.pyplot as plt

class DLA():

	'''
	DLA Class : Diffusion Limited Aggregation

	INPUT:
	1st Parameter : Dimention M (odd) of  M X M Matrix

					This is the input number M for M X M pixels/cells for an image/matrix.


	2nd Parameter : Number of Particles

					This is the number of particles for building the structure.


	3rd Parameter : Stickiness from [0,1]

					Stickiness is a parameter depending on the interaction of particles amoung each other.

																					   ####################################################	
	4th Parameter : Measure of distance of innter matrix from the structure (dist)  <- # Responsible for efficiency and quality of figure #
																					   ####################################################
					We take an inner matrix within the bigger M X M matrix. We introduce particles along it's border as it is closer to the structure. 
					After every few iterations we calculate the farthest point of the structure and introduce this border at a (dist) distance away.

					This inner matrix is torroidally bound as there is a much higher chance of particles sticking if they return closer to the structure.
					Appropriately large the (dist) parameter better 'Random Walks' we get as the particles introduced along the border have more space 
					to move freely.


	#################			Intro_New_Particle = Introduces new particle along the border of inner matrix (dim_temp X dim_temp)
	#				#								 The particle random walks inside this inner matrix and is torroidally bound inside it
	#				#								 to achieve greater efficiency. 
	#				#								 The size of the inner matrix is increased as the structure grows.
	#	 #######	#
	#	 #	   #	#
	#	 #  1  #    #    		Intro_New_Particle_anywhere = Introduces new particle inside the inner matrix (for the sake of increasing efficiency)
	#	 #     #	#						   
	#	 #######	#						  
	#				#						  
	#				#						  
	#				#		
	#################		
					 M X M	


	'''


	def __init__(self,dim,num,stickiness,dist):
		self.M = dim	            # Matrix is of the dimention : M X M (Assuming M is odd)
		self.num = num				# num is the number of Particles
		self.max_dimention = dim
		self.dist = dist
		# Centre of the Large M X M matrix
		self.row_centre = (dim-1)/2
		self.col_centre = (dim-1)/2

		self.stickiness = stickiness		 
		self.Matrix = self.Initialize_Matrix()
		self.stuck = False      	# Turns True when a particle gets stuck
		
		# Location of new Particle Introduced along the border
		self.row=0					
		self.col=0

		# Max row and Max col
		self.max_row = (self.max_dimention-1)/2
		self.max_col = (self.max_dimention-1)/2

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
		plt.imshow(self.Matrix,cmap='gray')
		plt.show()




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
				break




	# Randomly introduces a new particle anywhere in the matrix (To increase efficiency)
	def Intro_New_Particle_anywhere(self,dim):
		flag = True
		self.M = dim
		r_offset = self.row_centre - (dim-1)/2
		c_offset = self.col_centre - (dim-1)/2
		while(flag):
			rnd_row = rnd.randint(0,self.M-1)
			rnd_col = rnd.randint(0,self.M-1)
			if(self.Matrix[r_offset + rnd_row, c_offset + rnd_col] == 0):
				self.Matrix[r_offset+ rnd_row, c_offset + rnd_col] = 1
				self.row =  r_offset + rnd_row
				self.col =  c_offset + rnd_col
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

		# If a neighbouring cell has element 1
		for elem in self.adj:
			if(self.Matrix[elem[0],elem[1]] == 1):
				flag = True
				break 

		# If no neighbouring element is 1 
		if(flag == False): 
			self.Matrix[row,col] = 0
			num = rnd.randint(0,7)
			self.row , self.col = self.adj[num]
			self.Matrix[self.row,self.col] = 1
		
		# If a neighbouring element is 1 and particle does not stick probabilistically
		elif(flag == True and rnd.random() > self.stickiness):
			l=[]
			for eme in self.adj:
				if(self.Matrix[elem[0],elem[1]] == 0):
					l.append([elem[0],elem[1]])
			if len(l) != 0:
				num = rnd.randint(0,len(l))
				self.Matrix[row,col] = 0
				self.row , self.col = l[num]
				self.Matrix[self.row,self.col] = 1
		
		else:
			self.stuck = True
			self.Matrix[row,col] = 1 
			if(  (row-self.row_centre)**2 + (col-self.col_centre)**2 > (self.max_row-self.row_centre)**2 + (self.max_col-self.col_centre)**2 ) :
				self.max_row , self.max_col = row , col

		


	# Run for N particles 
	def Run_simulation(self):
		dim_temp = 51
		for i in range(0,self.num):
			if(i%100 == 0):
				print i,dim_temp

				if dim_temp < d.max_dimention:
					dim_temp = max(dim_temp, self.dist + 2* np.abs((max(self.max_row,self.max_col) - self.row_centre)))
				else:
					dim_temp = d.max_dimention
			
			self.Intro_New_Particle_anywhere(dim_temp)
			self.stuck = False
			while(self.stuck == False):
				self.random_step(self.row,self.col,dim_temp)




'''
FOR DLA
INPUT:
1st Parameter : Dimention M (odd) of  M X M Matrix
2nd Parameter : Number of Particles
3rd Parameter : Stickiness from [0,1]
4th Parameter : Measure of distance of innter matrix from the structure
'''

if __name__=='__main__':
	d = DLA(501,20000,1,51)

	start = timer()
	d.Run_simulation()
	end = timer()

	np.savetxt('matrix.txt',d.Matrix,fmt='%d')
	print("Time elapsed {}".format(end-start))
	d.plot()







