
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Rectangle;
import java.awt.event.MouseEvent;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.RandomAccessFile;

import org.jgraph.JGraph;
import org.jgraph.graph.AttributeMap;
import org.jgraph.graph.DefaultGraphModel;
import org.jgraph.graph.GraphCell;
import org.jgraph.graph.GraphConstants;
import org.jgraph.graph.GraphModel;
import org.jgrapht.DirectedGraph;
import org.jgrapht.Graph;
import org.jgrapht.ext.JGraphModelAdapter;

import tools.syncBlockStats.BlockEdge;
import tools.syncBlockStats.Field;

import com.jgraph.layout.JGraphCompoundLayout;
import com.jgraph.layout.JGraphFacade;
import com.jgraph.layout.JGraphLayout;
import com.jgraph.layout.organic.JGraphSelfOrganizingOrganicLayout;



import java.util.Map;

import javax.swing.JFrame;
import javax.swing.JScrollPane;
import javax.swing.ToolTipManager;
import javax.swing.border.LineBorder;


public class DisplayGraph {
	public static JGraphModelAdapter<Field, BlockEdge> adapter;
	public static void main(String[] args){	
		String graphName;
		
		if(args.length > 0){
			graphName = args[0] + ".ser";
		}
		else{
			graphName = "graph.ser";
		}
		
		Graph<Field, BlockEdge> graph = null;
		try {
			RandomAccessFile raf = new RandomAccessFile(graphName, "r");
			FileInputStream gin = new FileInputStream(raf.getFD());
			ObjectInputStream graph_ios = new ObjectInputStream(gin);
			graph = (Graph<Field, BlockEdge>) graph_ios.readObject();
			graph_ios.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		}
		
		if(graph.vertexSet().size() == 0){
			System.out.println("Empty graph. Nothing to display.");
			return;
		}
		
		//split groups of connected components into different windows for easier viewing
		//too many connected components, runs out of memory
		/*ConnectivityInspector<Field, BlockEdge> connectivity =
				new ConnectivityInspector<Field, BlockEdge>(graph);
		List<Set<Field>> ccs = connectivity.connectedSets();
		
		
		List<Set<Field>> combinedCCs = new ArrayList<Set<Field>>();
		for(int i = 0; i < ccs.size(); i+=10){
			if(i + 9 < ccs.size()){
				ccs.get(i).addAll(ccs.get(i + 1));
				ccs.get(i).addAll(ccs.get(i + 2));
				ccs.get(i).addAll(ccs.get(i + 3));
				ccs.get(i).addAll(ccs.get(i + 4));
				ccs.get(i).addAll(ccs.get(i + 5));
				ccs.get(i).addAll(ccs.get(i + 6));
				ccs.get(i).addAll(ccs.get(i + 7));
				ccs.get(i).addAll(ccs.get(i + 8));
				ccs.get(i).addAll(ccs.get(i + 9));
				combinedCCs.add(ccs.get(i));
			}
			else{
				for(int j = i + 1; j < ccs.size(); j++){
					ccs.get(i).addAll(ccs.get(j));
				}
				combinedCCs.add(ccs.get(i));
			}
		}

		
		for(Set<Field> cc : combinedCCs){
			Subgraph<Field, BlockEdge, DirectedGraph<Field, BlockEdge>> g = 
					new Subgraph<Field, BlockEdge, DirectedGraph<Field, BlockEdge>>(graph, cc);
		*/	
		
		//set up one layout for all connected components
		JGraphSelfOrganizingOrganicLayout sol = new JGraphSelfOrganizingOrganicLayout();
		sol.setDensityFactor(2000);
		sol.setStartRadius(100);
		sol.setMinRadius(80);
		JGraphLayout[] layouts = {sol};
		JGraphLayout compoundLayout = new JGraphCompoundLayout(layouts);
				
		//create jgraph
		adapter = 
				new MergingModelAdapter<Field, BlockEdge>(graph, createVertexAttributes(), createEdgeAttributes());
			
		JGraph graphVis = new ToolTipGraph(adapter);
		ToolTipManager.sharedInstance().registerComponent(graphVis);
			
		//configure jgraph
		graphVis.setEdgeLabelsMovable(false);
		graphVis.setConnectable(false);
		graphVis.setDisconnectable(false);

			
		JGraphFacade facade = new JGraphFacade(graphVis, new Field[0],
				true, false, false, true);
			
		compoundLayout.run(facade);
		Map layoutResult = facade.createNestedMap(true, true);
		graphVis.getGraphLayoutCache().edit(layoutResult);
		JFrame frame = new JFrame();
		frame.getContentPane().add(new JScrollPane(graphVis));
		frame.setMinimumSize(new Dimension(1000,500));
		frame.setVisible(true);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		//}
		
		
	}
	
