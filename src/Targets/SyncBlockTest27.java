public class SyncBlockTest27 {
	private static Integer x = 0;
	public static void main(String[] args){
		SyncBlockTest27 sbt = new SyncBlockTest27();
		synchronized(sbt.x){
			sbt.x = 7;
		}
	}
}
