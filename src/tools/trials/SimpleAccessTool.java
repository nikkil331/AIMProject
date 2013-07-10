import acme.util.option.CommandLine;
import rr.event.AccessEvent;
import rr.event.FieldAccessEvent;
import rr.tool.Tool;

public class SimpleAccessTool extends Tool{

	public SimpleAccessTool(String name, Tool next, CommandLine commandLine) {
		super(name, next, commandLine);
	}
	
	@Override
	public void access(AccessEvent e){
		if(e.getKind() == AccessEvent.Kind.FIELD){
			FieldAccessEvent fae = (FieldAccessEvent)e;
			System.out.println(fae.getAccessed());
		}
	}
}
