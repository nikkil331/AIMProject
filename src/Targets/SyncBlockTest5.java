
public class SyncBlockTest5 {
	int field = 0;
	public static void main(String[] args){
		SyncBlockTest5 sbt = new SyncBlockTest5();
		
		synchronized(sbt){
			int x = sbt.field;
		}
		synchronized(sbt){
			sbt.field = 1;
		}
		synchronized(sbt){
			int x = 5;
		}
	}
}
