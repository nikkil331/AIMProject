public class SyncBlockTest2 {
	int field = 0;
	
	public static void main(String[] args){
		SyncBlockTest2 sbt = new SyncBlockTest2();
		synchronized(sbt){
			int x = sbt.field;
		}
	}
}
