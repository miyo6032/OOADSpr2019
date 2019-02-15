import java.util.*; 

// Shape sorter provides and extra level of abstraction so that main doesn't have to deal
// with the details of sorting and keeping the database
public class ShapeSorter
{
    private List <Shape> shapesList = new ArrayList<Shape>(); 

    public void addShape(Shape s)
    {
        this.shapesList.add(s);
    }

    // Displays shapes by the number of edges
    public void displayShapes()
    {
        List <Shape> sortedShapes = new ArrayList(shapesList);
		// Sorts based on the Comparator defined below
        Collections.sort(sortedShapes, new SortByEdges());  

        for (Shape s : sortedShapes)
        {
        	s.displayFunction(); 
        }
    }
	
	// A comparator that determines which shapes are greater based on the number of edges
    // Behaves similarly to a python anonymous lambda function
	private static class SortByEdges implements Comparator<Shape> 
	{
		public int compare(Shape a, Shape b)
		{
			return a.getEdges()-b.getEdges(); 
		}
	}
}

