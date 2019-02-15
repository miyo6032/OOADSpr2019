//Michael Yoshimura, Gayathri Gude 
//OODA 4448 Homework Two
//Bruce Montgomery, Spring 2019

import java.util.*; 

public class Main
{
    public static void main(String[] args)
    {
		// This part of the code is a direct port from the original python version
        List <Shape> shapesList = new ArrayList<Shape>(); 
        shapesList.add(new Square()); 
        shapesList.add(new Circle());
        shapesList.add(new Triangle());  

		// Sorts based on the Comparator defined below
        Collections.sort(shapesList, new SortByEdges());  

        for (Shape s : shapesList)
        {
        	s.displayFunction(); 
        }
	}
	
	// A comparator that determines which shapes are greater based on the number of edges
	// Behaves similarly to a python anonymous lambda function
	public static class SortByEdges implements Comparator<Shape> 
	{
		public int compare(Shape a, Shape b)
		{
			return a.getEdges()-b.getEdges(); 
		}
	}
}

