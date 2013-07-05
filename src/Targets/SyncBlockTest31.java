public class SyncBlockTest31 {
	Integer x = 0;
	public SyncBlockTest31(){
		synchronized(this){
			this.x = 2;
		}
	}
	public static void main(String[] args){
		SyncBlockTest31 sbt = new SyncBlockTest31();
	}
}
