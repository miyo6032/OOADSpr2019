#Gayathri Gude, Michael Yoshimura 
#OODA 4448 Homework One, Problem IV
#Bruce Montgomery, Spring 2019


#abstract class 
class shapeNames():  

	def getEdges (self): 
		pass

	def displayFunction(self):  
		pass 

#class for name and edges: Square
class square(shapeNames): 
	def getEdges(self):  
		return 4  

	def displayFunction(self): 
		print("square")

#class for name and edges: Circle 
class circle(shapeNames): 
	def getEdges(self):  
		return 0  

	def displayFunction(self): 
		print("circle")

#class for name and edges: Triangle
class triangle(shapeNames): 
	def getEdges(self):  
		return 3  

	def displayFunction(self): 
		print("triangle")

shapeList = [square(), circle(), triangle()] 

# Sorts based on the number of edges of the shape
sortedList = sorted(shapeList, key=lambda shape: shape.getEdges())

for shape in sortedList:
	shape.displayFunction()