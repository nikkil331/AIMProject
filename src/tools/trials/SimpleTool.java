import acme.util.option.CommandLine;
import rr.event.AccessEvent;
import rr.event.MethodEvent;
import rr.state.ShadowVar;
import rr.tool.Tool;

public class SimpleTool extends Tool{
	final Tool next;
	
	public SimpleTool(String name, Tool next, CommandLine commandLine) {
		super(name, next, commandLine);
		this.next = next;
	}
	
	@Override
	public void access(AccessEvent fae) {
		if(fae.isWrite()){
			System.out.println("This field was written.");
		}
		else{
			System.out.println("This field was read.");
		}
		fae.putShadow(new ShadowVar(){});
	}
	
	@Override
	public void enter(MethodEvent me) {
		System.out.println("A method was entered.");
	}
	@Override
	public void exit(MethodEvent me) {
		System.out.println("A method was exited.");
	}
	@Override
	public void fini(){
	    
	}
}
