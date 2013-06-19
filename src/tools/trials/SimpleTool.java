import acme.util.option.CommandLine;
import rr.event.AccessEvent;
import rr.event.MethodEvent;
import rr.tool.Tool;


public class SimpleTool extends Tool{

	final Tool next;
	
	public SimpleTool(String name, Tool next, CommandLine commandLine) {
		super(name, next, commandLine);
		this.next = next;
	}
	@Override
	public void access(AccessEvent e){
		if(e.isWrite()){
			System.out.println("A field was written");
		}
		else{
			System.out.println("A field was read");
		}
	}
    /*@Override
	public void enter(MethodEvent e){
		System.out.println("A method was entered");
	}
	
	@Override
	public void exit(MethodEvent e){
		System.out.println("A method was exited");
		}*/
}
