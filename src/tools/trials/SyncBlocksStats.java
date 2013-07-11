import java.util.Stack;
import java.util.concurrent.ConcurrentHashMap;

import rr.meta.ClassInfo;
import rr.meta.SourceLocation;
import acme.util.decorations.Decoration;
import acme.util.decorations.DecorationFactory;
import acme.util.decorations.DefaultValue;
import acme.util.option.CommandLine;
import rr.tool.Tool;
import rr.event.AccessEvent;
import rr.event.AcquireEvent;
import rr.event.FieldAccessEvent;
import rr.event.MethodEvent;
import rr.event.ReleaseEvent;
import rr.event.VolatileAccessEvent;
import rr.state.ShadowLock;
import rr.state.ShadowThread;
import rr.state.ShadowVar;


public class SyncBlocksStats extends Tool {
	
	private static boolean testOutput = false;
	
	//private Counter count = new Counter();
	
	private static DecorationFactory<ShadowThread> fac = new DecorationFactory<ShadowThread>();
	private static Decoration<ShadowThread, Stack<AccessTracker>> locks =fac.make("locks", DecorationFactory.Type.SINGLE, 
				new DefaultValue<ShadowThread, Stack<AccessTracker>>(){
					public Stack<AccessTracker> get(ShadowThread t) { return new Stack<AccessTracker>();}
			}); 
	private static ConcurrentHashMap<SourceLocation, Counter> pcMap = new ConcurrentHashMap<SourceLocation, Counter>();
	
	private static class Counter{
		int  Total = 0;
		int Read = 0;
		int Write = 0;
		int None = 0;
	}
	
	private class AccessTracker{
		ShadowLock lock;
		Object o;
		boolean r = false;
		boolean w = false;
		SourceLocation loc;
		
		public AccessTracker(AcquireEvent ae){
			this.lock = ae.getLock();
			this.o = ae.getLock().getLock();
			this.loc = ae.getInfo().getLoc();
		}
	}
		
	public SyncBlocksStats(String name, Tool next, CommandLine commandLine) {
		super(name, next, commandLine);
	}
	
	@Override
	public void acquire(AcquireEvent ae){
		System.out.println("Lock at line " + ae.getInfo().getLoc().getLine());
		
		if(testOutput){
			System.out.println("thread " + ae.getThread().getTid() + " acquired " + ae.getLock().getLock().toString());
		}
		
		
		Stack<AccessTracker> localLocks = locks.get(ae.getThread());
		AccessTracker at = new AccessTracker(ae);
		Counter newCount = new Counter();
		newCount.Total++;
		if(pcMap.putIfAbsent(at.loc, newCount) != null){
			Counter prevCount = pcMap.get(at.loc);
			synchronized(prevCount){
				prevCount.Total++;
			}
		}
		
		localLocks.push(at);
	}
	@Override
	public void release(ReleaseEvent re){
		if(testOutput){
			System.out.println("thread " + re.getThread().getTid() + " released " + re.getLock().getLock().toString());
		}
		
		Stack<AccessTracker> localLocks = locks.get(re.getThread());
		
		AccessTracker at = localLocks.pop();
		Counter count = pcMap.get(at.loc);
		
		synchronized(count){
			if(at.w){
				count.Write++;
			}
			else if(at.r){
				count.Read++;
			}
			else{
				count.None++;
			}
		}
	}
	@Override
	public void access(AccessEvent ae){
		Stack<AccessTracker> localLocks = locks.get(ae.getThread());
		
		Object target = ae.getTarget();

		Object self = ae.getAccessed();
		
		for(AccessTracker at : localLocks){
			if (at.o == self){
				if(ae.isWrite()){
					at.w = true;
				}
				else{
					at.r = true;
				}
			}
			else if(at.o == target){
				at.r = true;
			}
			else if(at.o instanceof Class){
				Class<?> heldClass = (Class<?>)at.o;
				ClassInfo cinfo = ae.getAccessInfo().getEnclosing().getOwner();
				if(heldClass.getName().equals(cinfo.getName())) at.r = true;
			}
		}
	}
	
	
	
	@Override
	public void volatileAccess(VolatileAccessEvent e){
		access(e);
	}
	@Override
	public ShadowVar makeShadowVar(AccessEvent ae){
		return new ShadowVar(){};
	}
	
	@Override
	public void enter(MethodEvent me){
		if(testOutput){
			System.out.println(me.toString());
		}
		
	}
	@Override
	public void exit(MethodEvent me){
		if(testOutput){
			System.out.println(me.toString());
		}
	}
	
	@Override
	public void fini(){
		System.out.println("Number of Static Synchronized Blocks = " + pcMap.size());
		for(SourceLocation loc : pcMap.keySet()){
			Counter count = pcMap.get(loc);
			synchronized(count){
				System.out.printf("result['%s line %d'] = {\"total\" : %d , \"read\" : %d, \"write\" : %d, \"neither\" : %d}\n", 
						loc.getFile().replace('/', '.'), loc.getLine(), count.Total, count.Read, count.Write, count.None);
			}
		}
		
	}
}
