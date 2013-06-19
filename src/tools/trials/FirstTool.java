
import acme.util.decorations.Decoration;
import acme.util.option.CommandLine;
import rr.event.AccessEvent;
import rr.state.ShadowVar;
import rr.tool.Tool;
import rr.annotations.Abbrev;



public class FirstTool extends Tool{

	private final Tool next;
	
	public FirstTool(String name, Tool next, CommandLine commandLine) {
		super(name, next, commandLine);
		this.next = next;
	}

	@Override
	public void access (AccessEvent e){
		String response = "";
		if(e.isWrite()){
			if(e.getOriginalShadow() instanceof ReadWriteCount){
				ReadWriteCount c = (ReadWriteCount)e.getOriginalShadow();
				e.putShadow(c.incWrite());
				response = "This field has been written " + (c.getWrite()) + " times.";
			}
			else{
				e.putShadow(new ReadWriteCount().incWrite());
				response = "This field has been written 1 time.";
			}
		}
		else{
			if(e.getOriginalShadow() instanceof ReadWriteCount){
				ReadWriteCount c = (ReadWriteCount)e.getOriginalShadow();
				e.putShadow(c.incRead());
				response = "This field has been read " + (c.getRead()) + " times.";
			}
			else{
				e.putShadow(new ReadWriteCount().incRead());
				response = "This field has been read 1 time.";
			}
		}
		System.out.println(response);
		
	}
	

}
