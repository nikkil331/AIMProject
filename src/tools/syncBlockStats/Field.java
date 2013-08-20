package tools.syncBlockStats;
import java.io.Serializable;

import rr.meta.FieldInfo;
import rr.meta.SourceLocation;
import rr.state.ShadowVar;

public class Field implements ShadowVar, Serializable{
	public SourceLocation loc = SourceLocation.NULL;
	public String name = "";
	
	public boolean isField = false;
	public FieldInfo statField = null;
	
	public boolean merged = false;
		
	@Override
	public String toString(){
		return name;
	}
}

