import acme.util.decorations.Decoration;
import acme.util.decorations.DecorationFactory;
import acme.util.decorations.DefaultValue;
import acme.util.option.CommandLine;
import rr.event.AcquireEvent;
import rr.event.ReleaseEvent;
import rr.event.VolatileAccessEvent;
import rr.state.ShadowThread;
import rr.tool.Tool;

public class AcquireTool extends Tool{
	
	final Tool next;
	public static Decoration<ShadowThread, Boolean> synced = ShadowThread.makeDecoration("synced", 
			DecorationFactory.Type.SINGLE, new DefaultValue<ShadowThread, Boolean>(){
				public Boolean get(ShadowThread t){ return new Boolean(false);}
		});
	public AcquireTool(String name, Tool next, CommandLine commandLine) {
		super(name, next, commandLine);
		this.next = next;
	}
	
	@Override
	public void acquire(AcquireEvent e){
		synced.set(e.getThread(), true);
	}
	
	@Override
	public void release(ReleaseEvent e){
		synced.set(e.getThread(), false);
	}
	@Override
	public void volatileAccess(VolatileAccessEvent e){
		if(synced.get(e.getThread())){
			if(e.isWrite()){
				System.out.println("Thread " + e.getThread().getTid() + " wrote field first.");
				synced.set(e.getThread(), false);
			}
			else{
				System.out.println("Thread " + e.getThread().getTid() + " read field first.");
				synced.set(e.getThread(), false);
			}
		}
	}

}
