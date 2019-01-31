#Gayathri Gude, Michael Yoshimura 
#OODA 4448 Homework One, Problem IV
#Bruce Montgomery, Spring 2019

# If this is not found, run 'pip install Lib' to install the abc module
from abc import ABC, abstractmethod

# The shapeNames class is an abstract class that represents a general shape.
# Inhereting from ABC makes it abstract
class shapeNames(ABC):

	# Returns the number of edges for a shape
	@abstractmethod
	def getEdges (self): 
		pass

	# Displays the name for a shape
	@abstractmethod
	def displayFunction(self):  
		pass 

# class for name and edges: Square
class square(shapeNames): 
	def getEdges(self):  
		return 4  

	def displayFunction(self): 
		print("square")

# class for name and edges: Circle 
class circle(shapeNames): 
	def getEdges(self):  
		return 0  

	def displayFunction(self): 
		print("circle")

# class for name and edges: Triangle
class triangle(shapeNames): 
	def getEdges(self):  
		return 3  

	def displayFunction(self): 
		print("triangle")

# This is our database, where each item is a shape. 
shapeList = [square(), circle(), triangle()] 

# Sorts based on the number of edges of the shape
sortedList = sorted(shapeList, key=lambda shape: shape.getEdges())

for shape in sortedList:
	shape.displayFunction()