
import java.util.List;
import java.awt.Color;
import java.awt.Font;
import java.awt.Rectangle;
import java.awt.event.MouseEvent;
import java.awt.geom.Rectangle2D;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.ObjectInputStream;

import org.jgraph.JGraph;
import org.jgraph.event.GraphSelectionEvent;
import org.jgraph.event.GraphSelectionListener;
import org.jgraph.graph.AttributeMap;
import org.jgraph.graph.DefaultCellViewFactory;
import org.jgraph.graph.DefaultGraphModel;
import org.jgraph.graph.GraphConstants;
import org.jgraph.graph.GraphLayoutCache;
import org.jgraph.graph.GraphModel;
import org.jgrapht.DirectedGraph;
import org.jgrapht.ext.JGraphModelAdapter;

import rr.meta.ClassInfo;
import tools.syncBlockStats.Field;
import tools.syncBlockStats.StaticBlock;

import org.jgraph.graph.GraphCell;

import com.jgraph.io.svg.SVGGraphConstants;
import com.jgraph.layout.JGraphCompoundLayout;
import com.jgraph.layout.JGraphFacade;
import com.jgraph.layout.JGraphLayout;
import com.jgraph.layout.graph.JGraphSimpleLayout;
import com.jgraph.layout.hierarchical.JGraphHierarchicalLayout;
import com.jgraph.layout.organic.JGraphFastOrganicLayout;
import com.jgraph.layout.organic.JGraphOrganicLayout;
import com.jgraph.layout.organic.JGraphSelfOrganizingOrganicLayout;
import com.jgraph.layout.tree.JGraphTreeLayout;

import java.util.Map;

import javax.swing.BorderFactory;
import javax.swing.JFrame;
import javax.swing.JScrollPane;
import javax.swing.ToolTipManager;
import javax.swing.WindowConstants;
import javax.swing.border.LineBorder;


public class DisplayGraph {
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
		
		//default vertex attributes
		
		
		//create jgraph
		JGraphModelAdapter<Field, StaticBlock> adapter = new JGraphModelAdapter<Field, StaticBlock>(
				graph, createVertexAttributes(), createEdgeAttributes());
		//GraphLayoutCache view = new GraphLayoutCache(adapter, new ToolTipCellViewFactory(graphVis));
		
		JGraph graphVis = new ToolTipGraph(adapter);
		ToolTipManager.sharedInstance().registerComponent(graphVis);
		//graphVis.setUI(new LabelsGraphUI(adapter));
	
		
		//configure jgraph
		graphVis.setEdgeLabelsMovable(false);
		graphVis.setConnectable(false);
		graphVis.setDisconnectable(false);

		
		//setup graph layout
		JGraphFacade facade = new JGraphFacade(graphVis, new Field[0],
				true, false, false, true);
		JGraphFastOrganicLayout fol = new JGraphFastOrganicLayout();
		fol.setForceConstant(30);
		JGraphLayout[] layouts = {new JGraphSelfOrganizingOrganicLayout(), fol};
		JGraphLayout compoundLayout = new JGraphCompoundLayout(layouts);
		compoundLayout.run(facade);
		Map layoutResult = facade.createNestedMap(true, true);
		graphVis.getGraphLayoutCache().edit(layoutResult);
		
		JFrame frame = new JFrame();
		frame.getContentPane().add(new JScrollPane(graphVis));
		frame.pack();
		frame.setVisible(true);
		frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
	}
	
	public static AttributeMap createVertexAttributes(){
		 AttributeMap map = new AttributeMap();
	     Color c = Color.lightGray;
	     
	     GraphConstants.setBounds(map, new Rectangle(60, 40));
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

        
       GraphConstants.setLineEnd(map, GraphConstants.ARROW_CLASSIC);
       GraphConstants.setBeginFill(map, true);
       GraphConstants.setEndFill(map, true);
       GraphConstants.setEndSize(map, 6);
       GraphConstants.setRouting(map, GraphConstants.ROUTING_SIMPLE);
       GraphConstants.setLineStyle(map, GraphConstants.STYLE_BEZIER);
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
	
	public static class ToolTipGraph extends JGraph{
		public ToolTipGraph(GraphModel model){
			super(model);
		}	
		
		@Override	
		public String getToolTipText(MouseEvent e) {
			if(e != null) {
			    // Fetch Cell under Mousepointer
			    Object c = getFirstCellForLocation(e.getX(), e.getY());
			    if (c != null){
				// Convert Cell to String and Return
				if(graphModel.isEdge(c)){
				    return convertValueToString(c);
				}
				else return null;
			    }
			}
			return null;
		}
	}
}
