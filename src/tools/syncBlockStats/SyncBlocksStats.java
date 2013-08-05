package tools.syncBlockStats;
import java.awt.Rectangle;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.ArrayList;
import java.util.Set;
import java.util.Stack;
import java.util.concurrent.ConcurrentHashMap;

import javax.swing.JFrame;
import javax.swing.SwingConstants;
import javax.swing.WindowConstants;

import rr.meta.ClassInfo;
import rr.meta.SourceLocation;
import acme.util.decorations.Decoration;
import acme.util.decorations.DecorationFactory;
import acme.util.decorations.DefaultValue;
import acme.util.option.CommandLine;
import acme.util.option.CommandLineOption;
import rr.tool.Tool;
import rr.event.AccessEvent;
import rr.event.AcquireEvent;
import rr.event.ArrayAccessEvent;
import rr.event.MethodEvent;
import rr.event.ReleaseEvent;
import rr.event.VolatileAccessEvent;
import rr.state.ShadowThread;
import rr.state.ShadowVar;
import rr.event.FieldAccessEvent;

import org.jgraph.JGraph;
import org.jgraph.graph.DefaultGraphCell;
import org.jgraph.graph.GraphConstants;
import org.jgrapht.*;
import org.jgrapht.alg.BellmanFordShortestPath;
import org.jgrapht.alg.ConnectivityInspector;
import org.jgrapht.alg.CycleDetector;
import org.jgrapht.alg.DijkstraShortestPath;
import org.jgrapht.ext.JGraphModelAdapter;
import org.jgrapht.graph.*;
import org.jgrapht.traverse.DepthFirstIterator;



import java.util.Map;


public class SyncBlocksStats extends Tool {

/*----------------------------CLASS VARIABLES-----------------------*/
	private static boolean testOutput = false;
	
	//mapping from thread to thread local information (locks, accessed fields)
	private static DecorationFactory<ShadowThread> fac = new DecorationFactory<ShadowThread>();
	private static Decoration<ShadowThread, ThreadData> tdata =fac.make("tdata", DecorationFactory.Type.SINGLE, 
				new DefaultValue<ShadowThread, ThreadData>(){
					public ThreadData get(ShadowThread t) { return new ThreadData();}
			}); 
	
	//mapping from program location to access counts and depths
	private static ConcurrentHashMap<SourceLocation, Counter> pcMap = new ConcurrentHashMap<SourceLocation, Counter>();
	
	//state for recording partial order of accesses
	//private static Field lastAccessed = null;
	private static DirectedGraph<Field, StaticBlock> graph = new ListenableDirectedMultigraph<Field, StaticBlock>(StaticBlock.class);
	private static Set<Field> cycles = new HashSet<Field>();
	private static ConnectivityInspector<Field, StaticBlock> connections = new ConnectivityInspector<Field, StaticBlock>(graph);
	
	//commandline options to specify analysis
	CommandLineOption<Boolean> trackOrder;
	CommandLineOption<Boolean> trackCounts;
	CommandLineOption<String> outputName;
	
	
/*-----------------------------INNER CLASSES---------------------*/	
	
	private class AccessTracker{
		Object o;
		boolean r = false;
		boolean w = false;
		SourceLocation loc;
		int currDepth = 0;
		int firstRDepth = -1;
		int firstWDepth = -1;
		
		public AccessTracker(AcquireEvent ae){
			this.o = ae.getLock().getLock();
			synchronized(ae.getInfo()){
				SourceLocation origLoc = ae.getInfo().getLoc();
				synchronized(origLoc){
					this.loc = new SourceLocation(origLoc.getFile(), origLoc.getLine());
				}
			}
		}
	}
	
	private static class ThreadData{
		private final Stack<AccessTracker> locks = new Stack<AccessTracker>();
		private Field lastAccessed = null;
		private HashSet<Field> seen = new HashSet<Field>();
		public long accesses = 0;
		
		public Stack<AccessTracker> getLocks(){
			return locks;
		}
		
		public Field getLastAccessed(){
			return lastAccessed;
		}
		
		public void setLastAccessed(Field f){
			lastAccessed = f;
		}
		
		public HashSet<Field> getSeen(){
			return seen;
		}
		public void setSeen(HashSet<Field> seen){
			this.seen = seen; 
		}
		
	}
	
	private static class Counter{
		int  Total = 0;
		int Read = 0;
		int Write = 0;
		int None = 0;
		List<Integer> depths = new ArrayList<Integer>();
	}
/*----------------------------TOOL IMPLEMENTATION----------------------------*/
	
