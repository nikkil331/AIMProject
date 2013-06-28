public class SyncBlockTest26 {
	private Integer x = 0;
	private Character c = 'c';
	public static void main(String[] args){
		SyncBlockTest26 sbt = new SyncBlockTest26();
		synchronized(sbt.x){
			sbt.x.byteValue();
			sbt.x.intValue();
		}
		synchronized(sbt.c){
			sbt.c.charValue();
			sbt.c.hashCode();
		}
	}
}
