import acme.util.option.CommandLine;
import rr.event.AcquireEvent;
import rr.event.NewThreadEvent;
import rr.event.ReleaseEvent;
import rr.event.VolatileAccessEvent;
import rr.tool.Tool;


public class ThreadIDTool extends Tool{

	private final Tool next;
	public ThreadIDTool(String name, Tool next, CommandLine commandLine) {
		super(name, next, commandLine);
		this.next = next;
	}
	
	@Override
	public void create(NewThreadEvent e){
		System.out.println("Thread " + e.getThread().getTid() + " was created.");
		super.create(e);
	}
	@Override
	public void acquire(AcquireEvent e){
		System.out.println("Thread " + e.getThread().getTid() + " acquired a lock.");
		super.acquire(e);
	}
	@Override
	public void release(ReleaseEvent e){
		System.out.println("Thread " + e.getThread().getTid() + " released a lock.");
	}
	@Override
	public void volatileAccess(VolatileAccessEvent e){
		if(e.isWrite()){
			System.out.println("Thread " + e.getThread().getTid() + " wrote a volatile field");
		}
		else{
			System.out.println("Thread " + e.getThread().getTid() + " read a volatile field");
		}
	}

}
