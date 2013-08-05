import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.util.Set;

import org.jgrapht.DirectedGraph;
import org.jgrapht.alg.CycleDetector;

import tools.syncBlockStats.Field;
import tools.syncBlockStats.StaticBlock;


public class CylceFinder {
	public static void main(String[] args){
		String graphName;
		if(args.length > 0){
			graphName = args[0] + "_graph.ser"; 
		}
		else{
			graphName = "graph.ser";
		}
		
		DirectedGraph<Field, StaticBlock> graph = null;
		try {
			FileInputStream gin = new FileInputStream(graphName);
			ObjectInputStream graph_ois = new ObjectInputStream(gin);
			graph = (DirectedGraph<Field, StaticBlock>) graph_ois.readObject();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		}
		
		System.out.println("Number of nodes = " + graph.vertexSet().size());
		System.out.println("Number of edges = " + graph.edgeSet().size());
		
		CycleDetector<Field, StaticBlock> cd = new CycleDetector<Field, StaticBlock>(graph);
		Set<Field> cycles = cd.findCycles();
		System.out.println("Number of Cycles = " + cycles.size());
	}
}
