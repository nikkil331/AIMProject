
public class SyncBlockTest4 {
	int field = 0;
	
	public static void main(String[] args){
		SyncBlockTest4 sbt = new SyncBlockTest4();
		synchronized(sbt){
			sbt.field = 1;
		}
	}
}
