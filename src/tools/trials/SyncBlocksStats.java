import java.io.File;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.Arrays;
import java.util.Stack;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;

import rr.instrument.Constants;

import rr.RRMain;
import rr.meta.ClassInfo;

import acme.util.decorations.Decoration;
import acme.util.decorations.DecorationFactory;
import acme.util.decorations.DefaultValue;
import acme.util.io.URLUtils;
import acme.util.option.CommandLine;
import rr.tool.RR;
import rr.tool.Tool;
import rr.event.AccessEvent;
import rr.event.AcquireEvent;
import rr.event.ArrayAccessEvent;
import rr.event.ClassInitializedEvent;
import rr.event.FieldAccessEvent;
import rr.event.MethodEvent;
import rr.event.ReleaseEvent;
import rr.event.VolatileAccessEvent;
import rr.state.ShadowLock;
import rr.state.ShadowThread;
import rr.state.ShadowVar;


public class SyncBlocksStats extends Tool {
	
	private static boolean testOutput = false;
	
	private static Integer  Total = new Integer(0);
	private static Integer Read = new Integer(0);
	private static Integer Write = new Integer(0);
	private static Integer None = new Integer(0);
	
	private static ScriptEngine engine;
	
	private static DecorationFactory<ShadowThread> fac = new DecorationFactory<ShadowThread>();
	private static Decoration<ShadowThread, Stack<AccessTracker>> locks =fac.make("locks", DecorationFactory.Type.SINGLE, 
				new DefaultValue<ShadowThread, Stack<AccessTracker>>(){
					public Stack<AccessTracker> get(ShadowThread t) { return new Stack<AccessTracker>();}
			}); 
	
	private class AccessTracker{
		Object o;
		boolean r = false;
		boolean w = false;
		
		public AccessTracker(AcquireEvent ae){
			this.o = ae.getLock().getLock();
		}
	}
		
	public SyncBlocksStats(String name, Tool next, CommandLine commandLine) {
		super(name, next, commandLine);
		
		ScriptEngineManager manager = new ScriptEngineManager();
		engine = manager.getEngineByName("js");
	}
	
	@Override
	public void acquire(AcquireEvent ae){
		if(testOutput){
			System.out.println("thread " + ae.getThread().getTid() + " acquired " + ae.getLock().getLock().toString());
		}
		
		
		Stack<AccessTracker> localLocks = locks.get(ae.getThread());
		localLocks.push(new AccessTracker(ae));
		
		synchronized(Total){
			Total++;
		}
	}
	@Override
	public void release(ReleaseEvent re){
		if(testOutput){
			System.out.println("thread " + re.getThread().getTid() + " released " + re.getLock().getLock().toString());
		}
		
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
		
		Object target = ae.getTarget();
		if(target == null){
			try {
				ClassInfo cinfo = ae.getAccessInfo().getEnclosing().getOwner();
				
				target = Class.forName(cinfo.getName().replace('/', '.'), false, RRMain.loader);
			} catch (ClassNotFoundException e) {
				e.printStackTrace();
			} 
		}
		
		/*Object self = null;
		synchronized(engine){
			self = getLocationAccessed(ae, target);
		
			if(testOutput){
				if(self != null){
					System.out.println("thread " + ae.getThread().getTid() + (ae.isWrite() ? " wrote " : " read " ) + self.toString());}
				else {
					System.out.println("thread " + ae.getThread().getTid() + (ae.isWrite() ? " wrote" : " read ") + " null self");
				}
			}
		}*/
		
		Object self = null;
		if(ae.getKind() == AccessEvent.Kind.FIELD){
			self = ((FieldAccessEvent)ae).getAccessed();
		}
		
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
				if(at.o.toString().equals(target.toString())) at.r = true;
			}
		}
	}
	public Object getLocationAccessed(AccessEvent ae, Object target){

		String accessed = "";
		if(ae.getKind() == AccessEvent.Kind.FIELD || ae.getKind() == AccessEvent.Kind.VOLATILE){
			String field = "\"" + ((FieldAccessEvent)ae).getInfo().getField().getName() + "\"";
			
			//if field is static
			if(target instanceof Class){
				String classpath = Arrays.toString(URLUtils.getURLArrayFromString(System.getProperty("user.dir"),
						RR.classPathOption.get()));
				/*accessed = "var importer = new JavaImporter(Packages." + ((Class)target).getName() + ") \n" +
								  "with(importer) {\n" +
								  	 ((Class)target).getName() + "[" + field + "]\n" +
								  "}";*/
				accessed = "importPackage(Packages." + ((Class)target).getName() + ") \n" +
							((Class)target).getName() + "[" + field + "]\n";
				System.out.println(accessed);
				/*try {
					target = ((Class)target).newInstance();
					accessed = "target[" + field + "]";
				} catch (InstantiationException e) {
					accessed = "target";
					e.printStackTrace();
				} catch (IllegalAccessException e) {
					accessed = "target";
					e.printStackTrace();
				}*/
			}
			else {accessed = "target[" + field + "]";}
		}
		if(ae.getKind() == AccessEvent.Kind.ARRAY){
			accessed = "target[" + Integer.toString(((ArrayAccessEvent)ae).getIndex()) + "]"; 
		}
		
		
		Object self = null;
		engine.put("target", target);
		
		
		
		try {
			self = engine.eval(accessed);
		
			if(testOutput){
				System.out.println("Expression attempted was = " + accessed + " where target = " + target.toString() + " in thread " + ae.getThread().getTid());
				if(self == null) {
					System.out.println("Engine evaluated self to null");
				}
			}
		}catch (ScriptException e) {
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
	public void classInitialized(ClassInitializedEvent e){
		if(testOutput){
			System.out.println(e.getRRClass().getName() + " was initialized");
		}
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
		System.out.printf("result = {\"total\" : %d , \"read\" : %d, \"write\" : %d, \"neither\" : %d}\n", Total, Read, Write, None);
	}
}