	public SyncBlocksStats(String name, Tool next, CommandLine commandLine) {
		super(name, next, commandLine);
	  
		trackOrder = CommandLine.makeBoolean(
				"noOrder",
				true,
				CommandLineOption.Kind.EXPERIMENTAL,
				"Enable tracking of order of accesses. Default value is true");
		
		trackCounts = CommandLine.makeBoolean(
				"noCounts",
				true,
				CommandLineOption.Kind.EXPERIMENTAL,
				"Enable tracking of read, write, neither counts per static synchronized block." +
				"Default value is true");
		
		outputName = CommandLine.makeString(
				"output",
				"",
				CommandLineOption.Kind.EXPERIMENTAL,
				"Name modifier for order analysis output. -output=avrora will output the files " +
				"avrora_graph.ser and avrora_roots.ser if the trackOrder option is set to true."
				);
		
		commandLine.add(trackOrder);
		commandLine.add(trackCounts);
		commandLine.add(outputName);
	}
	
	
	@Override
	public void acquire(AcquireEvent ae){
		if(testOutput){
			System.out.println("thread " + ae.getThread().getTid() + " acquired " + ae.getLock().getLock().toString());
		}
		
		Stack<AccessTracker> localLocks = tdata.get(ae.getThread()).getLocks();
		AccessTracker at = new AccessTracker(ae);
		
		if(trackCounts.get()){
			updateBlockTotal(at);
		}
		
		localLocks.push(at);
	}
	
	private void updateBlockTotal(AccessTracker at){
		Counter newCount = new Counter();
		newCount.Total++;

		
		if(pcMap.putIfAbsent(at.loc, newCount) != null){
			Counter prevCount = pcMap.get(at.loc);
			synchronized(prevCount){
				prevCount.Total++;
			}
		}
	}
	
	@Override
	public void release(ReleaseEvent re){
		if(testOutput){
			System.out.println("thread " + re.getThread().getTid() + " released " + re.getLock().getLock().toString());
		}
		
		
		Stack<AccessTracker> localLocks = tdata.get(re.getThread()).getLocks();
		AccessTracker at = localLocks.pop();
		
		if(trackCounts.get()){
			updateBlockCategory(at);
		}
		
		if(trackOrder.get()){
			//reset variable tracking when finished with sync block
			if(localLocks.size() == 0){
				ThreadData td = tdata.get(re.getThread());
				td.setLastAccessed(null);
				td.setSeen(new HashSet<Field>());
			}
			//findNewCycles();
		}
	}
	
	private void updateBlockCategory(AccessTracker at){
		Counter count = pcMap.get(at.loc);
		
		synchronized(count){
			if(at.w){
				count.Write++;
				if(!count.depths.contains(at.firstWDepth)) count.depths.add(at.firstWDepth);
			}
			else if(at.r){
				count.Read++;
				if(!count.depths.contains(at.firstRDepth)) count.depths.add(at.firstRDepth);
			}
			else{
				count.None++;
			}
		}
	}
	
	private void findNewCycles(){
		synchronized(graph){
			CycleDetector<Field, StaticBlock> cd = new CycleDetector<Field, StaticBlock>(graph);
			Set<Field> newCycles = cd.findCycles();
			synchronized(cycles){
				cycles.addAll(newCycles);
			}
		}
	}
	
	@Override
	public void access(AccessEvent ae){
		ThreadData td = tdata.get(ae.getThread());
		td.accesses++;
		if((td.accesses % 10000) == 0) {
			System.out.println("There are " + graph.vertexSet().size() + " in the graph.");
		}
		Stack<AccessTracker> localLocks = td.getLocks();
		
		if(trackOrder.get()){
			//do only when in sync block
			if(localLocks.size() != 0){
				//get current field accessed
				Field curr = null;
				if(ae.getOriginalShadow() instanceof Field){
					curr = (Field)ae.getOriginalShadow();
				}
				else{
					curr = (Field)makeShadowVar(ae);
				}
				
				if(!td.getSeen().contains(curr)){
					curr.loc = localLocks.peek().loc;
							
					//get last field accessed in the sync block
					Field prev = td.getLastAccessed();
					
					//if the current field is the first field accessed in sync block
					if(prev == null){
						td.setLastAccessed(curr);
					}
					else{
						addAccessToGraph(prev, curr, prev.loc);
						td.setLastAccessed(curr);
					}
					td.getSeen().add(curr);
				}
			}
		}
		
		if(trackCounts.get()){
			categorizeAccess(ae, localLocks);
		}
	}
	
