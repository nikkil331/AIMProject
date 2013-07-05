
public class SyncBlockTest29 {
	public static void main(String[] args){
		SyncBlockTest29 sbt = new SyncBlockTest29();
		sbt = new SyncBlockTest29(); 
		synchronized(sbt){
			sbt = new SyncBlockTest29();
		}
	}
}