	public static AttributeMap createVertexAttributes(){
		 AttributeMap map = new AttributeMap();
	     Color c = Color.lightGray;
	     
	     GraphConstants.setBounds(map, new Rectangle(50, 20));
	     GraphConstants.setBorder(map, new LineBorder(Color.decode("#25507C"), 2));
	     GraphConstants.setBackground(map, c);
	     GraphConstants.setFont(
	            map,
	            GraphConstants.DEFAULTFONT.deriveFont(Font.PLAIN, 10));
	     GraphConstants.setOpaque(map, true);
	     GraphConstants.setEditable(map, false);
	     
	     
	     
	     return map;
	}
	
	public static AttributeMap createEdgeAttributes(){
		AttributeMap map = new AttributeMap();

        
       GraphConstants.setLineEnd(map, GraphConstants.ARROW_TECHNICAL);
       GraphConstants.setBeginFill(map, true);
       GraphConstants.setEndFill(map, true);
       GraphConstants.setEndSize(map, 6);
       GraphConstants.setRouting(map, GraphConstants.ROUTING_SIMPLE);
       GraphConstants.setLineStyle(map, GraphConstants.STYLE_SPLINE);
       GraphConstants.setLabelEnabled(map, false);

       GraphConstants.setForeground(map, Color.decode("#25507C"));
       GraphConstants.setFont(
            map,
            GraphConstants.DEFAULTFONT.deriveFont(Font.PLAIN, 11));
        GraphConstants.setLineColor(map, Color.decode("#7AA1E6"));
        GraphConstants.setSelectable(map, false);
        GraphConstants.setDisconnectable(map, false);
        GraphConstants.setConnectable(map, false);
        
       
        return map;
	}
	
	private static class MergingModelAdapter<V,E> extends JGraphModelAdapter<V,E>{
		public MergingModelAdapter (Graph<V,E> jGraphTGraph) {
			super(jGraphTGraph);
		}
        public MergingModelAdapter(
        		Graph<V,E> jGraphTGraph,
        		AttributeMap defaultVertexAttributes,
        		AttributeMap BlockEdgeAttributes) {
        	super(jGraphTGraph, defaultVertexAttributes, BlockEdgeAttributes);
        }
        public MergingModelAdapter(
        		Graph<V,E> jGraphTGraph, 
        		AttributeMap defaultVertexAttributes, 
        		AttributeMap BlockEdgeAttributes, 
        		JGraphModelAdapter.CellFactory<V,E> cellFactory) {
        	super(jGraphTGraph, defaultVertexAttributes, BlockEdgeAttributes, cellFactory);
        }
        
        @Override
        protected AttributeMap createVertexAttributeMap(GraphCell vertexCell){
        	AttributeMap map = super.createVertexAttributeMap(vertexCell);
        	if(cellToVertex.get(vertexCell) instanceof Field){
        		if(((Field)cellToVertex.get(vertexCell)).merged){
        			GraphConstants.setBorder((AttributeMap)map.get(vertexCell), 
        					new LineBorder(Color.GREEN, 1));
        		}
        	}
        	return map;
        }
	}
	
	private static class ToolTipGraph extends JGraph{
		public ToolTipGraph(GraphModel model){
			super(model);
		}	
		
		@Override	
		public String getToolTipText(MouseEvent e) {
			if(e != null) {
		      // Fetch Cell under Mousepointer
				Object c = getFirstCellForLocation(e.getX(), e.getY());
				if (c != null){
						if (DefaultGraphModel.isVertex(adapter, c)){
							if(graphModel instanceof JGraphModelAdapter<?,?>){
								Field v = ((JGraphModelAdapter<Field, BlockEdge>)adapter).
										cellToVertex.get(c);
								return v.loc.toString();
							}
						}
						else if(graphModel.isEdge(c)){
							return convertValueToString(c);
						}
					}				
			    }
			    return null;
		}
	}
}
