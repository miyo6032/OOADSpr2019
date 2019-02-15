// The main change occurs here, where we didn't want to have to override both methods every time
// we inhereted a new shape. Thus, we used a constructor to pass the information down into private fields.
// The trade offs are that the behavior is harder to chang at runtime, and parameters always have to passed down
// throught the constructor.
public abstract class Shape
{

	private int edges;
	private String name;

	public Shape(int edges, String name)
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