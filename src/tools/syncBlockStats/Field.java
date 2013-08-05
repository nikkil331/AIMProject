package tools.syncBlockStats;
import java.io.Serializable;

import rr.meta.SourceLocation;
import rr.state.ShadowVar;

public class Field implements ShadowVar, Serializable{
	public SourceLocation loc;
	public String name;
	public Object target;
		
	@Override
	public String toString(){
		return name;
	}
}

