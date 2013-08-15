import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.Set;

import org.jgraph.JGraph;
import org.jgraph.graph.DefaultEdge;
import org.jgrapht.DirectedGraph;
import org.jgrapht.Graph;
import org.jgrapht.alg.CycleDetector;
import org.jgrapht.graph.Subgraph;



import tools.syncBlockStats.Field;


public class CylceFinder {
	public static void main(String[] args){
		String graphName;
		if(args.length > 0){
			graphName = args[0] + "_graph.ser"; 
		}
		else{
			graphName = "graph.ser";
		}
		
		DirectedGraph<Field, DefaultEdge> graph = null;
		try {
			FileInputStream gin = new FileInputStream(graphName);
			ObjectInputStream graph_ois = new ObjectInputStream(gin);
			graph = (DirectedGraph<Field, DefaultEdge>) graph_ois.readObject();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		}
		
		System.out.println("Number of nodes = " + graph.vertexSet().size());
		System.out.println("Number of edges = " + graph.edgeSet().size());
		
		CycleDetector<Field, DefaultEdge> cd = new CycleDetector<Field, DefaultEdge>(graph);
		Set<Field> cycles = cd.findCycles();
		System.out.println("Number of Cycles = " + cycles.size());
		
		Graph<Field, DefaultEdge> cycleGraph = 
				new Subgraph<Field,DefaultEdge, DirectedGraph<Field, DefaultEdge>>(graph, cycles);
		
		String cyclesName;
		if(args.length > 0){
			cyclesName = args[0] + "_cycles.ser";
		}
		else{
			cyclesName = "cycles.ser";
		}
		
		FileOutputStream gout;
		try {
			gout = new FileOutputStream(cyclesName);
			ObjectOutputStream graph_oos = new ObjectOutputStream(gout);
			graph_oos.writeObject(cycleGraph);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
}
