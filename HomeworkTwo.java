//Michael Yoshimura, Gayathri Gude 
//OODA 4448 Homework Two
//Bruce Montgomery, Spring 2019

// If this java file doesn't seem to run, than you can look at the project under the HomeworkTwo directory

import java.util.*; 

public class Main
{
    public static void main(String[] args)
    {
		// This part of the code is a direct port from the original python version
        List <Shapes> shapesList = new ArrayList<Shapes>(); 
        shapesList.add(new Square()); 
        shapesList.add(new Circle()); 
        shapesList.add(new Triangle());  

		// Sorts based on the Comparator defined below
        Collections.sort(shapesList, new SortByShapes());  

        for (Shapes s : shapesList)
        {
        	s.displayFunction(); 
        }
    }
}  

// A comparator that determines which shapes are greater based on the number of edges
// Behaves similarly to a python anonymous lambda function
public class SortByShapes implements Comparator<Shapes> 
{
	public int compare(Shapes a, Shapes b)
	{
		return a.getEdges()-b.getEdges(); 
	}
}

// The main change occurs here, where we didn't want to have to override both methods every time
// we inhereted a new shape. Thus, we used a constructor to pass the information down into private fields.
// The trade offs are that the behavior is harder to chang at runtime, and parameters always have to passed down
// throught the constructor.
public abstract class Shapes
{

	private int edges;
	private String name;

	public Shapes(int edges, String name)
	{
		this.edges = edges;
		this.name = name;
	}

	public  int getEdges()
	{
		return this.edges;
	} 
	public  void displayFunction()
	{
		System.out.println(this.name);
	}
} 

public class Square extends Shapes
{
	public Square ()
	{
		super(4, "Square");
	}
}

public class Circle extends Shapes
{
	public Circle ()
	{
		super(0, "Circle");
	}
}

public class Triangle extends Shapes
{
	public Triangle ()
	{
		super(3, "Triangle");
	}
}

