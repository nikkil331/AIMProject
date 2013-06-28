public class SyncBlockTest23 {
	private Integer x = 0;
	public static void main(String[] args){
		SyncBlockTest23 sbt = new SyncBlockTest23();
		synchronized(sbt.x){
			sbt.x = 5;
		}
	}
}
