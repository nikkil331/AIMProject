package tools.syncBlockStats;

import org.jgrapht.graph.DefaultEdge;

import rr.meta.SourceLocation;

public class BlockEdge extends DefaultEdge{

	private static final long serialVersionUID = 1L;
	SourceLocation loc;
	
	public BlockEdge(){
		super();
	}
	@Override
	public String toString(){
		return loc.toString();
	}
}
