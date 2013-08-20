package tools.syncBlockStats;
import org.jgrapht.graph.DefaultEdge;


public class StaticBlock extends DefaultEdge{
	String file = "";
	int line;
	
	@Override
	public String toString(){
		return file + ":" + line;
	}
}
