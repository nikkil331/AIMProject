public class SyncBlockTest3 {
	int field = 0;
	
	public static void main(String[] args){
		SyncBlockTest3 sbt = new SyncBlockTest3();
		synchronized(sbt){
			int x = 5;
		}
	}

}