	private void addAccessToGraph(Field prev, Field curr, SourceLocation block){
		synchronized(graph){
			graph.addVertex(prev);
			graph.addVertex(curr);
			if(DijkstraShortestPath.<Field, StaticBlock>findPathBetween(graph, prev, curr) == null){
				StaticBlock e = graph.addEdge(prev, curr);
				e.file = block.getFile();
				e.line = block.getLine();
			}
		}
	}
	
	private void categorizeAccess(AccessEvent ae, Stack<AccessTracker>localLocks){
		Object target = ae.getTarget();
		Object self = ae.getAccessed();
		
		for(AccessTracker at : localLocks){
			if (at.o == self){
				if(ae.isWrite()){
					setFirstDepth(at, false);
					at.w = true;
				}
				else{
					setFirstDepth(at, true);
					at.r = true;
				}
			}
			else if(at.o == target){
				setFirstDepth(at, true);
				at.r = true;
			}
			else if(at.o instanceof Class){
				Class<?> heldClass = (Class<?>)at.o;
				ClassInfo cinfo = ae.getAccessInfo().getEnclosing().getOwner();
				if(heldClass.getName().equals(cinfo.getName().replace('/', '.'))) { 
					setFirstDepth(at, true);
					at.r = true;
				}
			}
		}
	}
	
	private void setFirstDepth(AccessTracker at, boolean isRead){
		if(isRead){
			if(!at.r){
				at.firstRDepth = at.currDepth;
			}
		}
		else{
			if(!at.w){
				at.firstWDepth = at.currDepth;
			}
		}
	}
	
	@Override
	public void volatileAccess(VolatileAccessEvent e){
		access(e);
	}
	@Override
	public ShadowVar makeShadowVar(AccessEvent ae){
		if(trackOrder.get()){
			Field f = new Field();
			if(ae.getKind() == AccessEvent.Kind.FIELD || ae.getKind() == AccessEvent.Kind.VOLATILE){
				FieldAccessEvent fae = (FieldAccessEvent)ae;
				f.name = fae.getInfo().getField().getName();
			}
			else{
				ArrayAccessEvent aae = (ArrayAccessEvent)ae;
				f.name = aae.getTarget().toString() + "[" + aae.getIndex() + "]";
			}
			return f;
		}
		return new ShadowVar(){};
	}
	
	@Override
	public void enter(MethodEvent me){
		if(testOutput){
			System.out.println(me.toString());
		}
		
		if(trackCounts.get()){
			Stack<AccessTracker> localLocks = tdata.get(me.getThread()).getLocks();
			for(AccessTracker at : localLocks){
				at.currDepth++;
			}
		}
		
	}
	@Override
	public void exit(MethodEvent me){
		if(testOutput){
			System.out.println(me.toString());
		}
		
		if(trackCounts.get()){
			Stack<AccessTracker> localLocks = tdata.get(me.getThread()).getLocks();
			for(AccessTracker at : localLocks){
				at.currDepth--;
			}
		}
	}
	
	@Override
	public void fini(){
		if(trackOrder.get())
			try {
				saveOrderAnalysis();
			} catch (IOException e) {
				e.printStackTrace();
			}
		if(trackCounts.get()) printCountsAnalysis();
	}
	
	private void saveOrderAnalysis() throws IOException{
		//System.out.println("Cycle Set Size = " + cycles.size());
		
		String output = outputName.get();
		String graphName;
		if(!output.isEmpty()){
			graphName = output + "_graph.ser";
		}
		else{
			graphName = "graph.ser";
		}
		FileOutputStream gout = new FileOutputStream(graphName);
		ObjectOutputStream graph_oos = new ObjectOutputStream(gout);
		graph_oos.writeObject(graph);
	}
	
	
	private void printCountsAnalysis(){
		synchronized(pcMap){
			System.out.println("Number of Static Synchronized Blocks = " + pcMap.size());
			
			Set<SourceLocation> keys = pcMap.keySet();
			for(SourceLocation loc : keys){
				Counter count = pcMap.get(loc);
				synchronized(count){
					StringBuilder sb = new StringBuilder();
					sb.append("[");
					for(Integer i : count.depths){
						sb.append(i + ",");
					}
					if(sb.length() > 1) sb.replace(sb.length() - 1, sb.length(), "]");
					else sb.append("]");
					
					System.out.printf("result['%s line %d'] = {\"total\" : %d , \"read\" : %d, " +
							"\"write\" : %d, \"neither\" : %d, \"depths\" : %s}\n", 
						loc.getFile().replace('/', '.'), loc.getLine(), count.Total, count.Read, count.Write, count.None, sb.toString());
				}
			}
		}
	}
}
