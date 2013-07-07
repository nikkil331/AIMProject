
public class SyncBlockTest4 {
	String field = "hey";
	
	public static void main(String[] args){
		SyncBlockTest4 sbt = new SyncBlockTest4();
		synchronized(sbt){
			sbt.field = "what?";
		}
	}
}
