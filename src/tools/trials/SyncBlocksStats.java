import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.Stack;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;

import rr.meta.ClassInfo;

import acme.util.decorations.Decoration;
import acme.util.decorations.DecorationFactory;
import acme.util.decorations.DefaultValue;
import acme.util.option.CommandLine;
import rr.tool.Tool;
import rr.event.AccessEvent;
import rr.event.AcquireEvent;
import rr.event.ArrayAccessEvent;
import rr.event.FieldAccessEvent;
import rr.event.ReleaseEvent;
import rr.event.VolatileAccessEvent;
import rr.state.ShadowLock;
import rr.state.ShadowThread;
import rr.state.ShadowVar;


public class SyncBlocksStats extends Tool {
	
	private static Integer  Total = new Integer(0);
	private static Integer Read = new Integer(0);
	private static Integer Write = new Integer(0);
	private static Integer None = new Integer(0);
	
	private static DecorationFactory<ShadowThread> fac = new DecorationFactory<ShadowThread>();
	private static Decoration<ShadowThread, Stack<AccessTracker>> locks =fac.make("locks", DecorationFactory.Type.SINGLE, 
				new DefaultValue<ShadowThread, Stack<AccessTracker>>(){
					public Stack<AccessTracker> get(ShadowThread t) { return new Stack<AccessTracker>();}
			}); 
	
	private class AccessTracker{
		//ClassInfo cinfo;
		Object o;
		boolean r = false;
		boolean w = false;
		
		public AccessTracker(AcquireEvent ae){
			this.o = ae.getLock().getLock();
			//this.cinfo = ae.getInfo().getEnclosing().getOwner();
		}
	}
		
	public SyncBlocksStats(String name, Tool next, CommandLine commandLine) {
		super(name, next, commandLine);	
	}
	
	@Override
	public void acquire(AcquireEvent ae){
		Stack<AccessTracker> localLocks = locks.get(ae.getThread());
		
		localLocks.push(new AccessTracker(ae));
		
		synchronized(Total){
			Total++;
		}
	}
	@Override
	public void release(ReleaseEvent re){
		Stack<AccessTracker> localLocks = locks.get(re.getThread());
		
		AccessTracker at = localLocks.pop();
		if(at.w){
			synchronized(Write){
				Write++;
			}
		}
		else if(at.r){
			synchronized(Read){
				Read++;
			}
		}
		else{
			synchronized(None){
				None++;
			}
		}
	}
	@Override
	public void access(AccessEvent ae){	
		
		Stack<AccessTracker> localLocks = locks.get(ae.getThread());
		
		Object self = getLocationAccessed(ae);
		
		for(AccessTracker at : localLocks){
			if (at.o == ae.getTarget() || at.o == self){
				if(ae.isWrite()){
					at.w = true;
				}
				else{
					at.r = true;
				}
			}
		}
	}
	public Object getLocationAccessed(AccessEvent ae){
		Object target = ae.getTarget();
		
		String accessed = "";
		if(ae.getKind() == AccessEvent.Kind.FIELD || ae.getKind() == AccessEvent.Kind.VOLATILE){
			String field = "\"" + ((FieldAccessEvent)ae).getInfo().getField().getName() + "\"";
			
			//if field is static, won't have lock on it anyway so return null
			if(target == null){
				/*try {
					ClassInfo cinfo = ae.getAccessInfo().getEnclosing().getOwner();
					
					target = Class.forName(cinfo.getName(), false, null).newInstance();
					accessed = "target[" + field + "]";
				} catch (ClassNotFoundException e) {
					accessed = "target";
					e.printStackTrace();
				} catch (InstantiationException e) {
					accessed = "target";
					e.printStackTrace();
				} catch (IllegalAccessException e) {
					accessed = "target";
					e.printStackTrace();
				}*/
				accessed = "target";
			}
			else {accessed = "target[" + field + "]";}
		}
		if(ae.getKind() == AccessEvent.Kind.ARRAY){
			accessed = "target[" + Integer.toString(((ArrayAccessEvent)ae).getIndex()) + "]"; 
		}
		
		
		Object self = null;
		ScriptEngineManager manager = new ScriptEngineManager();
		ScriptEngine engine = manager.getEngineByName("js");
		engine.put("target", target);
		
		//System.out.println(accessed);
		
		try {
			self = engine.eval(accessed);
		} catch (ScriptException e) {
			e.printStackTrace();
		}
		
		return self;
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
	public void fini(){
		System.out.printf("result.append(%d)\n" +
				"result.append(%d)\n" +
				"result.append(%d)\n" +
				"result.append(%d)\n", Total, Read, Write, None);
	}
}
