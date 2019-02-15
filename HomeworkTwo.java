//Michael Yoshimura, Gayathri Gude 
//OODA 4448 Homework Two
//Bruce Montgomery, Spring 2019


import java.util.*; 

public class Main
{
    public static void main(String[] args)
    {
        List <Shapes> shapesList = new ArrayList<Shapes>(); 
        shapesList.add(new Square()); 
        shapesList.add(new Circle()); 
        shapesList.add(new Triangle());  

        Collections.sort(shapesList, new SortByShapes());  

        for (Shapes s : shapesList)
        {
        	s.displayFunction(); 
        }
    }
}  

public class SortByShapes implements Comparator<Shapes> 
{
	public int compare(Shapes a, Shapes b)
	{
		return a.getEdges()-b.getEdges(); 
	}
}

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
		super(4, "Circle");
	}
}

public class Triangle extends Shapes
{
	public Triangle ()
	{
		super(4, "Triangle");
	}
}

