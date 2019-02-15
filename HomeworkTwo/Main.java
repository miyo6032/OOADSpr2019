//Michael Yoshimura, Gayathri Gude 
//OODA 4448 Homework Two
//Bruce Montgomery, Spring 2019

import java.util.*; 

public class Main
{
    public static void main(String[] args)
    {
		ShapeSorter sorter = new ShapeSorter();
        sorter.addShape(new Square()); 
        sorter.addShape(new Circle());
        sorter.addShape(new Triangle());  

		sorter.displayShapes();
	}
}

