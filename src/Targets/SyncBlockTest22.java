public class SyncBlockTest22 {
	Integer[] arr = {1,2,3};
	public static void main(String[] args){
		SyncBlockTest22 sbt = new SyncBlockTest22();
		synchronized(sbt.arr){
			sbt.arr = new Integer[2];
		}
	}
}
