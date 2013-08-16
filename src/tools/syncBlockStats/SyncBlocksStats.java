package tools.syncBlockStats;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.io.RandomAccessFile;
import java.util.HashSet;
import java.util.List;
import java.util.ArrayList;
import java.util.Set;
import java.util.Stack;
import java.util.concurrent.ConcurrentHashMap;

import java.util.Iterator;


import rr.meta.ClassInfo;
import rr.meta.FieldInfo;
import rr.meta.SourceLocation;
import acme.util.decorations.Decoration;
import acme.util.decorations.DecorationFactory;
import acme.util.decorations.DefaultValue;
import acme.util.option.CommandLine;
import acme.util.option.CommandLineOption;
import rr.tool.TaggedValue.Type;
import rr.tool.Tool;
import rr.event.AccessEvent;
import rr.event.AcquireEvent;
import rr.event.ArrayAccessEvent;
import rr.event.InterruptEvent;
import rr.event.JoinEvent;
import rr.event.MethodEvent;
import rr.event.ReleaseEvent;
import rr.event.SleepEvent;
import rr.event.VolatileAccessEvent;
import rr.event.WaitEvent;
import rr.state.ShadowThread;
import rr.state.ShadowVar;
import rr.event.FieldAccessEvent;


import org.jgrapht.DirectedGraph;
import org.jgrapht.alg.CycleDetector;
import org.jgrapht.alg.DijkstraShortestPath;
import org.jgrapht.alg.JohnsonsCycleFinder;
import org.jgrapht.graph.*;






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
	private static ConcurrentHashMap<SourceLocation, Counter> pcMap = 
			new ConcurrentHashMap<SourceLocation, Counter>();
	
	
	//mapping from static fields to shadow var instances
	private static ConcurrentHashMap<FieldInfo, List<Field>> fieldMap =
			new ConcurrentHashMap<FieldInfo, List<Field>>();
	
	//state for recording partial order of accesses
	private static DefaultDirectedGraph<Field, BlockEdge> globalGraph = 
			new DefaultDirectedGraph<Field, BlockEdge>(BlockEdge.class);
	
	static int LOCKS_GRABBED = 1;
	
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
				this.loc = ae.getInfo().getLoc();
			}
		}
	}
	
	private static class ThreadData{
		private final Stack<AccessTracker> locks = new Stack<AccessTracker>();
		private DefaultDirectedGraph<Field, BlockEdge> graph = new DefaultDirectedGraph<Field, BlockEdge>(BlockEdge.class);
		private Field lastAccessed = null;
		private HashSet<Field> seen = new HashSet<Field>();
		public int locksGrabbed;
		
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
	public void stop(ShadowThread st){
		ThreadData td = tdata.get(st);
		if(td.graph.vertexSet().size() != 0){
			unionGraph(td);
		}
	}
	
	@Override
	public void preSleep(SleepEvent se){
		ThreadData td = tdata.get(se.getThread());
		if(td.graph.vertexSet().size() != 0){
			unionGraph(td);
		}	
	}
	
	@Override
	public void preJoin(JoinEvent je){
		ThreadData td = tdata.get(je.getThread());
		if(td.graph.vertexSet().size() != 0){
			unionGraph(td);
		}
	}
	
	@Override
	public void preInterrupt(InterruptEvent ie){
		ThreadData td = tdata.get(ie.getThread());
		if(td.graph.vertexSet().size() != 0){
			unionGraph(td);
		}
	}
	
	@Override
	public void preWait(WaitEvent we){
		ThreadData td = tdata.get(we.getThread());
		if(td.graph.vertexSet().size() != 0){
			unionGraph(td);
		}
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
		
		tdata.get(ae.getThread()).locksGrabbed++;
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
		ThreadData td = tdata.get(re.getThread());
		
		Stack<AccessTracker> localLocks = td.getLocks();
		AccessTracker at = localLocks.pop();
		
		if(trackCounts.get()){
			updateBlockCategory(at);
		}
		
		if(trackOrder.get()){
			if(td.locksGrabbed % LOCKS_GRABBED == 0){
				unionGraph(td);
			}
			//reset variable tracking when finished with sync block
			if(localLocks.size() == 0){
				td.setLastAccessed(null);
				td.setSeen(new HashSet<Field>());
			}
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
	
	public void unionGraph(ThreadData td){
		synchronized(globalGraph){
			globalGraph.union(td.graph);
		}
		td.graph = new DefaultDirectedGraph<Field, BlockEdge>(BlockEdge.class);
		
	}
	
	
	@Override
	public void access(AccessEvent ae){
		ThreadData td = tdata.get(ae.getThread());
		Stack<AccessTracker> localLocks = td.getLocks();
		
		if(trackOrder.get()){
			//do only when in sync block
			if(localLocks.size() > 0){
				//get current field accessed
				Field curr = null;
				if(ae.getOriginalShadow() instanceof Field){
					curr = (Field)ae.getOriginalShadow();
				}
				else{
					curr = (Field)makeShadowVar(ae);
				}
				curr.loc = localLocks.peek().loc;
				
				//if access is a field type, add it to map
				if(ae.getKind() == AccessEvent.Kind.FIELD || ae.getKind() == AccessEvent.Kind.VOLATILE){
					FieldInfo field = curr.statField;
					
					List<Field> vList = new ArrayList<Field>();
					vList.add(curr);
					if(fieldMap.putIfAbsent(field, vList) != null){
						List<Field> vertices = fieldMap.get(field);
						synchronized(vertices){
							if(!vertices.contains(curr)) vertices.add(curr);
						}
					}
				}
				
				
				if(!td.getSeen().contains(curr)){
					//get last field accessed in the sync block
					Field prev = td.getLastAccessed();
					
					//if the current field is the first field accessed in sync block
					if(prev == null){
						td.setLastAccessed(curr);
						td.graph.addVertex(curr);
					}
					else{
						addEdgeAccessToGraph(td, prev, curr);
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
	
	private void addEdgeAccessToGraph(ThreadData td, Field prev, Field curr){
		td.graph.addVertex(prev);
		td.graph.addVertex(curr);
		if(DijkstraShortestPath.<Field, BlockEdge>findPathBetween(td.graph, prev, curr) == null){
			BlockEdge e = td.graph.addEdge(prev, curr);
			e.loc = prev.loc;
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
		Stack<AccessTracker> localLocks = tdata.get(ae.getThread()).locks;
		if(trackOrder.get()){
			Field f = new Field();
			if(ae.getKind() == AccessEvent.Kind.FIELD || ae.getKind() == AccessEvent.Kind.VOLATILE){
				FieldAccessEvent fae = (FieldAccessEvent)ae;
				f.isField = true;
				f.name = fae.getInfo().getField().getName();
				f.statField = fae.getInfo().getField();
			}
			else{
				ArrayAccessEvent aae = (ArrayAccessEvent)ae;
				f.isField = false;
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
				synchronized(globalGraph){
					saveOrderAnalysis();
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		if(trackCounts.get()) printCountsAnalysis();
	}
	
	private void saveOrderAnalysis() throws IOException{
		System.out.println("Number of nodes = " + globalGraph.vertexSet().size());
		System.out.println("Number of edges = " + globalGraph.edgeSet().size());
		
		//get vertices in cycle
		CycleDetector<Field, BlockEdge> cd = new CycleDetector<Field, BlockEdge>(globalGraph);
		Set<Field> cycles = cd.findCycles();
		
		//get edges in cycle subgraph
		Set<BlockEdge> edges = new HashSet<BlockEdge>();
        
        for(Field f : cycles){
        	Set<BlockEdge> outEs = globalGraph.outgoingEdgesOf(f);
        	for(BlockEdge e : outEs){
        		if(cycles.contains(globalGraph.getEdgeTarget(e))) edges.add(e);
        	}
        }
		
		DirectedGraph<Field, BlockEdge> cycleGraph = new DirectedSubgraph<Field, BlockEdge>(
				globalGraph,
				cycles,
				edges
				);
		
		
		//find number of simple cycles in cycle graph
		JohnsonsCycleFinder<Field,BlockEdge> johnsons = new JohnsonsCycleFinder<Field,BlockEdge>(cycleGraph);
		int numCycles = johnsons.getCycleCount();
		System.out.println("Number of simple cycles = " + numCycles);
		
		synchronized(globalGraph){
			mergeGraph();
		}
		
		//save cycle graph
        String output = outputName.get();
		String graphName;
		if(!output.isEmpty()){
			graphName = output + "_graph.ser";
		}
		else{
			graphName = "graph.ser";
		}
        
		RandomAccessFile raf = new RandomAccessFile(graphName, "rw");
		FileOutputStream gout = new FileOutputStream(raf.getFD());
		ObjectOutputStream graph_oos = new ObjectOutputStream(gout);
		graph_oos.writeObject(globalGraph);
		graph_oos.close();
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
	
	private void mergeGraph(){
		Set<FieldInfo> fields = fieldMap.keySet();
		for(FieldInfo f : fields){
			List<Field> vertices = fieldMap.get(f);
			
			int i = 0;
			while(i < vertices.size()){
				int j = i + 1;
				while(j < vertices.size()){
					if(!mergeVertices(vertices.get(i), vertices.get(j), i, j)){
						j++;
					}
				}
				i++;
			}
		}
	}
	
	//pass in vertex index in list to speed up deletion
	private boolean mergeVertices(Field v0, Field v1, int ind0, int ind1){
		//outgoing-edge sets
		System.out.println("merging vertices " + v0 + " and " + v1);
		if(globalGraph.containsEdge(v0, v1) || globalGraph.containsEdge(v1, v0)) return false;
		
		Set<BlockEdge> outEdges0 = globalGraph.outgoingEdgesOf(v0);
		Set<BlockEdge> outEdges1 = globalGraph.outgoingEdgesOf(v1);
		if(outEdges0.size() != outEdges1.size()){
			return false;
		}
		
		//incoming-edge sets
		Set<BlockEdge> inEdges0 = globalGraph.incomingEdgesOf(v0);
		Set<BlockEdge> inEdges1 = globalGraph.incomingEdgesOf(v1);
		if(inEdges0.size() != inEdges1.size()){
			return false;
		}
		
		
		//SourceLocation block = null;
		
		for(BlockEdge e0 : outEdges0){
			/*if(block == null){
				block = e0.loc;
			}*/
			Field target0 = globalGraph.getEdgeTarget(e0);
			boolean match = false;
			for(BlockEdge e1 : outEdges1){
				/*if(!e1.loc.equals(block)) {
					return false;
				}*/
				Field target1 = globalGraph.getEdgeTarget(e1);
				if(target0.isField && target1.isField){
					if(target0.statField.equals(target1.statField) && e0.loc.equals(e1.loc)) {
						match = true;
					}
				}
			}
			if(!match){
				System.out.println("adjacent nodes didn't match");
				return false;
			}
		}
		
		
		for(BlockEdge e0 : inEdges0){
			/*if(block == null){
				block = e0.loc;
			}*/
			Field source0 = globalGraph.getEdgeSource(e0);
			boolean match = false;
			for(BlockEdge e1 : inEdges1){
				/*if(!e1.loc.equals(block)){
					return false;
				}*/
				Field source1 = globalGraph.getEdgeSource(e1);
				if(source0.isField && source1.isField){
					if(source0.statField.equals(source1.statField) && e0.loc.equals(e1.loc)){
						match = true;
					}
				}
			}
			if(!match) {
				System.out.println("adjacent ndoes didn't match");
				return false;
			}
		}
		
		System.out.println("merging!");
		v0.merged = true;
		
		
		for(BlockEdge e : outEdges1){
			BlockEdge newE = globalGraph.addEdge(v0, globalGraph.getEdgeTarget(e));
			if(newE != null) newE.loc = e.loc;
		}
		for(BlockEdge e : inEdges1){
			BlockEdge newE = globalGraph.addEdge(globalGraph.getEdgeSource(e), v0);
			if(newE != null) newE.loc = e.loc;
		}
		globalGraph.removeVertex(v1);
		fieldMap.get(v1.statField).remove(ind1);
		
		return true;
	}
}
